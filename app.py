import npyscreen
from News import News
from CovidStatistics import CovidStatistics
import os


class MyApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("MAIN", MainForm, name="Health and Coivd Tool")
        self.addForm("NEWS", NewsForm, name="News")
        self.addForm("STATISTICS", StatisticsForm, name="Statistics", draw_line_at=12)
        self.addForm("SETTINGS", SettingsForm, name="Settings")
        self.addForm("MYARTICLES", MyArticles, name="MyArticles")

    def change_theme(self, theme):
        if theme == "Colorful":
            npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
            self.onStart()
        elif theme == "Black and White":
            npyscreen.setTheme(npyscreen.Themes.BlackOnWhiteTheme)
            self.onStart()
        elif theme == "Elegant":
            npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
            self.onStart()
        elif theme == "Default":
            npyscreen.setTheme(npyscreen.Themes.DefaultTheme)
            self.onStart()


class MainForm(npyscreen.FormWithMenus):
    main_article = open('sites/articles/article0.txt', 'r', encoding='utf-8')
    title = main_article.readline()
    article = main_article.readlines()

    def create(self):
        self.first_article_title = self.add(npyscreen.TitleText, name=str(self.title), editable=False)
        self.article = self.add(npyscreen.Pager, name="article", values=self.article)
        self.menu = self.new_menu(name="Main Menu", shortcut="m")
        self.menu.addItem("News", self.press_1, "1")
        self.menu.addItem("Statistics", self.press_2, "2")
        self.menu.addItem("Settings", self.press_3, "3")
        self.menu.addItem("Exit", self.exit_program, "^X")
        self.main_article.close()

    def press_1(self):
        self.parentApp.switchForm('NEWS')

    def press_2(self):
        self.parentApp.switchForm("STATISTICS")

    def press_3(self):
        self.parentApp.switchForm("SETTINGS")

    def exit_program(self):
        exit = npyscreen.notify_yes_no("Do you want to exit the program?", "Exit?", editw=1)
        if exit:
            npyscreen.notify_wait("Ok,\n Bye then :(")
            self.parentApp.switchForm(None)
        else:
            self.parentApp.switchForm("MAIN")


class NewsForm(npyscreen.FormWithMenus, npyscreen.ActionForm):
    articles = []
    titles = []

    def create(self):
        self.articles_scraper = News()
        self.title = self.add(npyscreen.TitleText, name=" ", editable=False)
        self.nextrely += 1
        self.page_no = self.add(npyscreen.Slider, name="Page no", value=0, out_of=len(self.articles) + 1,
                                editable=False)
        self.nextrely += 1
        self.page = self.add(npyscreen.Pager, name="Article",
                             values=["There is no articles to view try Getting or "
                                     "Downloading them from the context menu", ], )
        self.menu = self.add_menu("News Menu")
        self.menu.addItem("Next Article", self.get_next_article, '1')
        self.menu.addItem("Previous Article", self.get_previous_article, '2')
        self.submenu_medical = self.menu.addNewSubmenu('Medicalnews Articles', 'm')
        self.submenu_gov = self.menu.addNewSubmenu('TVN24 Articles', 'g')
        self.menu.addItem("My Articles", self.switchToMyArticles, '1')
        self.submenu_medical.addItem("Download", self.download_who_articles, '1')
        self.submenu_medical.addItem("Get", self.get_who_articles, '2')
        self.submenu_gov.addItem("Download", self.download_gov_articles, '1')
        self.submenu_gov.addItem("Get", self.get_gov_articles, '2')

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

    def switchToMyArticles(self):
        self.parentApp.switchForm("MYARTICLES")

    def download_who_articles(self):
        download_answer = npyscreen.notify_yes_no("Do you want to download health articles?\n")
        if download_answer:
            npyscreen.notify_wait("Be patient it might take some time :)")
            self.articles_scraper.get_who_articles()

    def download_gov_articles(self):

        download_answer = npyscreen.notify_yes_no("Do you want to download government articles?\n")
        if download_answer:
            npyscreen.notify_wait("Be patient it might take some time :)")
            self.articles_scraper.get_gov_articles()

    def get_next_article(self):
        try:
            self.page_no.value += 1
            self.page.values = self.articles[int(self.page_no.value)]
            self.title.value = self.titles[int(self.page_no.value)]
        except IndexError:
            self.page_no.value -= 1
            npyscreen.notify_wait("There is no next article to go to!", "ERROR!", form_color="DANGER")

    def get_previous_article(self):
        try:
            self.page_no.value -= 1
            self.page.values = self.articles[int(self.page_no.value)]
            self.title.value = self.titles[int(self.page_no.value)]
        except IndexError:
            self.page_no.value += 1
            npyscreen.notify_wait("There is no previous article to go to!", "ERROR!", form_color="DANGER")

    def get_who_articles(self):
        download = npyscreen.notify_yes_no("Do you want to view health articles", 'Confirm?', editw=1)
        if download:
            self.articles.clear()
            self.titles.clear()
            self.page_no.value = 0
            for file in os.listdir('sites/articles'):
                article_file = open('sites/articles/' + file, encoding='utf-8')
                self.titles.append(article_file.readline())
                self.articles.append(article_file.readlines())
            self.page.values = self.articles[0]
            self.title.value = self.titles[0]
            self.page_no.out_of = len(self.articles)

    def get_gov_articles(self):
        try:
            download = npyscreen.notify_yes_no("Do you want to view government articles", 'Confirm?', editw=1)
            if download:
                self.articles.clear()
                self.titles.clear()
                self.page_no.value = 0
                for file in os.listdir('sites/gov_articles'):
                    article_file = open('sites/gov_articles/' + file, encoding='utf-8')
                    self.titles.append(article_file.readline())
                    self.articles.append(article_file.readlines())
                self.page.values = self.articles[0]
                self.title.value = self.titles[0]
                self.page_no.out_of = len(self.articles)
        except IndexError:
            npyscreen.notify_wait("There is no articles to view, have you tried downloading them?","WARNING",
                                  form_color="WARNING")


class MyArticles(npyscreen.FormWithMenus, npyscreen.ActionForm):
    articles = []
    titles = []

    def create(self):
        self.articles_scraper = News()
        self.give_url = self.add(npyscreen.TitleText, name="Base URL", value="https://www.medicalnewstoday.com/")
        self.nextrely += 1
        self.title = self.add(npyscreen.TitleText, name=" ", editable=False)
        self.nextrely += 1
        self.page_no = self.add(npyscreen.Slider, name="Page no", value=0, out_of=len(self.articles) + 1,
                                editable=False)
        self.nextrely += 1
        self.page = self.add(npyscreen.Pager, name="Article",
                             values=["Hi, if you need articles from other sites type the url up there, but be careful,"
                                     "Some sites might not be formated properly ", ])
        self.menu = self.add_menu("News Menu")
        self.menu.addItem("Next Article", self.get_next_article, '1')
        self.menu.addItem("Previous Article", self.get_previous_article, '2')
        self.menu.addItem("Return to News", self.parentApp.switchFormPrevious, '2')

    def on_ok(self):
        download = npyscreen.notify_yes_no(f"Do you want to download articles from {self.give_url.value} ", 'Confirm?',
                                           editw=1)
        if download:
            self.articles_scraper.get_my_articles(self.give_url.value)
            self.get_my_articles()

    def get_next_article(self):
        try:
            self.page_no.value += 1
            self.page.values = self.articles[int(self.page_no.value)]
            self.title.value = self.titles[int(self.page_no.value)]
        except IndexError:
            self.page_no.value -= 1
            npyscreen.notify_wait("There is no next article to go to!", "ERROR!", form_color="DANGER")

    def get_previous_article(self):
        try:
            self.page_no.value -= 1
            self.page.values = self.articles[int(self.page_no.value)]
            self.title.value = self.titles[int(self.page_no.value)]
        except IndexError:
            self.page_no.value += 1
            npyscreen.notify_wait("There is no previous article to go to!", "ERROR!", form_color="DANGER")

    def get_my_articles(self):
         try:
            self.titles.clear()
            self.articles.clear()
            self.page_no.value = 0
            for file in os.listdir('sites/my_articles'):
                article_file = open('sites/my_articles/' + file, encoding='utf-8')
                self.titles.append(article_file.readline())
                self.articles.append(article_file.readlines())
            self.page.values = self.articles[0]
            self.title.value = self.titles[0]
            self.page_no.out_of = len(self.articles)
         except IndexError:
             npyscreen.notify_wait("Unexpected error ocured, please check the link you set for the download", "ERROR!",
                                   form_color="DANGER")


class StatisticsForm(npyscreen.ActionForm, npyscreen.SplitForm):
    def create(self):
        self.country = self.add(npyscreen.TitleText, name="Country", max_height=1)
        self.population = self.add(npyscreen.TitleText, name="Population")
        self.new_cases = self.add(npyscreen.TitleText, name="New Cases")
        self.active_cases = self.add(npyscreen.TitleText, name="Active Cases")
        self.cases_per_million = self.add(npyscreen.TitleText, name="Per million")
        self.ratio = self.add(npyscreen.TitleSlider, name="New\\active cases ratio %", out_of=50)
        self.nextrely += 1
        self.get_country_stats = self.add(npyscreen.ButtonPress, when_pressed_function=self.get_country_stats,
                                          name="Get Country Statistics")
        self.covid_stats = CovidStatistics()
        self.nextrely += 2
        self.new_section = self.add(npyscreen.TitleFixedText, name="Global statistics",
                                    editable=False, color="DEFAULT")
        self.nextrely += 1
        self.select_continet = self.add(npyscreen.TitleSelectOne, name="Select Continent", max_height=8,
                                        scroll_exit=True,
                                        values=['Europe', 'Asia', 'Australia', 'North-America', 'South-America',
                                                'Africa'])
        self.get_statistics = self.add(npyscreen.ButtonPress, when_pressed_function=self.get_statistics_function,
                                       name="Get Continent Statistics", )

    def get_country_stats(self):
        stats = self.covid_stats.get_country_stats(self.country.value.capitalize())
        if stats is None:
            npyscreen.notify_confirm("Country not found", "ERROR", form_color="STANDOUT")
        else:
            self.population.value = str(stats['population'])
            self.population.display()
            self.new_cases.value = str(stats['cases']['new'])
            self.new_cases.display()
            self.active_cases.value = str(stats['cases']['active'])
            self.active_cases.display()
            self.cases_per_million.value = str(stats['cases']['1M_pop'])
            self.cases_per_million.display()
            self.ratio.value = int(int(stats['cases']['new'][1:]) / stats['cases']['active'] * 100)
            self.ratio.display()

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

    def get_statistics_function(self):
        continent_stats = self.covid_stats.get_country_stats(self.select_continet.get_selected_objects()[0])
        npyscreen.notify_confirm(f"New cases: {continent_stats['cases']['new']}\n"
                                 f"Active cases {continent_stats['cases']['active']}\n"
                                 f"Critical cases: {continent_stats['cases']['critical']}\n"
                                 f"Recovered cases: {continent_stats['cases']['recovered']}\n"
                                 f"Total cases: {continent_stats['cases']['total']}\n",
                                 f"{self.select_continet.get_selected_objects()[0]}")


class AboutForm(npyscreen.ActionForm):
    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


class SettingsForm(npyscreen.ActionForm):
    def create(self):
        self.select_theme = self.add(npyscreen.TitleSelectOne, scroll_exit=True, name="Color Theme",
                                     values=["Colorful", "Black and White", "Elegant", "Default"])

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

    def on_ok(self):
        option = npyscreen.notify_yes_no("Do you want to apply the changes?\n"
                                         "Else theme will be set to Default", editw=1)
        if option:
            npyscreen.notify_wait("Changes saved :)")
            self.parentApp.change_theme(self.select_theme.get_selected_objects()[0])
            self.parentApp.switchForm("MAIN")
        else:
            npyscreen.setTheme(npyscreen.Themes.DefaultTheme)
            self.parentApp.switchForm("MAIN")
