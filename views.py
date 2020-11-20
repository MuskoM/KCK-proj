class MainMenu:

    menu_list = None

    def __init__(self):
        self.menu_list = ['News', 'Statistics', 'About', 'Exit']

    def print_menu(self, selected_row, __stdscr, text_color_schemes):
        h,w = __stdscr.get_screen().getmaxyx()

        for idx, row in enumerate(self.menu_list):
            if idx == selected_row:
                text_color_schemes.set_text_color_pair('secondary')
                __stdscr.justify_center(row, h // 4 - len(self.menu_list) + idx)
                text_color_schemes.clear_text_color_pair('secondary')
            else:
                __stdscr.justify_center(row, h // 4 - len(self.menu_list) + idx)


class NewsMenu:

    def print_menu(self):
        self.__stdscr.clear()
        self.__stdscr.justify_center("This is a news menu", 3)


class AboutMenu:

    def print_menu(self):
        self.__stdscr.clear()
        self.__stdscr.justify_center("This is an about menu", 3)


class StatisticsMenu:

    def print_menu(self):
        self.__stdscr.clear()
        self.__stdscr.justify_center("This is a statistics menu", 3)