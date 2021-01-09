from app import MyApp
import tkinter
from guiApp import MainWindow
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

if __name__ == '__main__':

    # App = MyApp()
    # App.run()
    root = tk.Tk()

    app = MainWindow(master=root)
    root.config(bg="#666666")
    app.master.title("My app")
    app.mainloop()

