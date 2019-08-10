import sys
from sys import stdin, exit
from time import sleep
from util.card import Card
from util.graphics import GraphicsBoard
import shutil
from PodSixNet.Connection import connection, ConnectionListener


class Client(ConnectionListener):
    def __init__(self, host, port, name="ANON", sort_hand_ascending=False):
        self.Connect((host, port))
        print("Oh Hell client started")
        print("Ctrl-C to exit")
        self.name = name
        self.sort_hand_ascending = sort_hand_ascending
        self.gb = None
        # get a nickname from the user before starting
        connection.Send({"action": "name", "name": name})

    def Loop(self):
        connection.Pump()
        self.Pump()

    #################
    ### Built-ins ###
    #################

    def Network_connected(self, data):
        print("You are now connected to the server")

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()

    #######################################
    ### Network event/message callbacks ###
    #######################################

    def Network_server_name(self, data):
        print("Server set name to", data['name'])
        self.name = data['name']
        connection.Send({'action': "ready", 'name': self.name})

    def Network_names(self, data):
        print("*** users:", ', '.join([p for p in data['names']]), "***")

        # game is about to start; start up graphics
        # if len(data['names']) == 4:
        # self.gb = GraphicsBoard()

    def Network_pause(self, data):
        print("*** USER HAS DISCONNECTED, FATAL ***")
        exit(1)

    def Network_update(self, data):
        print("UPDATED!!!")
        if not self.gb:
            self.gb = GraphicsBoard()

        b = data['boardstate']

        # Reformat cards as Card objects
        if b['trump_card'] is not None:
            b['trump_card'] = Card(b['trump_card'][0], b['trump_card'][1])
        if b['led_card'] is not None:
            b['led_card'] = Card(b['led_card'][0], b['led_card'][1])
        for player in b['players']:
            b['players'][player]['cards_in_hand'] = [
                Card(card[0], card[1]) for card in b['players'][player]['cards_in_hand']
            ]

        if b['next_to_act'] != b['players'][self.name]['id']:
            # player is not the actor; just update screen
            self.gb.draw_board(b, self.name)
            return

        # player must be actor, should either bid or play
        assert b['next_to_act'] == b['players'][self.name]['id']

        if b['activity'] == 'bid':
            bid = self.gb.get_bid(b, self.name)
            connection.Send({'action': 'bid', 'bid': bid})
        else:
            play = self.gb.get_play(b, self.name)
            played_card = b['players'][self.name][play]
            connection.Send({'action': 'play', 'play': played_card.to_array()})

    def Network_end_game(self, data):
        b = data['boardstate']
        w = data['winner']
        self.gb.end_game(b, w)


if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        print("Usage:", sys.argv[0], "host:port name [--sort_hand_ascending]")
        print("e.g.", sys.argv[0], "localhost:8080 Isaac")
    else:
        size = shutil.get_terminal_size()
        assert (size.columns >= 181 and size.lines >= 58), \
            "Resize terminal to at least 181x58"
        host, port = sys.argv[1].split(":")
        c = Client(host,
                   int(port),
                   name=sys.argv[2],
                   sort_hand_ascending=(len(sys.argv) == 4))
        while 1:
            c.Loop()
            sleep(0.001)
