import os

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesnocancel, askyesno,showerror,showinfo
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar
import locale
from News import News
from tkinter.font import Font
from CovidStatistics import CovidStatistics
locale.setlocale(locale.LC_ALL, '')

H1_FONT_SIZE = 24
H2_FONT_SIZE = 18
H3_FONT_SIZE = 15
PARAGRAPGH_FONT_SIZE = 13


class MainWindow(tk.Frame):
    news_viewer_window = None
    stats_window = None
    settings_window = None

    # Initialize the main window and utilities
    def __init__(self, master):
        super().__init__(master)

        # Module containing scraping utilities
        self.news_module = News()

        self.menu_label = ttk.Label(master, text="Health&Covid Tools", anchor="center",
                                    font=Font(size=H1_FONT_SIZE))
        self.menu_label.grid(sticky="NSEW")
        # Main window
        self.news_menu_button = ttk.Button(master, text="News", command=self.open_news_viewer_window)
        self.news_menu_button.grid(sticky="NSEW")
        self.statistics_menu_button = ttk.Button(master, text="Statistics", command=self.open_covid_stats_window)
        self.statistics_menu_button.grid(sticky="NSEW")
        self.settings_menu_button = ttk.Button(master, text="Settings", command=self.open_covid_settings_window)
        self.settings_menu_button.grid(sticky="NSEW")

        self.master.columnconfigure(self.menu_label, weight=1)
        self.master.rowconfigure(self.menu_label, weight=1)
        self.master.columnconfigure(self.news_menu_button, weight=1)
        self.master.rowconfigure(self.news_menu_button, weight=1)
        self.master.columnconfigure(self.statistics_menu_button, weight=1)
        self.master.rowconfigure(self.statistics_menu_button, weight=1)
        self.master.columnconfigure(self.settings_menu_button, weight=1)
        self.master.rowconfigure(self.settings_menu_button, weight=1)

    def open_covid_stats_window(self):
        self.covid_stats_window = CovidStatsWindow(self)

    def open_covid_settings_window(self):
        self.covid_settings_window = SettingsWindow(self)

    # Opens a window with news reader
    def open_news_viewer_window(self):
        self.news_viewer_window = NewsWindow(self)


class NewsWindow:
    def __init__(self, master):
        self.master = master
        news_module = News()
        self.news_viewer_window = tk.Toplevel(self.master)
        self.news_viewer_window.title("News Viewer")

        # Notebook
        self.news_notebook = ttk.Notebook(self.news_viewer_window)
        self.gov_tab = NotebookTab(self.news_notebook, text="GOV Articles", path="sites/gov_articles/",
                                   download_function=news_module.get_gov_articles)
        self.who_tab = NotebookTab(self.news_notebook, text="WHO Articles", path="sites/articles/",
                                   download_function=news_module.get_who_articles)
        self.my_tab = NotebookTab(self.news_notebook, text="My Articles", path="sites/my_articles/",
                                  download_function=None)

        self.news_notebook.grid(sticky="NSWE")
        self.news_viewer_window.rowconfigure(self.news_notebook,weight=1)
        self.news_viewer_window.columnconfigure(self.news_notebook,weight=1)


class SettingsWindow:
    def __init__(self, master):
        self.master = master
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.title("Settings")

        # Color Selection
        my_articles_config_frame = ttk.Frame(self.settings_window)
        ttk.Label(my_articles_config_frame, text="My Articles").grid(column=0,row=0)
        self.URL_config = ttk.Entry(my_articles_config_frame)
        self.URL_config.grid(column=1,row=0,sticky="EW")
        my_articles_config_frame.grid(sticky="EW")
        ttk.Separator(my_articles_config_frame, orient="horizontal").grid()
        save_config_btn = tk.Button(self.settings_window, text="Save", command=self.save, anchor="ne",)
        save_config_btn.grid(sticky="s")

        config_file = open('bin/config.conf')
        self.URL_config.insert("1",config_file.readline().split("=")[1])

        self.settings_window.rowconfigure(my_articles_config_frame,weight=1)
        self.settings_window.columnconfigure(my_articles_config_frame,weight=1)
        my_articles_config_frame.rowconfigure(self.URL_config, weight=1)
        my_articles_config_frame.columnconfigure(self.URL_config, weight=1)

    def save(self):
        config_file = open('bin/config.conf', "w")
        config_file.write(f"URL={self.URL_config.get()}")
        config_file.close()
        showinfo("Settings","Settings Saved!",parent=self.settings_window)



class CovidStatsWindow:
    def __init__(self, master):
        self.master = master
        self.COVID_MODULE = CovidStatistics()
        self.COUNTRY_NAME = "Poland"
        self.stats_window = tk.Toplevel(self.master)
        # self.stats_window.maxsize(300, 300)
        self.stats_window.title("Covid Stats")

        statistics_fragment = ttk.Frame(self.stats_window)
        statistics_fragment.grid(sticky="NSWE")

        self.country_label = ttk.Label(statistics_fragment, text=self.COUNTRY_NAME, font=Font(size=H1_FONT_SIZE))
        self.country_label.grid(sticky="NSWE", column=0, row=0)

        self.population_stat = ttk.Label(statistics_fragment, text="Population: ", font=Font(size=H2_FONT_SIZE))
        self.population_stat.grid(row=1)

        self.new_cases_stat = ttk.Label(statistics_fragment, text="00000000", font=Font(size=H2_FONT_SIZE))
        self.new_cases_stat.grid(sticky="NSW", row=2)

        self.active_cases_stat = ttk.Label(statistics_fragment, text="00000000", font=Font(size=H2_FONT_SIZE))
        self.active_cases_stat.grid(sticky="NSW", row=3)

        self.per_million_stat = ttk.Label(statistics_fragment, text="00000000", font=Font(size=H2_FONT_SIZE))
        self.per_million_stat.grid(sticky="NSW", row=4)
        self.get_stats()

        self.input_country = ttk.Button(statistics_fragment, text="Input country name", command=self.country_popup)
        self.input_country.grid()

        self.global_stats_fragment = ttk.Frame(self.stats_window, padding= "20px 0px 5px 0px")
        self.global_stats_fragment.grid(sticky="NSWE", column=1, row=0)

        global_stats_label = ttk.Label(self.global_stats_fragment, text="Global statistics", font=Font(size=H1_FONT_SIZE))
        global_stats_label.grid(sticky="NSWE")

        self.global_new_cases = ttk.Label(self.global_stats_fragment, text="New cases: ", font=Font(size=H2_FONT_SIZE))
        self.global_new_cases.grid(sticky="NSWE")

        self.global_active_cases = ttk.Label(self.global_stats_fragment, text="New cases: ", font=Font(size=H2_FONT_SIZE))
        self.global_active_cases.grid(sticky="NSWE")

        self.global_critical_cases = ttk.Label(self.global_stats_fragment, text="New cases: ", font=Font(size=H2_FONT_SIZE))
        self.global_critical_cases.grid(sticky="NSWE")

        self.global_recovered_cases = ttk.Label(self.global_stats_fragment, text="New cases: ", font=Font(size=H2_FONT_SIZE))
        self.global_recovered_cases.grid(sticky="NSWE")

        self.global_total_cases = ttk.Label(self.global_stats_fragment, text="New cases: ", font=Font(size=H2_FONT_SIZE),
                                            padding="0px 0px 0px 5px")
        self.global_total_cases.grid(sticky="NSWE")

        self.global_stats_box = ttk.Combobox(self.global_stats_fragment, state="readonly")
        self.global_stats_box["values"] = ('Europe', 'Asia', 'Australia', 'North-America', 'South-America',
                                                'Africa')
        self.global_stats_box.current(0)
        self.get_global_stats()
        self.global_stats_box.grid(sticky="NSEW")

        self.get_global_stats_btn  = ttk.Button(self.global_stats_fragment, text="Get Global Stats",
                                                command=self.get_global_stats)
        self.get_global_stats_btn.grid()

        # Layout Config
        self.stats_window.columnconfigure(statistics_fragment, weight=1)
        self.stats_window.rowconfigure(statistics_fragment, weight=1)

    def get_stats(self):
        try:
            stat = self.COVID_MODULE.get_country_stats(self.COUNTRY_NAME.capitalize())
            self.country_label["text"] = self.COUNTRY_NAME.capitalize()
            self.population_stat["text"] = f"Population: {stat['population']:n}"
            self.new_cases_stat["text"] = f"New Cases: {int(stat['cases']['new']):n}"
            self.active_cases_stat["text"] = f"Active Cases: {stat['cases']['active']:n}"
            self.per_million_stat["text"] = f"Per 1 million: {int(stat['cases']['1M_pop']):n}"
        except TypeError:
            print("Error")

    def get_global_stats(self):
        continent_stats = self.COVID_MODULE.get_country_stats(self.global_stats_box.get())
        self.global_active_cases["text"] = f"Active cases: {continent_stats['cases']['active']:n}"
        self.global_critical_cases["text"] = f"Critical cases: {continent_stats['cases']['critical']:n}"
        self.global_new_cases["text"] = f"New cases: {int(continent_stats['cases']['new']):n}"
        self.global_recovered_cases["text"] = f"Recovered cases: {continent_stats['cases']['recovered']:n}"
        self.global_total_cases["text"] = f"Total cases: {continent_stats['cases']['total']:n}"

    def country_popup(self):
        self.dialog = tk.Toplevel(self.master)
        self.dialog.title("Input country")
        self.county_input_label = ttk.Label(self.dialog, text="Input country name here:", padding="0px 0px 0px 5px")
        self.county_input_label.grid(sticky="NSWE")

        self.county_input = ttk.Entry(self.dialog)
        self.county_input.grid(sticky="NSWE")

        self.confirm_dialog_btn = ttk.Button(self.dialog, text="Confirm", command=self.on_click)
        self.confirm_dialog_btn.grid(sticky="NSEW")

    def on_click(self):
        self.COUNTRY_NAME = self.county_input.get()
        self.get_stats()
        self.dialog.destroy()


class NotebookTab:
    def __init__(self, notebook, **kwargs):
        config_file = open('./bin/config.conf')
        self.URL = config_file.readline().split("=")[1]
        config_file.close()
        self.title = kwargs["text"]
        self.files_path = kwargs["path"]
        self.download_function = kwargs["download_function"]
        self.articles = []
        self.titles = []
        self.page_no = 0
        self.news_module = News()
        self.notebook = notebook
        self.gov_articles_tab = ttk.Frame(notebook)
        notebook.add(self.gov_articles_tab, text=kwargs["text"])

        # Article label
        self.news_title_label = ttk.Label(self.gov_articles_tab, text="Title", font=Font(size=H1_FONT_SIZE), )
        self.news_title_label.grid(sticky="NSWE")
        # Container for the article
        self.news_reader_fragment = ScrolledText(self.gov_articles_tab, font=Font(size=PARAGRAPGH_FONT_SIZE))
        self.news_reader_fragment.insert('1.0', 'Download and Load Articles to see anything')
        self.news_reader_fragment['state'] = 'disabled'
        self.news_reader_fragment.grid(sticky="NSWE")
        # Article number indicator
        self.news_article_page_progress = Progressbar(self.gov_articles_tab,
                                                      mode="determinate")
        self.news_article_page_progress['value'] = 0
        self.news_article_page_progress.grid(sticky="NSWE")
        self.news_article_page_progress.update()
        self.news_title_label.config(wraplength=self.news_article_page_progress.winfo_width())
        buttons_grid_frame = ttk.Frame(self.gov_articles_tab)
        buttons_grid_frame.grid(row=3, column=0)
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
        get_health_articles_button = ttk.Button(article_buttons_frame,
                                                text="Load Articles",
                                                command=self.get_articles).grid(row=0, column=2)

        # Frame for download_article_type buttons
        download_health_articles_button = ttk.Button(article_buttons_frame,
                                                     text="Download Articles",
                                                     command=self.download_articles).grid(row=0, column=3)

        self.gov_articles_tab.columnconfigure(self.news_title_label,weight=1)
        self.gov_articles_tab.rowconfigure(self.news_title_label,weight=1)
        self.gov_articles_tab.rowconfigure(self.news_reader_fragment,weight=10)
        self.gov_articles_tab.columnconfigure(self.news_reader_fragment,weight=10)

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

    def get_articles(self):
        download = askyesno('Confirm?', f"Do you want to view {self.title}", parent=self.notebook)
        if download:
            self.articles.clear()
            self.titles.clear()
            self.news_article_page_progress["value"] = 0
            for file in os.listdir(self.files_path):
                article_file = open(self.files_path + file, encoding='utf-8')
                self.titles.append(article_file.readline())
                self.articles.append(article_file.read())
            self.news_reader_fragment["state"] = "normal"
            self.news_reader_fragment.delete("1.0", "end")
            self.news_reader_fragment.insert("1.0", self.articles[0])
            self.news_reader_fragment["state"] = "disabled"
            self.news_title_label["text"] = self.titles[0]
            self.news_article_page_progress["maximum"] = len(self.articles)

    def get_articles_wthout_confirmation(self):
        self.articles.clear()
        self.titles.clear()
        self.news_article_page_progress["value"] = 0
        for file in os.listdir(self.files_path):
            article_file = open(self.files_path + file, encoding='utf-8')
            self.titles.append(article_file.readline())
            self.articles.append(article_file.read())
        self.news_reader_fragment["state"] = "normal"
        self.news_reader_fragment.delete("1.0", "end")
        self.news_reader_fragment.insert("1.0", self.articles[0])
        self.news_reader_fragment["state"] = "disabled"
        self.news_title_label["text"] = self.titles[0]
        self.news_article_page_progress["maximum"] = len(self.articles)

    def download_articles(self):
        download = askyesno("Download?", f"Do you want to download {self.title} ?, This might take a while.",
                            parent=self.notebook)
        if download:
            if self.download_function is not None:
                self.download_function
            else:
                if self.URL is None:
                    self.articles_popup()
                else:
                    try:
                        self.news_module.get_my_articles(self.URL)
                    except Exception:
                        showerror("ERROR!", "Bad URL, try again!", parent=self.notebook)
                        self.articles_popup()

    def articles_popup(self):
        self.dialog = tk.Toplevel(self.notebook)
        self.dialog.title("Input URL")
        self.county_input_label = ttk.Label(self.dialog, text="Input URL here:", padding="0px 0px 0px 5px")
        self.county_input_label.grid(sticky="NSWE")

        self.URL_input = ttk.Entry(self.dialog)
        self.URL_input.grid(sticky="NSWE")

        self.confirm_dialog_btn = ttk.Button(self.dialog, text="Confirm", command=self.on_click)
        self.confirm_dialog_btn.grid(sticky="NSEW")

    def on_click(self):
        self.URL = self.URL_input.get()
        try:
            self.news_module.get_my_articles(self.URL)
        except Exception:
            showerror("ERROR!", "Bad URL, try again!", parent=self.dialog)
            self.articles_popup()
        config_file = open('./bin/config.conf',"w")
        config_file.write(f"URL={self.URL}")
        config_file.close()
        self.dialog.destroy()

