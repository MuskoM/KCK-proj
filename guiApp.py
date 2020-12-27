from News import News
from CovidStatistics import CovidStatistics
import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.messagebox import askyesnocancel
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
from tkinter.ttk import Style


class MainWindow(tk.Frame):
    news_viewer_window = None;
    stats_window = None;
    settings_window = None;

    def __init__(self,master):
        super().__init__(master)
        self.menu = tk.Menu(self.master)
        self.styles = Style()
        self.styles.theme_use('awlight')
        self.initalize_menus()

        self.news_reader = ScrolledText()
        self.news_reader.pack()
        self.pack()

    def open_news_viewer_window(self):
        self.news_viewer_window = tk.Toplevel(self.master)
        self.news_viewer_window.title("News Viewer")
        news_reader_fragment = ScrolledText(self.news_viewer_window)
        tk.Label(self.news_viewer_window, text="Title").pack()
        article_page_progress = Progressbar(self.news_viewer_window, length=300, mode="determinate")
        article_page_progress['value'] = 50
        article_page_progress.pack()
        news_reader_fragment.insert('1.0', 'oi whats\nthe matter')
        news_reader_fragment['state'] = 'disabled'
        news_reader_fragment.pack()
        tk.Label(self.news_viewer_window, text="This is a covid Stats window").pack()


    def open_covid_stats_window(self):
        self.stats_window = tk.Toplevel(self.master)
        self.stats_window.title("Covid Stats")
        tk.Label(self.stats_window, text="This is a covid Stats window").pack()

    def open_settings_window(self):
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("Settings")
        # Color Selection
        color_group_frame = tk.Frame(self.settings_window)
        tk.Label(color_group_frame, text="This is a color group frame").pack()
        tk.Button(color_group_frame,text="Default").pack()
        color_group_frame.pack()

        # Other Settings Selection
        other_settings_frame = tk.Frame(self.settings_window, pady=15)
        tk.Label(other_settings_frame, text="This is a label for other settings frame").pack()

        other_settings_frame.pack()


    def initalize_menus(self):
        self.master.config(menu=self.menu)

        file_menu = tk.Menu(self.menu)
        edit_menu = tk.Menu(self.menu)
        modules_menu = tk.Menu(self.menu)

        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New")
        file_menu.add_command(label="Save")
        self.menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_separator()
        edit_menu.add_command(label="Settings",command=self.open_settings_window)
        self.menu.add_cascade(label="Modules", menu=modules_menu)
        modules_menu.add_command(label="News Reader", command=self.open_news_viewer_window)
        modules_menu.add_command(label="Covid Statistics", command=self.open_covid_stats_window)


    def print_contents(self,event):
        if self.contents.get() == "AskQuestion":
            print("Hi, the current contents is: " + self.contents.get())
        else:
            answer = askyesnocancel("Asking", "Yes no dialog")
            print(answer)
