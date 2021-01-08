from app import MyApp
import tkinter
from guiApp import MainWindow
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

if __name__ == '__main__':

    # App = MyApp()
    # App.run()
    root = ThemedTk(theme="clam")

    app = MainWindow(master=root)
    app.master.title("My app")
    app.mainloop()

