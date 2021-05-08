import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from main.models import Post


class Command(BaseCommand):
    help = 'Parse and fill posts from website'
    website = 'https://doroshenkoaa.ru/med/'

    def handle(self, *args, **kwargs):
        my_request = requests.get(Command.website)
        soup = BeautifulSoup(my_request.content, 'html.parser')
        partial_article = ""
        article_links = []

        for a in soup.select("h2.title > a"):
            article_links.append(a['href'])

        for article in article_links:
            article_request = requests.get(article)
            soup = BeautifulSoup(article_request.content, 'html.parser')
            article_title = soup.find("h1", {"itemprop": "headline"}).text.strip()

            article_part = soup.find_all('div', {"itemprop": "articleBody"})
            for x in article_part:
                for part in x.findAll('p'):
                    partial_article = part.text.strip()

            post = Post(title=article_title, description=' ', content=partial_article)
            post.save()
