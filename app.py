import npyscreen
from News import News
from CovidStatistics import CovidStatistics
import os


class MyApp(npyscreen.NPSAppManaged):
    def onStart(self):
        npyscreen.setTheme(npyscreen.Themes.DefaultTheme)
        self.addForm("MAIN", MainForm, name="Health and Coivd Tool")
        self.addForm("NEWS", NewsForm, name="News")
        self.addForm("STATISTICS", StatisticsForm, name="Statistics", draw_line_at=10)
        self.addForm("SETTINGS", SettingsForm, name="Settings")


class MainForm(npyscreen.FormWithMenus):

    title_file = open('sites/article_titles.txt', 'r', encoding='utf-8')
    main_article = open('sites/articles/article0.txt', 'r')

    article = main_article.readlines()
    def create(self):
        self.first_article_title = self.add(npyscreen.TitleText, name=str(self.title_file.readline()), editable=False)
        self.article = self.add(npyscreen.Pager,name="article", values=self.article)
        self.menu = self.new_menu(name="Main Menu", shortcut="m")
        self.menu.addItem("News", self.press_1, "1")
        self.menu.addItem("Statistics", self.press_2, "2")
        self.menu.addItem("Settings", self.press_3, "3")
        self.menu.addItem("Exit", self.exit_program, "^X")
        self.title_file.close()
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
        self.title = self.add(npyscreen.TitleText,name =" ", editable=False)
        self.nextrely +=1
        self.page_no = self.add(npyscreen.Slider, name="Page no", value=0, out_of=len(self.articles)+1, editable=False)
        self.nextrely += 1
        self.page = self.add(npyscreen.Pager, name="Article",
                             values = ["There is no articles to view",])
        self.menu = self.add_menu("News Menu")
        self.menu.addItem("Next Article",self.get_next_article,'1')
        self.menu.addItem("Previous Article",self.get_previous_article,'2')
        self.submenu_medical = self.menu.addNewSubmenu('Medical Articles', 'm')
        self.submenu_gov = self.menu.addNewSubmenu('Government Articles', 'g')
        self.submenu_medical.addItem("Download",self.download_who_articles, '1')
        self.submenu_medical.addItem("Get",self.get_who_articles, '2')
        self.submenu_gov.addItem("Download", self.download_gov_articles, '1')
        self.submenu_gov.addItem("Get", self.get_gov_articles, '2')

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

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
        if self.page_no.value < self.page_no.out_of:
            self.page_no.value += 1
            self.page.values = self.articles[int(self.page_no.value)]
            self.title.value= self.titles[int(self.page_no.value)]
        else:
            self.page_no.value = self.page_no.value

    def get_previous_article(self):
        if self.page_no.value > 0:
            self.page_no.value -= 1
            self.page.values = self.articles[int(self.page_no.value)]
            self.title.value = self.titles[int(self.page_no.value)]
        else:
            self.page_no.value = self.page_no.value

    def get_who_articles(self):
        download = npyscreen.notify_yes_no("Do you want to view health articles", 'Confirm?', editw=1)
        if download:
            self.articles.clear()
            self.page_no.value = 0
            title_file = open('sites/article_titles.txt', encoding='utf-8')
            self.titles = [title for title in title_file]
            for file in os.listdir('sites/articles'):
                article_file = open('sites/articles/' + file, encoding='utf-8')
                self.articles.append(article_file.readlines())
            self.page.values = self.articles[0]
            self.title.value = self.titles[0]
            self.page_no.out_of = len(self.articles)

    def get_gov_articles(self):
        download = npyscreen.notify_yes_no("Do you want to view government articles", 'Confirm?', editw=1)
        if download:
            self.articles.clear()
            self.page_no.value = 0
            title_file = open('sites/article_titles_gov.txt', encoding='utf-8')
            self.titles = [title for title in title_file]
            for file in os.listdir('sites/gov_articles'):
                article_file = open('sites/gov_articles/' + file, encoding='utf-8')
                self.articles.append(article_file.readlines())
            self.page.values = self.articles[0]
            self.title.value = self.titles[0]
            self.page_no.out_of = len(self.articles)


class StatisticsForm(npyscreen.ActionForm, npyscreen.SplitForm):
    def create(self):
        self.country = self.add(npyscreen.TitleText, name="Country", max_height=1)
        self.population = self.add(npyscreen.TitleText, name="Population")
        self.new_cases = self.add(npyscreen.TitleText, name="New Cases")
        self.active_cases = self.add(npyscreen.TitleText, name="Active Cases")
        self.cases_per_million = self.add(npyscreen.TitleText, name="Per million")
        self.ratio = self.add(npyscreen.TitleSlider, name="New\\active cases ratio %", out_of=50)
        self.nextrely += 1
        self.covid_stats = CovidStatistics()
        self.new_section = self.add(npyscreen.TitleFixedText, name="Country with highiest number of new cases",
                                    editable=False, color="DEFAULT")

    def on_ok(self):
        stats = self.covid_stats.get_country_stats(self.country.value)
        if stats is None:
            npyscreen.notify_confirm("Country not found", "ERROR", form_color="STANDOUT")
        else:
            self.population.value = str(stats['population'])
            self.new_cases.value = str(stats['cases']['new'])
            self.active_cases.value = str(stats['cases']['active'])
            self.cases_per_million.value = str(stats['cases']['1M_pop'])
            self.ratio.value = int(int(stats['cases']['new'][1:]) / stats['cases']['active'] * 100)

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


class AboutForm(npyscreen.ActionForm):
    def on_cancel(self):
        self.parentApp.switchForm("MAIN")


class SettingsForm(npyscreen.ActionForm):
    def create(self):
        self.selected = self.add(npyscreen.TitleText, name="Selected")
        self.select_theme = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name="Color Theme",
                                     values=["Colorful", "Black and White", "Elegant", "Default"])

    def on_cancel(self):
        self.parentApp.switchForm("MAIN")

    def on_ok(self):
        self.selected.value = self.select_theme.value

        if self.select_theme.value == [0]:
            npyscreen.setTheme(npyscreen.Themes.ColorfulTheme)
        elif self.select_theme.value == [1]:
            npyscreen.setTheme(npyscreen.Themes.BlackOnWhiteTheme)
        elif self.select_theme.value == [2]:
            npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        elif self.select_theme.value == [3]:
            npyscreen.setTheme(npyscreen.Themes.DefaultTheme)

        option = npyscreen.notify_yes_no("Do you want to apply the changes?\n"
                                         "Else theme will be set to Default", editw=1)
        if option:
            npyscreen.notify_wait("Changes saved :)")
            self.parentApp.switchForm("MAIN")
        else:
            npyscreen.setTheme(npyscreen.Themes.DefaultTheme)
            self.parentApp.switchForm("MAIN")
