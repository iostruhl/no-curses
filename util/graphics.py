import curses
from curses import panel
from card import Card

class GraphicsBoard:
    sizes = {
        'padding'                   : 1,
        'vertical_spacing'          : 1,
        'horizontal_spacing'        : 5,
        'card_height'               : 11,
        'card_width'                : 13,
        'player_info_window_height' : 6,
        'player_info_window_width'  : 13,
        'bid_window_height'         : 3,
        'bid_window_width'          : 4,
        'game_info_window_height'   : 5,
        'game_info_window_width'    : 20,
        'score_chart_height'        : 29,
        'score_chart_width '        : 68
    }

    x_offsets = {
    }

    y_offsets = {
    }

    def __init__(self):
        # set up curses
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        curses.cur_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        self.clean_board()

        # offsets to center UI
        self.cols_offset = (curses.COLS - 181) // 2
        self.rows_offset = (curses.LINES - 58) // 2

    def __del__(self):
        # shut down curses
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def clean_board(self):
        # all windows and panels for curses
        self.windows = {
                hand_windows        : [[]   for _ in range(4)],
                hand_panels         : [[]   for _ in range(4)],
                in_play_windows     : [None for _ in range(4)],
                player_info_windows : [None for _ in range(4)],
                trump_window        : None,
                game_info_window    : None,
                score_chart_window  : None,
        }

        self.stdscr.erase()
        self.stdscr.refresh()

    def draw_board(self, boardstate, name):
        activity      = boardstate['activity']
        hand_num      = boardstate['hand_num']
        next_to_act   = boardstate['next_to_act']
        trump         = boardstate['trump_card']
        players       = boardstate['players']
        score_history = boardstate['score_history']

        self.draw_hands(players, name)
        self.draw_in_play(players, name)
        self.draw_trump(trump)
        self.draw_player_info(players, name, next_to_act, activity)
        self.draw_game_info(players, hand_num, activity)
        self.draw_score_chart(score_history)

    def draw_hands(self, players, name):
        for player in players.values():
            seat = self.id_to_seat(player['id'], players[name]['id'])
            hand_size = len(player['cards_in_hand'])

            # initialize curses windows
            self.windows.hand_windows[seat] = [
                curses.newwin(sizes['card_height'], sizes['card_width'],
                              y_offsets['hand'][seat][i] + self.rows_offset,
                              x_offsets['hand'][seat][i] + self.cols_offset)
                for i in range(hand_size)
            ]

            # initialize curses panels
            self.windows.hand_panels[seat] = [
                panel.new_panel(self.windows.hand_windows[seat][i])
                for i in range(hand_size)
            ]

            # draw each card in the hand
            for c in range(hand_size):
                card = player['cards_in_hand'][c]
                card_window = self.windows.hand_windows[seat][c]
                card_window.erase()
                if (card.visible):
                    card_window.attron(curses.color_pair(card.color()))
                card_window.addstr(card.to_ascii())
                card_window.refresh()

    def draw_in_play(self, players, name):
        for player in players.values():
            seat = self.id_to_seat(player['id'], players[name]['id'])

            # initialize curses window
            self.windows.in_play_windows[seat] = curses.newwin(
                sizes['card_height'], sizes['card_width'],
                y_offsets['in_play'][seat] + self.rows_offset,
                x_offsets['in_play'][seat] + self.cols_offset
            )

            # draw card in play
            card = player['card_in_play']
            if card:
                card_window = self.windows.in_play_windows[seat]
                card_window.erase()
                card_window.attron(curses.color_pair(card.color()))
                card_window.addstr(card.to_ascii())
                card_window.refresh()

    def draw_trump(self, trump):
        # initialize curses window
        self.windows.trump_window = curses.newwin(
            sizes['card_height'], sizes['card_width'],
            y_offsets['trump'] + self.rows_offset,
            x_offsets['trump'] + self.cols_offset
        )

        # draw trump
        trump_window = self.windows.trump_window
        trump_window.erase()
        trump_window.attron(curses.color_pair(trump.color()))
        trump_window.addstr(trump.to_ascii())
        trump_window.refresh()

    def draw_player_info(self, players, name, active_id, activity):
        for player in players.values():
            seat = self.id_to_seat(player['id'], players[name]['id'])

            # initialize curses window
            self.windows.player_info_windows[seat] = curses.newwin(
                sizes['player_info_window_height'], sizes['player_info_window_width'],
                y_offsets['player_info_window'][seat] + self.rows_offset,
                x_offsets['player_info_window'][seat] + self.cols_offset
            )

            # draw player info
            player_info_window = self.windows.player_info_windows[seat]
            player_info_window.erase()
            if player['dealer']:
                player_info_window.attron(curses.color_pair(5))
            if player['id'] == active_id:
                player_info_window.attron(curses.A_BLINK)
            player_info_window.addstr('\n ' + player['display_name'] + '\n')
            player_info_window.attroff(curses.A_BLINK)
            player_info_window.addstr(' ' + f"Score: {player['score']}" + '\n')
            if player['bid']:
                player_info_window.addstr(' ' + f"Bid: {player['bid']}" + '\n')
            if activity == 'play':
                player_info_window.addstr(' ' + f"Won: {player['tricks_taken']}")
            player_info_window.box()
            player_info_window.refresh()

    def draw_game_info(self, players, hand_num, activity):
        # initialize curses window
        self.windows.game_info_window = curses.newwin(
            sizes['game_info_window_height'], sizes['game_info_window_width'],
            y_offsets['game_info_window'] + self.rows_offset,
            x_offsets['game_info_window'] + self.cols_offset
        )

        # draw game info
        game_info_window = self.windows.game_info_window
        game_info_window.erase()
        bids = list(player['bid' for player in players.values())
        bid_total = sum(filter(None, bids))
        if actibity == 'bid':
            game_info_window.addstr('\n ' + 'HAND: {hand_num}' + '\n')
            game_info_window.addstr(' ' + f'Bids Taken: {bid_total}' + '\n'
            game_info_window.addstr(' ' + f'Bids Remaining: {hand_num - bid_total}' + '\n')
        else:
            if bid_total > hand_num:
                game_info_window.attron(curses.color_pair(2))
                game_info_window.addstr('\n ' + f'HAND: {hand_num}' + '\n')
                game_info_window.addstr('\n ' + f'OVERBID (+{bid_total - hand_num})' + '\n')
            else:
                game_info_window.attron(curses.color_pair(1))
                game_info_window.addstr('\n ' + f'HAND: {hand_num}' + '\n')
                game_info_window.addstr('\n ' + f'OVERBID ({bid_total - hand_num})' + '\n')
        game_info_window.box()
        game_info_window.refresh()

    def draw_score_chart(self, players, score_history):
        # initialize curses window
        self.windows.score_chart_window = curses.newwin(
            sizes['score_chart_height'], sizes['score_chart_width'],
            y_offsets['score_chart'] + self.rows_offset,
            x_offsets['score_chart'] + self.cols_offset
        )

        score_chart_window = self.windows.score_chart_window
        score_rows = max(score_history.keys())

        # draw score chart
        # draw lines and rows headers
        for i in range(1, score_rows):
            score_chart_window.hline(2*i, 0, curses.ACS_HLINE, sizes['score_chart_width'])
            score_chart_window.addstr(1 + 2*i, 1, f'{i}'.rjust(5))
        for i in range(1, 4):
            score_chart_window.vline(0, 7 + 15*i, curses.ACS_VLINE, 3 + 2*score_rows)
        score_chart_window.addstr(1, 1, " Hand")
        score_chart_window.box()

        # draw players' names and scores
        for player in players:
            score_chart_window.addstr(1, 8 + 15*players[player]['id'], player.center(13),
                                      curses.A_BOLD)

            for i in range(1, score_rows):
                score_chart_window.addstr(1 + 2*(i + 1), 8 + 15*players[player]'id'],
                                          f"{score_history[i][player]}".rjust(13))

        score_chart_window.refresh()

    def id_to_seat(self, target_id, relative_to_id):
        # determine the seating of a player relative to player whose screen
        # is being drawn, who is always at the bottom of the screen
        return (target_id - relative_to_id) % 4
