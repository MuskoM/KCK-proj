import curses
from WindowInterface import WindowInterface


class TextTerminal(WindowInterface):
    """
    Concrete adapter class for the ncurses library
    Tools for creating your dream terminal using curses
    """
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

    def draw_rectangle(self):
        """Draws a rectangle on a given position"""
        try:
            self.__stdscr.border(0)
            box = curses.newwin(20,20,5,5)
            box.box()
            self.__stdscr.refresh()
            box.refresh()
        finally:
            pass

    def draw_border(self):
        """Draws a border around the terminal window"""
        try:
            self.__stdscr.border(0)
            self.__stdscr.refresh()
        finally:
            pass

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

    def print_modifier_string(self, string, x, y, option):
        """Prints a string with a modifier"""
        self.__stdscr.addstr(y, x, string, option)
        self.__stdscr.refresh()

    def justify_center(self, text, y):
        """Puts a string in the middle of the terminal"""
        h, w = self.__stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        self.print_string(text, x, y)
        return x, y

    def justify_center_with_modifier(self, text, y,option):
        """Puts a string in the middle of the terminal with a given modifier"""
        h, w = self.__stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        self.print_modifier_string(text, x, y, option)

    def get_key_pressed(self):
        key = self.__stdscr.getch()
        self.__last_key_pressed = key

        return key

    def clear(self):
        """Clears the terminal"""
        self.__stdscr.clear()

    def get_screen(self):
        return self.__stdscr

    def get_raw_input(self, r, c, prompt_string):
        """Prompts user for an input"""
        curses.echo()
        self.__stdscr.addstr(r,c,prompt_string)
        self.__stdscr.refresh()
        input = self.__stdscr.getstr(r+1,c,20)
        curses.noecho()
        return input



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
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLUE)
        self.__color_pairs['primary'] = 1
        self.__color_pairs['secondary'] = 2
        self.__color_pairs['text_magenta'] = 3
        self.__color_pairs['info'] = 4
        self.__color_pairs['error'] = 5
        self.__color_pairs['success'] = 6
        self.__color_pairs['text_field'] = 7

    def set_text_color_pair(self,color_pair='primary'):
        self.__stdscr.attron(curses.color_pair(self.__color_pairs[color_pair]))

    def clear_text_color_pair(self,color_pair='primary'):
        self.__stdscr.attroff(curses.color_pair(self.__color_pairs[color_pair]))

    def use_color_pair(self, name):
       return curses.color_pair(self.__color_pairs[name])
