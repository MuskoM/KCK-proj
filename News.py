import newspaper
from newspaper import Article
from bs4 import BeautifulSoup
from requests import get


class News:

    def __init__(self):
        self.base_url = "https://www.gov.pl/web/koronawirus/wiadomosci"
        self.base_link = "https://www.gov.pl"

    def get_article_urls(self):
        links = []
        base_file = open('sites/article_links.txt','w',encoding='utf-8')
        page = get(self.base_url)

        base_soup = BeautifulSoup(page.text, 'html.parser')

        for divs in base_soup.find_all('div', {"class": "art-prev art-prev--near-menu"}):
            for anchor in divs.find_all('a',):
                print("Found the URL:", anchor['href'])
                links.append(self.base_link + anchor['href'])
        print('======================================================================================================')

        base_file.writelines(i + '\n' for i in links)

        base_file.close()

    def get_articles(self):
        file = open('sites/article_links.txt','r')

        links = file.readlines()

        for link in links:
            print(link)
