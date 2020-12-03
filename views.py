from curses.textpad import rectangle, Textbox
from CovidStatistics import CovidStatistics
import curses
import textwrap


class Menu:
    """
    Base class for all the menu views

    """
    stdscr = None
    text_color_schemes = None

    def __init__(self, stdscr, text_color_schemes):
        self.stdscr = stdscr
        self.text_color_schemes = text_color_schemes
        self.stdscr.draw_border()


class MainMenu(Menu):
    """
        Main menu view
    """

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

        self.stdscr.draw_rectangle()

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


class NewsMenu(Menu):
    """
    News menu view
    """

    def __init__(self, stdscr, text_color_schemes):
        super().__init__(stdscr, text_color_schemes)
        self.title_banner = open('templates/News_banner.txt')
        self.files = ['text1.txt', 'text2.txt']

    def print_banner(self, file):
        self.title_banner = open('templates/' + file)
        for index, line in enumerate(self.title_banner):
            self.text_color_schemes.set_text_color_pair('text_magenta')
            self.stdscr.justify_center(line, index + 2)
            self.text_color_schemes.clear_text_color_pair('text_magenta')

    def print_menu(self):
        h,w = self.stdscr.get_screen().getmaxyx()
        file_no = 0
        mypad = curses.newpad(h-10, w-10)
        mypad.bkgd(' ', self.text_color_schemes.use_color_pair('secondary'))
        mypad_pos = 0
        mypad.refresh(mypad_pos,0,h//10,w//7,h- h//10,w-w//7)

        hbox, wbox = self.stdscr.get_screen().getmaxyx()

        while 1:
            file = open("sources/" + self.files[file_no])

            for index, line in enumerate(file):
                mypad.addstr(index, wbox - wbox + 1,
                             textwrap.indent(textwrap.fill(textwrap.dedent(line), wbox - wbox // 2), '  '))
                mypad.refresh(mypad_pos, 0, hbox // 10, wbox // 7, hbox - hbox // 10, wbox - wbox // 7)

            self.stdscr.print_string("Press END to stop reading", w // 7, h - h // 10 + 2)
            file.close()
            key = self.stdscr.get_key_pressed()

            if key == curses.KEY_UP:
                mypad_pos += 1
                mypad.refresh(mypad_pos,0,h//10,w//7,h- h//10,w-w//7)
            elif key == curses.KEY_DOWN:
                mypad_pos -= 1
                mypad.refresh(mypad_pos, 0, h//10, w//7, h-h//10, w-w//7)
            elif key == curses.KEY_LEFT:
                mypad.clear()
                file_no -= 1
                mypad.refresh(mypad_pos, 0, hbox // 10, wbox // 7, hbox - hbox // 10, wbox - wbox // 7)
            elif key == curses.KEY_RIGHT:
                mypad.clear()
                file_no += 1
                mypad.refresh(mypad_pos, 0, hbox // 10, wbox // 7, hbox - hbox // 10, wbox - wbox // 7)
            elif key == curses.KEY_END:
                self.stdscr.print_string( "Press END again to go back", w//7, h-h//10 +2)
                break


class StatisticsMenu(MainMenu):

    messages = {
        "input_message": "Input country name"
    }

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
            self.text_color_schemes.clear_text_color_pair('error')
            self.text_color_schemes.set_text_color_pair('info')
            self.stdscr.justify_center_with_modifier(f"Press Enter to continue...", y + 2, curses.A_UNDERLINE)
            self.text_color_schemes.clear_text_color_pair('info')
        else:
            self.text_color_schemes.set_text_color_pair('info')
            self.stdscr.justify_center(f"Country: {stats['country']}", y + 1)
            self.stdscr.justify_center(f"Population: {stats['population']}", y + 2)
            self.stdscr.justify_center(f"New Cases: {stats['cases']['new']}", y + 3)
            self.stdscr.justify_center(f"Active Cases: {stats['cases']['active']}", y + 4)
            self.stdscr.justify_center(f"Cases per 1 million people: {stats['cases']['1M_pop']}", y + 5)
            self.text_color_schemes.clear_text_color_pair('info')
            self.stdscr.justify_center_with_modifier(f"Press Enter to continue...", y + 7, curses.A_UNDERLINE)


class SettingsMenu(MainMenu):
    """
    Settings menu view
    """

    def __init__(self, stdscr, text_color_schemes):
        super().__init__(stdscr, text_color_schemes)
        self.menu_list = ['Color Scheme', 'Settins 1', 'Settings 2', 'Return']


class AboutMenu:

    def print_menu(self):
        self.__stdscr.clear()
        self.__stdscr.justify_center("This is an about menu", 3)


class Papaj(Menu):

    file = None

    def __init__(self, stdsrc, text_color_schemes):
        super().__init__(stdsrc, text_color_schemes)
        self.file = open('templates/papaj.txt')

    def print_papaj(self):
        for index, line in enumerate(self.file):
            self.stdscr.justify_center(line, index)

