import os

import tkinter as tk
from tkinter.colorchooser import askcolor
from tkinter.messagebox import askyesnocancel, askyesno
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from News import News
from app import MyApp


class MainWindow(tk.Frame):
    news_viewer_window = None;
    stats_window = None;
    settings_window = None;

    # Initialize the main window and utilities
    def __init__(self, master):
        super().__init__(master)
        # Module containing scraping utilities
        self.articles = []
        self.titles = []
        self.page_no = 0
        self.news_module = News()
        self.terminalUi = MyApp()


        self.menu = tk.Menu(self.master)

        # Setting style of app
        self.styles = Style()
        self.styles.theme_use('awlight')

        self.initalize_menus()
        self.grid()

        # Main window
        self.news_reader = ScrolledText()
        self.news_reader.grid(sticky="NSWE")
        first_article = open("sites/articles/article0.txt")
        self.news_reader.insert('1.0', first_article.read())
        first_article.close()
        self.master.columnconfigure(self.news_reader, weight=1)
        self.master.rowconfigure(self.news_reader, weight=1)

    # Opens a window with news reader
    def open_news_viewer_window(self):
        self.news_viewer_window = tk.Toplevel(self.master)
        self.news_viewer_window.title("News Viewer")

        # Article label
        self.news_title_label = tk.Label(self.news_viewer_window, text="sss").grid(sticky="NSWE")

        # Container for the article
        self.news_reader_fragment = ScrolledText(self.news_viewer_window)

        self.news_reader_fragment.insert('1.0', 'oi whats\nthe matter')
        self.news_reader_fragment['state'] = 'disabled'
        self.news_reader_fragment.grid(sticky="NSWE")

        # Article number indicator
        self.news_article_page_progress = Progressbar(self.news_viewer_window,
                                                      mode="determinate")
        self.news_article_page_progress['value'] = 0;
        self.news_article_page_progress.grid(sticky="NSWE")

        # Buttons for prev and next article
        article_buttons_frame = tk.Frame(self.news_viewer_window)
        article_buttons_frame.grid()
        previous_article_btn = tk.Button(article_buttons_frame,
                                         command=self.get_previous_article,
                                         text="Previous article").grid(row=0, column=0)
        next_article_btn = tk.Button(article_buttons_frame,
                                     text="Next article",
                                     command=self.get_next_article).grid(row=0, column=1)

        # Layout config
        self.news_viewer_window.columnconfigure(self.news_reader_fragment, weight=1)
        self.news_viewer_window.rowconfigure(self.news_reader_fragment, weight=1)

    def open_covid_stats_window(self):
        self.stats_window = tk.Toplevel(self.master, width=200, height=200)
        self.stats_window.maxsize(200, 200)
        self.stats_window.title("Covid Stats")

        statistics_fragment = tk.Frame(self.stats_window)
        statistics_fragment.grid(sticky="NSWE")

        population_label = tk.Label(statistics_fragment, text="Population")
        population_label.grid(sticky="NSWE", column=0, row=1)

        population_stat = tk.Label(statistics_fragment, text="00000000")
        population_stat.grid(column=1, row=1)

        new_cases_label = tk.Label(statistics_fragment, text="New Cases")
        new_cases_label.grid(sticky="NSWE", column=0, row=2)

        new_cases_stat = tk.Label(statistics_fragment, text="00000000")
        new_cases_stat.grid(sticky="NSW", column=1, row=2)

        active_cases_label = tk.Label(statistics_fragment, text="Active Cases")
        active_cases_label.grid(sticky="NSWE", column=0, row=3)

        active_cases_stat = tk.Label(statistics_fragment, text="00000000")
        active_cases_stat.grid(sticky="NSW", column=1, row=3)

        per_million_label = tk.Label(statistics_fragment, text="Per million")
        per_million_label.grid(sticky="NSWE", column=0, row=4)

        per_million_stat = tk.Label(statistics_fragment, text="00000000")
        per_million_stat.grid(sticky="NSW", column=1, row=4)

        # TODO: Create a popup input window
        input_country = tk.Button(self.stats_window, text="Input country name")
        input_country.grid()
        # Layout Config
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
        tk.Button(color_group_frame, text="Default").pack()
        color_group_frame.pack()

        # Other Settings Selection
        other_settings_frame = tk.Frame(self.settings_window, pady=15)
        tk.Label(other_settings_frame, text="This is a label for other settings frame").pack()

        other_settings_frame.pack()

    def initalize_menus(self):
        self.master.config(menu=self.menu)

        # Topbar menus
        file_menu = tk.Menu(self.menu)
        edit_menu = tk.Menu(self.menu)
        modules_menu = tk.Menu(self.menu)

        # Modules Menu
        self.menu.add_cascade(label="Modules", menu=modules_menu)
        modules_menu.add_command(label="News Reader", command=self.open_news_viewer_window)
        modules_menu.add_command(label="Covid Statistics", command=self.open_covid_stats_window)
        modules_menu.add_separator()
        modules_menu.add_command(label="Settings", command=self.open_settings_window)

        # Menu for loading the articles
        self.menu.add_cascade(label="Get", menu=file_menu)
        file_menu.add_command(label="TVN24 Articles", command=self.get_who_articles)
        file_menu.add_command(label="GOV Articles", command=self.get_gov_articles)

        # Menu for downloading the articles
        self.menu.add_cascade(label="Download", menu=edit_menu)
        edit_menu.add_command(label="TVN24 Articles", command=self.news_module.get_who_articles)
        edit_menu.add_command(label="GOV Articles", command=self.news_module.get_gov_articles)

    # HERE ARE NEWS READER FUNCTIONS

    def get_previous_article(self):
        try:
            self.page_no -= 1
            self.news_article_page_progress["value"] = self.page_no
            self.news_reader_fragment["state"] = "normal"
            self.news_reader_fragment.delete("1.0", "end")
            self.news_reader_fragment.insert("1.0", self.articles[self.page_no])
            self.news_reader_fragment["state"] = "disabled"
            self.news_title_label["text"] = self.news_article_page_progress["value"]
        except IndexError:
            self.page_no += 1

    def get_next_article(self):
        try:
            self.page_no += 1
            self.news_article_page_progress["value"] = self.page_no
            self.news_reader_fragment["state"] = "normal"
            self.news_reader_fragment.delete("1.0", "end")
            self.news_reader_fragment.insert("1.0", self.articles[self.page_no])
            self.news_reader_fragment["state"] = "disabled"
            self.news_title_label["value"] = self.news_article_page_progress["value"]
        except IndexError:
            self.page_no -= 1

    def get_who_articles(self):
        download = askyesno('Confirm?', "Do you want to view health articles")
        print(download)
        if download:
            self.articles.clear()
            self.titles.clear()
            self.news_article_page_progress["value"] = 0
            for file in os.listdir('sites/articles'):
                article_file = open('sites/articles/' + file, encoding='utf-8')
                self.titles.append(article_file.readline())
                self.articles.append(article_file.read())
            self.news_reader_fragment["state"] = "normal"
            self.news_reader_fragment.delete("1.0", "end")
            self.news_reader_fragment.insert("1.0", self.articles[0])
            self.news_reader_fragment["state"] = "disabled"
            self.news_title_label["text"] = self.titles[0]
            self.news_article_page_progress["maximum"] = len(self.articles)

    def get_gov_articles(self):
        download = askyesno('Confirm?', "Do you want to view government articles")
        if download:
            self.articles.clear()
            self.titles.clear()
            self.news_article_page_progress["value"] = 0
            for file in os.listdir('sites/gov_articles'):
                article_file = open('sites/gov_articles/' + file, encoding='utf-8')
                self.titles.append(article_file.readline())
                self.articles.append(article_file.readlines())
            self.news_reader_fragment["state"] = "normal"
            self.news_reader_fragment.delete("1.0", "end")
            self.news_reader_fragment.insert("1.0", self.articles[0])
            self.news_reader_fragment["state"] = "disabled"
            self.news_title_label["text"] = self.titles[0]
            self.news_article_page_progress["maximum"] = len(self.articles)
