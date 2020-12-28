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
        self.grid()

        self.news_reader = ScrolledText()
        self.news_reader.grid(sticky="NSWE")
        self.news_reader.insert('1.0',"sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss")
        self.master.columnconfigure(self.news_reader, weight=1)
        self.master.rowconfigure(self.news_reader, weight=1)


    def open_news_viewer_window(self):
        self.news_viewer_window = tk.Toplevel(self.master)
        self.news_viewer_window.title("News Viewer")

        news_reader_fragment = ScrolledText(self.news_viewer_window)
        titile_label = tk.Label(self.news_viewer_window, text="Title").grid(sticky="NSWE")
        article_page_progress = Progressbar(self.news_viewer_window,
                                            mode="determinate")
        article_page_progress['value'] = 50

        article_page_progress.grid(sticky="NSWE")
        news_reader_fragment.insert('1.0', 'oi whats\nthe matter')
        news_reader_fragment['state'] = 'disabled'
        news_reader_fragment.grid(sticky="NSWE")

        article_buttons_frame = tk.Frame(self.news_viewer_window)
        article_buttons_frame.grid()
        previous_article_btn = tk.Button(article_buttons_frame,
                                         text="Previous article").grid(row=0,column=0)
        next_article_btn = tk.Button(article_buttons_frame,
                                     text="Next article").grid(row=0,column=1)
        self.news_viewer_window.columnconfigure(news_reader_fragment, weight=1)
        self.news_viewer_window.rowconfigure(news_reader_fragment, weight=1)


    def open_covid_stats_window(self):
        self.stats_window = tk.Toplevel(self.master, width=200, height=200)
        self.stats_window.maxsize(200,200)
        self.stats_window.title("Covid Stats")
        statistics_fragment = tk.Frame(self.stats_window)
        statistics_fragment.grid(sticky="NSWE")


        population_label = tk.Label(statistics_fragment, text="Population")
        population_label.grid(sticky="NSWE", column=0, row=1)
        population_stat = tk.Label(statistics_fragment, text="00000000")
        population_stat.grid( column=1, row=1)
        new_cases_label = tk.Label(statistics_fragment, text="New Cases")
        new_cases_label.grid(sticky="NSWE", column=0, row=2)
        new_cases_stat = tk.Label(statistics_fragment, text="00000000")
        new_cases_stat.grid(sticky="NSW", column=1, row=2)
        active_cases_label = tk.Label(statistics_fragment, text="Active Cases")
        active_cases_label.grid(sticky="NSWE", column=0, row=3)
        active_cases_stat = tk.Label(statistics_fragment, text="00000000")
        active_cases_stat.grid(sticky="NSW", column=1,row=3)
        per_million_label = tk.Label(statistics_fragment, text="Per million")
        per_million_label.grid(sticky="NSWE", column=0, row=4)
        per_million_stat = tk.Label(statistics_fragment, text="00000000")
        per_million_stat.grid(sticky="NSW", column=1, row=4)

        # TODO: Create a popup input window
        input_country = tk.Button(self.stats_window,text="Input country name")
        input_country.grid()

        self.stats_window.columnconfigure(statistics_fragment, weight=1)
        self.stats_window.rowconfigure(statistics_fragment, weight=1)
        statistics_fragment.columnconfigure(population_label, weight=1)
        statistics_fragment.columnconfigure(population_label, weight=1)

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

        self.menu.add_cascade(label="Modules", menu=modules_menu)
        modules_menu.add_command(label="News Reader", command=self.open_news_viewer_window)
        modules_menu.add_command(label="Covid Statistics", command=self.open_covid_stats_window)
        modules_menu.add_separator()
        modules_menu.add_command(label="Settings", command=self.open_settings_window)
        self.menu.add_cascade(label="Get", menu=file_menu)
        file_menu.add_command(label="TVN24 Articles")
        file_menu.add_command(label="GOV Articles")
        self.menu.add_cascade(label="Download", menu=edit_menu)
        edit_menu.add_command(label="TVN24 Articles")
        edit_menu.add_command(label="GOV Articles")



