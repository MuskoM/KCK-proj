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
        self.menu_list = ['News', 'Statistics', 'About','Settings', 'Exit']
        self.title_banner = open('templates/program_name.txt')

    def print_banner(self,file):
        self.title_banner = open('templates/' + file)
        for index, line in enumerate(self.title_banner):
            self.text_color_schemes.set_text_color_pair('text_magenta')
            self.stdscr.justify_center(line, index +2)
            self.text_color_schemes.clear_text_color_pair('text_magenta')

    def print_menu(self, selected_row):
        h,w = self.stdscr.get_screen().getmaxyx()

        for index, line in enumerate(self.title_banner):
            self.text_color_schemes.set_text_color_pair('secondary')
            self.stdscr.justify_center(line, index +2)
            self.text_color_schemes.clear_text_color_pair('secondary')

        for idx, row in enumerate(self.menu_list):
            if idx == selected_row:
                self.text_color_schemes.set_text_color_pair('secondary')
                self.stdscr.justify_center(row, h // 4 - len(self.menu_list) + idx)
                self.text_color_schemes.clear_text_color_pair('secondary')
            else:
                self.stdscr.justify_center(row, h // 4 - len(self.menu_list) + idx)

        self.stdscr.print_string("F1 - Menu | END - Exit", w - len("F1 - Menu | END - Exit") -1, h-1)


class SettingsMenu(MainMenu):

    def __init__(self, stdscr, text_color_schemes):
        super().__init__(stdscr, text_color_schemes)
        self.menu_list = ['Color Scheme', 'Settins 1', 'Settings 2', 'Return', 'Exit']


class NewsMenu:

    def print_menu(self):
        self.__stdscr.clear()
        self.__stdscr.justify_center("This is a news menu", 3)


class AboutMenu:

    def print_menu(self):
        self.__stdscr.clear()
        self.__stdscr.justify_center("This is an about menu", 3)


class Papaj(Menu):

    file = None

    def __init__(self, stdsrc, text_color_schemes):
        super().__init__(stdsrc, text_color_schemes)
        self.file = open('templates/program_name.txt')

    def print_papaj(self):
        for index, line in enumerate(self.file):
            self.stdscr.justify_center(line, index)


class StatisticsMenu(MainMenu):

    covid_stats = None

    def __init__(self, stdsrc, text_color_schemes):
        super().__init__(stdsrc, text_color_schemes)
        self.covid_stats = CovidStatistics()

    def print_menu(self,selected_row):
        pass

    def print_country_data(self, y, country_name):
        country_name = str(country_name)[2:-1:]
        stats = self.covid_stats.get_country_stats(country_name)
        if stats is None:
            self.text_color_schemes.set_text_color_pair('error')
            self.stdscr.justify_center(f"Country not found", y)
            self.text_color_schemes.set_text_color_pair('primary')
        else:
            self.text_color_schemes.set_text_color_pair('text_cyan')
            self.stdscr.justify_center(f"Country: {stats['country']}", y + 1)
            self.stdscr.justify_center(f"Population: {stats['population']}", y + 2)
            self.stdscr.justify_center(f"New Cases: {stats['cases']['new']}", y + 3)
            self.stdscr.justify_center(f"Active Cases: {stats['cases']['active']}", y + 4)
            self.stdscr.justify_center(f"Cases per 1 million people: {stats['cases']['1M_pop']}", y + 5)
            self.text_color_schemes.clear_text_color_pair('primary')


