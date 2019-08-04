import curses
from curses import panel

class GraphicsBoard:
    spacings = {
        padding                   : 1,
        vertical_spacing          : 1,
        horizontal_spacing        : 5,
        card_height               : 11,
        card_width                : 13,
        player_info_window_height : 6,
        player_info_window_width  : 13,
        bid_window_height         : 3,
        bid_window_width          : 4,
        game_info_window_height   : 5,
        game_info_window_width    : 20,
        score_chart_height        : 29,
        score_chart_width         : 68
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
        self.rows_offset = curses.LINES - 58) // 2

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
                play_windows        : [None for _ in range(4)],
                player_info_windows : [None for _ in range(4)],
                trump_window        : None,
                game_info_window    : curses.newwin(),
                score_chart_window  : curses.newwin()
        }

        self.stdscr.erase()
        self.stdscr.refresh()

    def draw_board(self, boardstate):
        self.draw_hands()
        self.draw_player_info()
        self.draw_trump()
        self.draw_game_info()
        self.draw_score_chart()
