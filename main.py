from app import MyApp
import tkinter
from guiApp import MainWindow
import tkinter as tk

if __name__ == '__main__':

    # App = MyApp()
    # App.run()
    root = tk.Tk()
    root.tk.call('lappend', 'auto_path', './awthemes-10.1.2')

    app = MainWindow(master=root)
    app.master.title("My app")
    app.mainloop()

