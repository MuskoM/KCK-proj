from TextTerminal import TextTerminal, TextColor
import time
import curses

terminal = TextTerminal()
text_color_schemes = TextColor(terminal.get_screen())
terminal.initialize()
current_row = 0


class MainMenu:
    menu_list = ['News', 'Statistics', 'About','Exit']
    __stdscr = terminal.get_screen()

    def print_menu(self, selected_row):
        h,w = self.__stdscr.getmaxyx()

        for idx, row in enumerate(self.menu_list):
            if idx == selected_row:
                text_color_schemes.set_text_color_pair('secondary')
                terminal.justify_center(row, h//4 - len(self.menu_list) + idx)
                text_color_schemes.clear_text_color_pair('secondary')
            else:
                terminal.justify_center(row, h // 4 - len(self.menu_list) + idx)


if __name__ == '__main__':

    while 1:

        menu = MainMenu()
        menu.print_menu(current_row)

        key = terminal.get_key_pressed()

        if key == curses.KEY_UP:
            terminal.print_string("Key Up", 0, 0)
            current_row = (current_row - 1) % len(menu.menu_list)
        elif key == curses.KEY_DOWN:
            terminal.print_string("Key Down", 0, 1)
            current_row = (current_row + 1) % len(menu.menu_list)
        elif key == curses.KEY_ENTER or key in [10, 13]:
            terminal.print_string("Enter pressed", 0, 2)
        elif key == curses.KEY_END:
            terminal.close()
            break

    terminal.close()


