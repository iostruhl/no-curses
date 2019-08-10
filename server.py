from PodSixNet.Server import Server
from PodSixNet.Channel import Channel
from fuzzywuzzy import process
from util import sheets_logging
from time import sleep
from random import shuffle
import util.card as card
from copy import deepcopy
import sys

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        self.name = "ANON"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        self._server.remove_channel(self)

    ##################################
    ### Network specific callbacks ###
    ##################################

    def Network_name(self, data):
        print("Client", self.name, "sent", data)
        if self._server.untracked:
            self.name = data['name']
        else:
            # chooses the best matched full name, so that we can log easily at the end
            choices = [
                "Ben Harpe", "Alex Wulff", "Alex Mariona", "Owen Schafer",
                "Isaac Struhl"
            ]
            self.name = process.extract(data['name'], choices, limit=1)[0][0]

        self._server.handle_name(self.name)

    def Network_ready(self, data):
        print("Client", self.name, "sent", data)
        assert (self.name == data['name'])
        self._server.handle_ready()

    def Network_bid(self, data):
        print("Client", self.name, "sent", data)
        self._server.handle_bid(self.name, data['bid'])

    def Network_play(self, data):
        print("Client", self.name, "sent", data)
        self._server.handle_play_card(self.name, data['card'])


class OHServer(Server):
    channelClass = ClientChannel

    def __init__(self, untracked=False, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        # Internal
        self.untracked = untracked
        self.user_channels = []
        self.initialize_new_game = True
        self.ready_count = 0
        self.ordered_names = []

        # In game specific
        self.waiting_for_user = False
        self.should_deal_hand = True
        self.next_to_bid_first = 0

        # Public (with hand display caveat)
        self.boardstate = {
            'activity'      : "bid",
            'next_to_act'   : 0,
            'hand_num'      : 1,
            'trump_card'    : None,
            'led_card'      : None,
            'players'       : dict(),
            'score_history' : dict()
        }

        print("Server launched")

    def Connected(self, channel, addr):
        if len(self.user_channels) < 4:
            print("New channel", str(addr))
            self.user_channels.append(channel)

    def remove_channel(self, channel):
        self.ready_count -= 1
        print("Remove Player " + str(channel.name))
        self.user_channels.remove(channel)
        if not self.initialize_new_game:
            self.send_pause()

    def send_pause(self):
        # DO SOME OTHER STUFF HERE
        self.send_all({'action': "pause"})

    def send_all(self, data):
        print("Server: sending to ALL :", data)
        [channel.Send(data) for channel in self.user_channels]

    def send_one(self, name, data, echo=True):
        for channel in self.user_channels:
            if channel.name == name:
                if echo:
                    print("Server: sending to", name, ":", data)
                channel.Send(data)

    def handle_name(self, name):
        self.send_one(name, {'action': "server_name", 'name': name})
        self.send_all({
            'action': "names",
            'names': [channel.name for channel in self.user_channels]
        })
        if name not in self.boardstate['players']:
            self.boardstate['players'][name] = {
                'display_name'  : self.display_name(name),
                'id'            : None,
                'bid'           : None,
                'score'         : 0,
                'cards_in_hand' : [],
                'card_in_play'  : None,
                'tricks_taken'  : 0,
                'dealer'        : False
            }

    def display_name(self, name):
        if name.split(' ')[0].lower == "alex":
            return name.split(' ')[1]
        return name.split(' ')[0]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

    # --- Game Logic ---
    def handle_ready(self):
        self.ready_count += 1
        if self.ready_count == 4:
            self.start_or_resume_game()

    def start_or_resume_game(self):
        print("Game starting.")
        if self.initialize_new_game:
            # Set the ids of the players to {0..3}
            # Indicating their position at the start.
            self.ordered_names = [
                player for player in self.boardstate['players']
            ]
            shuffle(self.ordered_names)
            for name in self.boardstate['players']:
                self.boardstate['players'][name]['id'] = self.ordered_names.index(name)
            self.boardstate['players'][self.ordered_names[3]]['dealer'] = True

            # This initialization should happen only once.
            self.initialize_new_game = False

        # If a user disconnected, this may be True;
        # setting it to False will replay the last action.
        self.waiting_for_user = False
        # Figures out based entirely on the current boardstate what to do,
        # and then executes that action.
        while True:
            self.do_next_action()
            self.Pump()

    def do_next_action(self):
        '''
        activity (bid, play)
        next_to_act (int, id)
        hand_num (int)
        trump card (Card?)
        led card (Card?) # for validation only
        players: {
            name: {
                id (int)
                score (int)
                bid (int?)
                tricks taken (int?)
                cards in hand (Card[])
                card in play (Card?)
            }
        }
        '''
        # Busy wait until a user has responded.
        if self.waiting_for_user:
            sleep(0.1)
            return

        if self.should_deal_hand:
            print('dealing')
            deck = card.Deck()
            deck.shuffle()
            for name in self.boardstate['players']:
                self.boardstate['players'][name]['cards_in_hand'] = [
                    deck.next().to_array() for _ in range(self.boardstate['hand_num'])
                ]
            # Set the trump card if there are still cards remaining in the deck.
            self.boardstate['trump_card'] = deck.next().to_array()
            self.should_deal_hand = False

        if self.shouldBid():
            print('bidding')
            self.boardstate['activity'] = "bid"
            for name in self.boardstate['players']:
                self.send_one(
                    name, {
                        'action': "update",
                        'boardstate': self.hide_non_player_hands(name=name)
                    })
            self.waiting_for_user = True
        elif self.shouldPlay():
            print('playing')
            self.boardstate['activity'] = "play"
            for name in self.boardstate['players']:
                self.send_one(
                    name, {
                        'action': "update",
                        'boardstate': self.hide_non_player_hands(name=name)
                    })
            self.waiting_for_user = True
        else:
            print('finishing')
            self.finish_trick()
            self.maybe_finish_hand()
            self.maybe_finish_game()

    # Precondition: hand is dealt.
    def shouldBid(self):
        # If anyone does not have a bid set, we should bid.
        for name in self.boardstate['players']:
            if self.boardstate['players'][name]['bid'] is None:
                return True
        return False

    # Precondition: everyone has a bid set.
    def shouldPlay(self):
        # If anyone doesn't have a card in play, we should play.
        for name in self.boardstate['players']:
            if self.boardstate['players'][name]['card_in_play'] is None:
                return True
        return False

    def handle_bid(self, name: str, bid: int):
        # Increment next_to_act mod 4
        self.boardstate['next_to_act'] = (self.boardstate['next_to_act'] +
                                          1) % 4
        self.boardstate['players'][name]['bid'] = bid
        self.waiting_for_user = False

    def handle_play_card(self, name: str, card: list):
        # Increment next_to_act mod 4
        self.boardstate['next_to_act'] = (self.boardstate['next_to_act'] +
                                          1) % 4
        if self.boardstate['led_card'] is None:
            self.boardstate['led_card'] = card
        self.boardstate['players'][name]['card_in_play'] = card
        self.boardstate['players'][name]['cards_in_hand'].remove(card)
        self.waiting_for_user = False

    def finish_trick(self):
        winner_name = max(
            self.boardstate['players'],
            key=lambda name: card.trick_value(
                card=self.boardstate['players'][name]['card_in_play'],
                trump_card=self.boardstate['trump_card'],
                led_card=self.boardstate['led_card']))
        # Set the winner to next to act.
        self.boardstate['next_to_act'] = self.boardstate['players'][
            winner_name]['id']
        # Clear the led card.
        self.boardstate['led_card'] = None
        # Increment winner's trick count.
        self.boardstate['players'][winner_name]['tricks_taken'] += 1
        # Clear cards in play.
        for name in self.boardstate['players']:
            self.boardstate['players'][name]['card_in_play'] = None

    # Precondition: No cards are in play (guaranteed by finish_trick)
    def maybe_finish_hand(self):
        # Do not finish hand if there are still cards to be played.
        for name in self.boardstate['players']:
            if len(self.boardstate['players'][name]['cards_in_hand']) != 0:
                return

        # Update player states
        self.boardstate['score_history'][self.boardstate['hand_num']] = dict()
        for name in self.boardstate['players']:
            # Update score
            tricks_taken = self.boardstate['players'][name]['tricks_taken']
            bid = self.boardstate['players'][name]['bid']
            if tricks_taken == bid:
                self.boardstate['players'][name][
                    'score'] += 10 + tricks_taken**2
            else:
                diff = abs(tricks_taken - bid)
                self.boardstate['players'][name]['score'] -= int(
                    5 * (diff * (diff + 1)) / 2)
            # Reset the bid and tricks taken. Cards in hand and in play should already be correctly empty.
            self.boardstate['players'][name]['bid'] = None
            self.boardstate['players'][name]['tricks_taken'] = 0
            self.boardstate['players'][name]['dealer'] = False
            # Update the score history with the players and scores.
            self.boardstate['score_history'][self.boardstate['hand_num']][name] = \
                self.boardstate['players'][name]['score']

        # Reset or update relevant boardstate values.
        self.boardstate['players'][self.next_to_bid_first]['dealer'] = True
        self.next_to_bid_first = (self.next_to_bid_first + 1) % 4
        self.boardstate['next_to_act'] = self.next_to_bid_first
        self.boardstate['activity'] = "bid"
        self.boardstate['hand_num'] += 1
        self.boardstate['trump_card'] = None

    def maybe_finish_game(self):
        if self.boardstate['hand_num'] <= 13:
            return
        winner = max(
            self.boardstate['players'],
            key=lambda name: self.boardstate['players'][name]['score'])
        scores = [[name, self.boardstate['players'][name]['score']]
                  for name in self.boardstate['players']]
        self.send_all({
            'action'     : "end_game",
            'boardstate' : self.boardstate,
            'winner'     : winner,
            'scores'     : scores
        })
        if not self.untracked:
            sheets_logging.log_game(scores)

        # Wait for the user to ctrl c. Eventually we can just reset and start another game immediately.
        while True:
            sleep(1000)

    def hide_non_player_hands(self, name):
        clean_boardstate = deepcopy(self.boardstate)
        for player_name in clean_boardstate['players']:
            if name != player_name:
                clean_boardstate['players'][player_name]['cards_in_hand'] = [
                    card.Card().to_array() for _ in range(len(
                    self.boardstate['players'][name]['cards_in_hand']))
                ]
        return clean_boardstate


# Run the server
if __name__ == "__main__":
    # get command line argument of server, port
    if len(sys.argv) not in [2, 3]:
        print("Usage:", sys.argv[0], "host:port <untracked>")
        print("e.g.", sys.argv[0], "localhost:31425")
        print("or", sys.argv[0], "localhost:31425 untracked")
        exit(1)
    host, port = sys.argv[1].split(":")
    s = OHServer(untracked=(len(sys.argv) == 3), localaddr=(host, int(port)))
    try:
        s.Launch()
    except:
        print("\nServer killed by signal.")
