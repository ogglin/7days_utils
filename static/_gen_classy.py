import math
import re

from utils import *

main_url_aidas = 'https://aidas.us/private-ads/'
file_url_aidas = '/var/www/aidas_files/digital/'
main_url_7days = 'https://7days.us/chastnye-obyavleniya/'
file_url_7days = '/var/www/7days_files/digital/'
categories = [
    ('goryachie_predlojeniya', 'Горячие предложения'),
    ('ishchu_rent', 'Ищу рент'),
    ('nedvijimost', 'Недвижимость'),
    ('znakomstva', 'Знакомства'),
    ('sdaetsya', 'Сдается'),
    ('uroki', 'Уроки'),
    ('uslugi', 'Услуги'),
    ('ishchu_rabotu', 'Ищу работу'),
    ('trebuyutsya_na_rabotu', 'Требуются на работу'),
    ('biznes_na_prodaju', 'Бизнес на продажу'),
    ('kuplya-prodaja', 'Купля-Продажа'),
    ('', 'Cars sale'),
    ('', 'Looking for roommate'),
    ('', 'Repair and service'),
    ('', 'Real Estate abroad'),
    ('', 'Miscellaneous'),
]



def get_classys(title, link, pages):
    print(title)
    for p in range(pages):
        print(link + '/' + str(p + 1))
        page = get_page(link + '/' + str(p + 1))
        hrefs = [a for a in page.select('div.class-all a')]
        print(page)


def get_cats():
    page = get_page(main_url_7days)
    cats = []
    hrefs = [a for a in page.select('div.classy-cats a')]
    for href in hrefs:
        count = href.find('span').text.replace('(', '').replace(')', '')
        title = href.text.replace('(' + count + ')', '').strip()
        for cat in categories:
            if cat[1] == title:
                cats.append((title, math.ceil(int(count) / 10), main_url_7days + cat[0]))
    return cats


def init():
    cats = get_cats()
    get_classys(cats[0][0], cats[0][2], cats[0][1])
    for cat in cats:
        get_classys(cat[0], cat[2], cat[1])
