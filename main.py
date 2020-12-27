from app import MyApp
import tkinter
from guiApp import MainWindow
import tkinter as tk

if __name__ == '__main__':

    # App = MyApp()
    # App.run()
    root = tk.Tk()
    app = MainWindow(master=root)
    app.master.title("My app")
    app.master.maxsize(200,200)
    app.mainloop()

