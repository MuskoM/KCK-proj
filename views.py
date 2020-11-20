from curses.textpad import rectangle, Textbox
from CovidStatistics import CovidStatistics


class Menu:
    stdscr = None
    text_color_schemes = None

    def __init__(self, stdscr, text_color_schemes):
        self.stdscr = stdscr
        self.text_color_schemes = text_color_schemes


class MainMenu(Menu):

    menu_list = None

    def __init__(self, stdscr, text_color_schemes):
        super().__init__(stdscr,text_color_schemes)
        self.menu_list = ['News', 'Statistics', 'About', 'Exit']

    def print_menu(self, selected_row):
        h,w = self.stdscr.get_screen().getmaxyx()
        for idx, row in enumerate(self.menu_list):
            if idx == selected_row:
                self.text_color_schemes.set_text_color_pair('secondary')
                self.stdscr.justify_center(row, h // 4 - len(self.menu_list) + idx)
                self.text_color_schemes.clear_text_color_pair('secondary')
            else:
                self.stdscr.justify_center(row, h // 4 - len(self.menu_list) + idx)

        self.stdscr.print_string("F1 - Menu | END - Exit", w - len("F1 - Menu | END - Exit") -1, h-1)


class NewsMenu:

    def print_menu(self):
        self.__stdscr.clear()
        self.__stdscr.justify_center("This is a news menu", 3)


class AboutMenu:

    def print_menu(self):
        self.__stdscr.clear()
        self.__stdscr.justify_center("This is an about menu", 3)


class StatisticsMenu(Menu):

    poland_statistics = {}

    def __init__(self, stdsrc, text_color_schemes):
        super().__init__(stdsrc, text_color_schemes)
        covid_stats = CovidStatistics()
        covid_stats.get_response()
        self.poland_statistics = covid_stats.get_statistics()
        print(self.poland_statistics)

    def print_menu(self):
        self.stdscr.clear()
        self.stdscr.justify_center(f"{self.poland_statistics['country']}", 3)
        self.stdscr.justify_center(f"{self.poland_statistics['new_cases']}", 4)