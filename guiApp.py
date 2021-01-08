import os

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesnocancel, askyesno
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
from tkinter.ttk import Style
from News import News
from CovidStatistics import CovidStatistics
from app import MyApp


class MainWindow(tk.Frame):
    news_viewer_window = None;
    stats_window = None;
    settings_window = None;

    # Initialize the main window and utilities
    def __init__(self, master):
        super().__init__(master)

        # Module containing scraping utilities
        self.news_module = News()

        self.menu = tk.Menu(self.master)

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

    def initalize_menus(self):
        self.master.config(menu=self.menu)

        modules_menu = tk.Menu(self.menu)

        # Modules Menu
        self.menu.add_cascade(label="Modules", menu=modules_menu)
        modules_menu.add_command(label="News Reader", command=self.open_news_viewer_window)
        modules_menu.add_command(label="Covid Statistics", command=self.open_covid_stats_window)
        modules_menu.add_separator()
        modules_menu.add_command(label="Settings", command=self.open_covid_settings_window)


    def open_covid_stats_window(self):
        self.covid_stats_window = CovidStatsWindow(self)

    def open_covid_settings_window(self):
        self.covid_settings_window = SettingsWindow(self)

    # Opens a window with news reader
    def open_news_viewer_window(self):
        self.news_viewer_window = NewsWindow(self)


class NewsWindow:
    def __init__(self, master):
        self.articles = []
        self.titles = []
        self.page_no = 0
        self.news_module = News()
        self.master = master
        self.news_viewer_window = tk.Toplevel(self.master)
        self.news_viewer_window.title("News Viewer")

        # Article label
        self.news_title_label = ttk.Label(self.news_viewer_window, text="sss")
        self.news_title_label.grid(sticky="NSWE")

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

        buttons_grid_frame = ttk.Frame(self.news_viewer_window)
        buttons_grid_frame.grid(row=1,column=1)

        # Buttons for prev and next article
        article_buttons_frame = ttk.Frame(buttons_grid_frame, relief="flat")
        article_buttons_frame.grid(row=0)
        previous_article_button = ttk.Button(article_buttons_frame,
                                         command=self.get_previous_article,
                                         text="Previous article").grid(row=0, column=0)
        next_article_button = ttk.Button(article_buttons_frame,
                                     text="Next article",
                                     command=self.get_next_article).grid(row=0, column=1)

        # Frame for get_article_type buttons
        get_article_buttons_label = ttk.Label(buttons_grid_frame, text="LOAD", justify="left")
        get_article_buttons_label.grid(row=1)
        get_article_buttons_frame = ttk.Frame(buttons_grid_frame, relief="flat",)
        get_article_buttons_frame.grid(row=2)
        get_gov_articles_button = ttk.Button(get_article_buttons_frame,
                                     command=self.get_gov_articles,
                                     text="GOV articles",
                                     ).grid(row=0, column=0)
        get_health_articles_button = ttk.Button(get_article_buttons_frame,
                                        text="WHO articles",
                                        command=self.get_who_articles).grid(row=0, column=1)

        # Frame for download_article_type buttons
        get_article_buttons_label = ttk.Label(buttons_grid_frame, text="DOWNLOAD")
        get_article_buttons_label.grid(row=3)
        download_article_buttons_frame = ttk.Frame(buttons_grid_frame, relief="raised")
        download_article_buttons_frame.grid(row=4)

        download_gov_articles_button = ttk.Button(download_article_buttons_frame,
                                     command=self.download_gov_articles,
                                     text="GOV articles").grid(row=0, column=0)
        download_health_articles_button = ttk.Button(download_article_buttons_frame,
                                        text="WHO articles",
                                        command=self.download_who_articles).grid(row=0, column=1)

        # Layout config
        self.news_viewer_window.columnconfigure(self.news_reader_fragment, weight=1)
        self.news_viewer_window.rowconfigure(self.news_reader_fragment, weight=1)

        # HERE ARE NEWS READER FUNCTIONS

    def download_gov_articles(self):
        download = askyesno("Download?", "Do you want to download GOV articles?, This might take a while.",
                            parent=self.news_viewer_window)
        if download:
            self.news_module.get_gov_articles()

    def download_who_articles(self):
        download = askyesno("Download?", "Do you want to download WHO articles?, This might take a while.",
                            parent=self.news_viewer_window)
        if download:
            self.news_module.get_who_articles()

    def get_previous_article(self):
        try:
            self.page_no -= 1
            self.news_article_page_progress["value"] = self.page_no
            self.news_reader_fragment["state"] = "normal"
            self.news_reader_fragment.delete("1.0", "end")
            self.news_reader_fragment.insert("1.0", self.articles[self.page_no])
            self.news_reader_fragment["state"] = "disabled"
            self.news_title_label["text"] = self.titles[self.news_article_page_progress["value"]]
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
            self.news_title_label["text"] = self.titles[self.news_article_page_progress["value"]]
        except IndexError:
            self.page_no -= 1


    def get_who_articles(self):
        download = askyesno('Confirm?', "Do you want to view health articles", parent=self.news_viewer_window)
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
        download = askyesno('Confirm?', "Do you want to view government articles", parent=self.news_viewer_window)
        if download:
            self.articles.clear()
            self.titles.clear()
            self.news_article_page_progress["value"] = 0
            for file in os.listdir('sites/gov_articles'):
                article_file = open('sites/gov_articles/' + file, encoding='utf-8')
                self.titles.append(article_file.readline())
                self.articles.append(article_file.read())
            self.news_reader_fragment["state"] = "normal"
            self.news_reader_fragment.delete("1.0", "end")
            self.news_reader_fragment.insert("1.0", self.articles[0])
            self.news_reader_fragment["state"] = "disabled"
            self.news_title_label["text"] = self.titles[0]
            self.news_article_page_progress["maximum"] = len(self.articles)

class SettingsWindow:

    def __init__(self, master):
        self.master = master
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("Settings")

        # Color Selection
        color_group_frame = ttk.Frame(self.settings_window)
        ttk.Label(color_group_frame, text="This is a color group frame").pack()
        ttk.Button(color_group_frame, text="Default").pack()
        color_group_frame.pack()

        # Other Settings Selection
        other_settings_frame = ttk.Frame(self.settings_window)
        ttk.Label(other_settings_frame, text="This is a label for other settings frame").pack()

        other_settings_frame.pack()


class CovidStatsWindow:
    def __init__(self,master):
        self.master = master
        self.COVID_MODULE = CovidStatistics()
        self.COUNTRY_NAME = "Poland"
        self.stats_window = tk.Toplevel(self.master, width=200, height=200)
        self.stats_window.maxsize(200, 200)
        self.stats_window.title("Covid Stats")

        statistics_fragment = ttk.Frame(self.stats_window)
        statistics_fragment.grid(sticky="NSWE")

        self.country_label = ttk.Label(statistics_fragment, text=self.COUNTRY_NAME)
        self.country_label.grid(sticky="NSWE", column=0, row=0)

        population_label = ttk.Label(statistics_fragment, text="Population")
        population_label.grid(sticky="NSWE", column=0, row=1)

        self.population_stat = ttk.Label(statistics_fragment, text="00000000")
        self.population_stat.grid(column=1, row=1)

        new_cases_label = ttk.Label(statistics_fragment, text="New Cases")
        new_cases_label.grid(sticky="NSWE", column=0, row=2)

        self.new_cases_stat = ttk.Label(statistics_fragment, text="00000000")
        self.new_cases_stat.grid(sticky="NSW", column=1, row=2)

        active_cases_label = ttk.Label(statistics_fragment, text="Active Cases")
        active_cases_label.grid(sticky="NSWE", column=0, row=3)

        self.active_cases_stat = ttk.Label(statistics_fragment, text="00000000")
        self.active_cases_stat.grid(sticky="NSW", column=1, row=3)

        per_million_label = ttk.Label(statistics_fragment, text="Per million")
        per_million_label.grid(sticky="NSWE", column=0, row=4)

        self.per_million_stat = ttk.Label(statistics_fragment, text="00000000")
        self.per_million_stat.grid(sticky="NSW", column=1, row=4)

        self.get_stats()

        self.input_country = ttk.Button(self.stats_window, text="Input country name", command=self.country_popup)
        self.input_country.grid()
        # Layout Config
        self.stats_window.columnconfigure(statistics_fragment, weight=1)
        self.stats_window.rowconfigure(statistics_fragment, weight=1)
        statistics_fragment.columnconfigure(population_label, weight=1)
        statistics_fragment.columnconfigure(population_label, weight=1)

    def get_stats(self):
        try:
            stat = self.COVID_MODULE.get_country_stats(self.COUNTRY_NAME.capitalize())
            self.country_label["text"] = self.COUNTRY_NAME.capitalize()
            self.population_stat["text"] = stat["population"]
            self.new_cases_stat["text"] = stat["cases"]["new"]
            self.active_cases_stat["text"] = stat['cases']['active']
            self.per_million_stat["text"] = stat['cases']['1M_pop']
        except TypeError:
            pass


    def country_popup(self):
        self.dialog = tk.Toplevel(self.master)
        self.dialog.title("Input country")
        self.county_input_label = ttk.Label(self.dialog,text="Input country name here:")
        self.county_input_label.grid(sticky="NSWE")

        self.county_input = ttk.Entry(self.dialog)
        self.county_input.grid(sticky="NSWE")

        self.confirm_dialog_btn = ttk.Button(self.dialog,text="Confirm", command=self.on_click)
        self.confirm_dialog_btn.grid(sticky="NSEW")

    def on_click(self):
        self.COUNTRY_NAME = self.county_input.get()
        self.get_stats()
        self.dialog.destroy()