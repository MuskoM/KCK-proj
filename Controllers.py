from views import MainMenu, NewsMenu, StatisticsMenu,Papaj,SettingsMenu
import curses
from TextTerminal import TextTerminal, TextColor


class MenuController:
    terminal = TextTerminal()
    text_color_schemes = None
    current_row = 0

    def __init__(self):
        self.text_color_schemes = TextColor(self.terminal.get_screen())
        self.terminal.initialize()

    def openPapaj(self):
        newpapaj = Papaj(self.terminal,self.text_color_schemes)
        newpapaj.print_papaj()

    def openSettingsMenu(self):
        self.terminal.clear()
        settings_menu = SettingsMenu(self.terminal,self.text_color_schemes)

        while 1:
            settings_menu.print_menu(self.current_row)

            key = self.terminal.get_key_pressed()
            self.terminal.print_string(str(self.current_row), 0, 4)

            if key == curses.KEY_UP:
                self.terminal.print_string("Key Up", 0, 0)
                self.current_row = (self.current_row - 1) % 5
            elif key == curses.KEY_DOWN:
                self.terminal.print_string("Key Down", 0, 1)
                self.current_row = (self.current_row + 1) % 5
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.terminal.print_string("Enter pressed", 0, 2)
                if self.current_row == 1:
                    pass
                elif self.current_row == 2:
                    pass
                elif self.current_row == 3:
                    break
            elif key == curses.KEY_END:
                break
            elif key == curses.KEY_F1:
                pass
            elif key == curses.KEY_F2:
                self.terminal.clear()
                main_menu = MainMenu(self.terminal,self.text_color_schemes)
                main_menu.print_menu(self.current_row)

    def openMainMenu(self):
        self.terminal.clear()
        main_menu = MainMenu(self.terminal, self.text_color_schemes)

        while 1:
            main_menu.print_menu(self.current_row)

            key = self.terminal.get_key_pressed()
            self.terminal.print_string(str(self.current_row), 0, 4)

            if key == curses.KEY_UP:
                self.terminal.print_string("Key Up", 0, 0)
                self.current_row = (self.current_row - 1) % 5
            elif key == curses.KEY_DOWN:
                self.terminal.print_string("Key Down", 0, 1)
                self.current_row = (self.current_row + 1) % 5
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.terminal.print_string("Enter pressed", 0, 2)
                if self.current_row == 1:
                    self.openStatisticsMenu()
                elif self.current_row == 3:
                    self.openSettingsMenu()
            elif key == curses.KEY_END:
                self.terminal.close()
                break
            elif key == curses.KEY_F1:
                self.terminal.clear()
                main_menu.print_menu(self.current_row)
            elif key == curses.KEY_PPAGE:
                self.terminal.get_screen().scroll(-1)
            elif key == curses.KEY_NPAGE:
                self.terminal.get_screen().scroll(1)


    def openStatisticsMenu(self):
        self.terminal.clear()
        statistics_menu = StatisticsMenu(self.terminal,self.text_color_schemes)

        while 1:
            statistics_menu.print_menu(self.current_row)

            key = self.terminal.get_key_pressed()
            self.terminal.print_string(str(self.current_row), 0, 4)
            if key == curses.KEY_UP:
                self.terminal.print_string("Key Up", 0, 0)
                self.current_row = (self.current_row - 1) % 5
            elif key == curses.KEY_DOWN:
                self.terminal.print_string("Key Down", 0, 1)
                self.current_row = (self.current_row + 1) % 5
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.terminal.print_string("Enter pressed", 0, 2)
                break

    def get_terminal(self):
        return self.terminal

    def get_text_color_schemes(self):
        return self.text_color_schemes
