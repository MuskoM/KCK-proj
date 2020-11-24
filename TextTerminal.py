import curses
from WindowInterface import WindowInterface


class TextTerminal(WindowInterface):
    """Tools for creating your dream terminal using curses"""
    __terminal_settings = None
    __stdscr = None
    __last_key_pressed = None

    def __init__(self):
        self.__stdscr = curses.initscr()

    def initialize(self):
        """Initializes the window without a cursor, typing callbacks and confirmations"""
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.__stdscr.keypad(True)

    def close(self):
        """Closes the window and resets terminal settings"""
        curses.nocbreak()
        curses.curs_set(1)
        self.__stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def print_string(self, string, x, y):
        """Prints a string and refreshes the terminal"""
        self.__stdscr.addstr(y, x, string)
        self.__stdscr.refresh()

    def justify_center(self, text, y):
        """Puts a string in the middle of the terminal"""
        h, w = self.__stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        self.print_string(text, x, y)

    def get_key_pressed(self):
        key = self.__stdscr.getch()
        self.__last_key_pressed = key

        return key

    def clear(self):
        self.__stdscr.clear()

    def get_screen(self):
        return self.__stdscr


class TextColor:
    """
    Class contains a color pallets for a terminal

    ...

    Attributes
    ----------
    __color_pairs : dict
        a dictionary containing curses pairs of colors
    __stdscr : CursesWindow
        window where colors are changed

    Methods
    -------
    change_text_color_pair(color_pair='primary')
        changes the current color pair for printing text
    """
    __color_pairs = {}
    __stdscr = None

    def __init__(self,screen):
        self.__stdscr = screen
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.__color_pairs['primary'] = 1
        self.__color_pairs['secondary'] = 2

    def set_text_color_pair(self,color_pair='primary'):
        self.__stdscr.attron(curses.color_pair(self.__color_pairs[color_pair]))

    def clear_text_color_pair(self,color_pair='primary'):
        self.__stdscr.attroff(curses.color_pair(self.__color_pairs[color_pair]))
