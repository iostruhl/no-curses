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
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
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
                game_info_window    : curses.newwin(),
                score_chart_window  : curses.newwin()
        }

        self.stdscr.erase()
        self.stdscr.refresh()

    def draw_board(self, boardstate, name):
        self.draw_hands(boardstate['players'], name)
        self.draw_in_play(boardstate['players'], name)
        self.draw_trump(boardstate['trump_card'])
        self.draw_player_info(boardstate['players'], boardstate['next_to_act'], name)
        self.draw_game_info(boardstate['players'], boardstate['hand_num'])
        self.draw_score_chart(boardstate['score_history'])

    def draw_hands(self, players, name):
        for player in players:
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
        for player in players:
            seat = self.id_to_seat(player['id'], players[name]['id'])

            # initialize curses window
            self.windows.in_play_windows[seat] = curses.newwin(
                sizes['card_height'], sizes['card_width'],
                y_offsets['in_play'][seat] + self.rows_offset,
                x_offsets['in_play'][seat] + self.cols_offset
            )

            # draw card in play
            card = player['card_in_play']
            if (card):
                card_window = self.windows.in_play_windows[seat]
                card_window.erase()
                card_window.attron(curses.color_pair(card.color()))
                card_window.addstr(card.to_ascii())
                card_window.refresh()

    def name_to_seat(self, target_id, relative_to_id):
        # determine the seating of a player relative to player whose screen
        # is being drawn, who is always at the bottom of the screen
        return (target_id - relative_to_id) % 4
