import newspaper
from newspaper import news_pool
import textwrap


class News:

    def __init__(self):
        self.base_url = "https://tvn24.pl/tagi/Koronawirus_w_Polsce"
        self.newspaper_link = "https://www.medicalnewstoday.com/"

    def get_who_articles(self):

        covid_articles = newspaper.build(self.newspaper_link, memoize_articles=False)
        papers = [covid_articles, ]
        news_pool.set(papers, threads_per_source=4)
        news_pool.join()

        for index, article in enumerate(covid_articles.articles):
            print(article.url)
            article.parse()
            write_file = open('sites/articles/article' + str(index) + '.txt', 'w', encoding='utf-8')
            write_file.write(str(article.title) + "\n")
            write_file.write(textwrap.fill(article.text, width=120))
            write_file.close()

    def get_gov_articles(self):
        gov_articles = newspaper.build(self.base_url, memoize_articles=False)

        for index, article in enumerate(gov_articles.articles):
            if index < 15:
                article.download()
                article.parse()
                write_file = open('sites/gov_articles/article' + str(index+1) + '.txt', 'w', encoding='utf-8')
                write_file.write(str(article.title) + "\n")
                write_file.write(textwrap.fill(article.text, width=120))
                write_file.close()
            else:
                break

    def get_my_articles(self, url):
        gov_articles = newspaper.build(url, memoize_articles=False)

        for index, article in enumerate(gov_articles.articles):
            if index < 15:
                article.download()
                article.parse()
                write_file = open('sites/my_articles/article' + str(index+1) + '.txt', 'w', encoding='utf-8')
                write_file.write(str(article.title) + "\n")
                write_file.write(textwrap.fill(article.text, width=120))
                write_file.close()
            else:
                break


