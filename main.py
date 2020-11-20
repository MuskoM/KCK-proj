from Controllers import MenuController
import curses

terminal = MenuController.terminal
current_row = 0


if __name__ == '__main__':
    menuController = MenuController()

    menuController.openMainMenu()



