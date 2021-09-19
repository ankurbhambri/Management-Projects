import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

from movies.models import Movie
from movies.views import try_or


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str,
                            help='Indicates the url')
        # parser.add_argument('--step', type=int,
        #                     help='Indicates the range while fetching data')

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        # step = kwargs['step']
        r = requests.get(url)
        htmlcont = r.content
        count = 0
        already_count = 0
        context = {}
        soup = BeautifulSoup(htmlcont, 'html.parser')
        pagecontent = soup.find_all("div", class_="pagecontent")
        content_tuple = list()
        for i in pagecontent:
            titles = i.find_all("td", {"class": "titleColumn"})
            ratings = i.find_all("td", {"class": "ratingColumn imdbRating"})
            content_tuple = list(zip(titles, ratings))

        for tittle, ratings in content_tuple:
            context = {
                "tittle": try_or(
                    lambda: tittle.find("a").get_text(), ''),
                "year": try_or(
                    lambda: int(
                        tittle.find("span").get_text().strip("()")), ''),
                "rating": try_or(
                    lambda: float(
                        ratings.find("strong").get_text()), '')
            }
            url2 = "https://www.imdb.com/" + tittle.find("a").get('href')
            r2 = requests.get(url2)
            htmlcont2 = r2.content
            soup2 = BeautifulSoup(htmlcont2, 'html.parser')
            img_data = soup2.find("div", class_="poster")
            data1 = soup2.find_all("div", class_="title_block")
            data2 = soup2.find_all("div", class_="plot_summary")
            img_url = try_or(
                lambda: img_data.find("img").get("src"), '')
            for i in data1:
                context['extra_feild'] = {
                    "release_data": try_or(
                        lambda: i.find_all('a')[-1].get_text().strip('\n'), ''),
                    "runtime": try_or(
                        lambda: i.find('time').get_text().strip(' \n '), '')
                }
            for i in data2:
                context['extra_feild'].update({
                    "director": try_or(
                        lambda: i.find(
                            class_="credit_summary_item").get_text().split('\n')[-1], ''),
                    "writers": try_or(
                        lambda: i.find_all(
                            class_="credit_summary_item")[1].get_text().split('\n')[2], ''),
                    "summary_text": try_or(
                        lambda: i.find(class_="summary_text").get_text().strip(' \n '), '')
                })
            movie_obj = Movie.objects.filter(
                tittle=tittle.find("a").get_text(),
                year=int(tittle.find("span").get_text().strip("()")),
                rating=float(ratings.find("strong").get_text())
            )
            if movie_obj:
                already_count += 1
            else:
                Movie.objects.create(image_url=img_url, **context)
                count += 1
        print(already_count, "movies data alread in system")
        print(count, "movies data successfully inserted")
