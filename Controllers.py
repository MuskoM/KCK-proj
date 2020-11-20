from views import MainMenu, NewsMenu
import curses
from TextTerminal import TextTerminal, TextColor


class MenuController:
    terminal = TextTerminal()
    text_color_schemes = None
    current_row = 0

    def __init__(self):
        self.text_color_schemes = TextColor(self.terminal.get_screen())
        self.terminal.initialize()

    def openView(self, current_row_id):
        return {
            0: lambda x : self.terminal.print_string("YOLO",0,6),
        }[current_row_id]

    def openMainMenu(self):
        main_menu = MainMenu()

        while 1:
            main_menu.print_menu(self.current_row, self.terminal, self.text_color_schemes)

            key = self.terminal.get_key_pressed()
            self.terminal.print_string(str(self.current_row), 0, 5)
            if key == curses.KEY_UP:
                self.terminal.print_string("Key Up", 0, 0)
                self.current_row = (self.current_row - 1) % 4
            elif key == curses.KEY_DOWN:
                self.terminal.print_string("Key Down", 0, 1)
                self.current_row = (self.current_row + 1) % 4
            elif key == curses.KEY_ENTER or key in [10, 13]:
                self.terminal.print_string("Enter pressed", 0, 2)
                MenuController.openView(self.current_row, self.current_row)
            elif key == curses.KEY_END:
                self.terminal.close()
                break

        self.terminal.close()

        return MainMenu.print_menu(self.current_row)

    def get_terminal(self):
        return self.terminal

    def get_text_color_schemes(self):
        return self.text_color_schemes
