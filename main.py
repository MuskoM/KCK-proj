from Controllers import MenuController
import curses
from time import sleep
from CovidStatistics import CovidStatistics


def main() -> int:
    return curses.wrapper(c_main)


def c_main(stdscr)-> int:
    menuController = MenuController()
    # sleep(5)
    menuController.terminal.get_screen().clear()
    menuController.openMainMenu()
    return 0


if __name__ == '__main__':
    exit(main())