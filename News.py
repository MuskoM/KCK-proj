import newspaper
from bs4 import BeautifulSoup
import requests
from newspaper import news_pool


class News:

    def __init__(self):
        self.base_url = "https://www.gov.pl/koronawirus/wiadomosci"
        self.base_link = "https://www.gov.pl"
        self.newspaper_link = "https://www.medicalnewstoday.com/"

    def get_who_articles(self):

        covid_articles = newspaper.build(self.newspaper_link,memoize_articles=False)
        titles = open('sites/article_titles.txt', 'w', encoding="utf-8")
        papers = [covid_articles, ]
        news_pool.set(papers,threads_per_source=4)
        news_pool.join()

        for index, article in enumerate(covid_articles.articles):
            print(article.url)
            article.parse()
            titles.write(str(article.title) + "\n")
            write_file = open('sites/articles/article' + str(index) + '.txt', 'w', encoding='utf-8')
            write_file.write(article.text)
            write_file.close()

        titles.close()

    def get_article_urls(self):
        links = []
        base_file = open('sites/article_links.txt','w',encoding='utf-8')
        page = requests.get(self.base_url)

        base_soup = BeautifulSoup(page.text, 'html.parser')

        for divs in base_soup.find_all('div', {"class": "art-prev art-prev--near-menu"}):
            for anchor in divs.find_all('a',):
                print("Found the URL:", anchor['href'])
                links.append(self.base_link + anchor['href'])
        print('======================================================================================================')

        base_file.writelines(i + '\n' for i in links)

        base_file.close()



    def get_gov_articles(self):
        gov_articles = newspaper.build("https://www.gov.pl/web/koronawirus/dzialania-rzadu",memoize_articles=False)
        titles = open('sites/article_titles_gov.txt','a',encoding="utf-8")

        papers = [gov_articles, ]
        news_pool.set(papers, threads_per_source=4)
        news_pool.join()

        for index, article in enumerate(gov_articles.articles):
            print(article.url)
            article.download()
            article.parse()
            write_file = open('sites/gov_articles/article' + str(index) + '.txt', 'w', encoding='utf-8')
            titles.write(str(article.title) + "\n")
            write_file.write(article.text)
            write_file.close()

        titles.close()


