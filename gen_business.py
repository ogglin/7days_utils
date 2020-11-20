import re

from utils import *

category_list_7days = [
    ('avto', 'Авто-Мото'),
    ('gruzoperevozki', 'Грузоперевозки'),
    ('iskusstvo-i-razvlecheniya', 'Искусство и Развлечения'),
    ('magaziny', 'Магазины'),
    ('religioznyye-organizatsii', 'Общественные организации'),
    ('produkty', 'Продукты'),
    ('strakhovka', 'Страхование'),
    ('trebuyutsya-na-rabotu', 'Требуются водители траков'),
    ('yuristy-advokaty', 'Юристы, адвокаты'),
    ('uslugi', 'Бытовые услуги'),
    ('meditsina', 'Здоровье и Медицина'),
    ('obsluzhivaniye-i-remont-kompyuterov', 'Компьютеры и сайты'),
    ('nedvizhimost', 'Недвижимость'),
    ('otdykh', 'Отдых'),
    ('puteshestviya', 'Путешествия'),
    ('tovary-i-uslugi-dlya-zhivotnykh', 'Товары и услуги для животных'),
    ('advokatyfinansy', 'Финансы'),
    ('yakhty', 'Яхты'),
    ('vse-dlya-doma', 'Все для дома'),
    ('internet-i-tv-provaydery', 'Интернет и ТВ провайдеры'),
    ('krasota-i-ukhod-za-soboy', 'Красота и уход'),
    ('obucheniye', 'Обучение'),
    ('oformleniye-dokumentov', 'Оформление/перевод документов'),
    ('restorany', 'Рестораны'),
    ('trebuyutsya', 'Требуются'),
    ('ekstrasensy', 'Экстрасенсы, астрологи'),
]

category_list_aidas = [
    ('draudimas', 'Draudimas'),
    ('finansai-advokatai', 'Finansai, advokatai'),
    ('keliones', 'Kelionės'),
    ('medicina', 'Medicina'),
    ('nekilnojamasis-turtas', 'Nekilnojamasis turtas'),
    ('parduotuves-ispardavimai', 'Parduotuvės, išpardavimai'),
    ('paslaugos', 'Paslaugos'),
    ('restoranai', 'Restoranai'),
    ('siulo-darba', 'Siūlo darbą'),
    ('siuntos', 'Siuntos'),
    ('stomatologija', 'Stomatologija'),
    ('svietimas-ugdymas', 'Švietimas, ugdymas'),
    ('pramogos', 'Pramogos'),
]


def get_aidas_business():
    url = 'https://aidas.us/ethnic-ads/'
    sdesc = 'Verslo Čikaga.'
    slang = 'lt-lt'
    slogo = 'https://aidas.us/vendor/img/logo_aidas.png'
    image_url = 'https://aidas.us/frontend/web/uploads/chicago/'
    for cat in category_list_aidas:
        q = f'''SELECT cc.name, cc.description, cc.image, cc.alias FROM chicago_companies as cc
                LEFT JOIN chicago_categories as ccat on cc.chicago_categories_id = ccat.id
                LEFT JOIN chicago_categories as pcat on ccat.parent_id = pcat.id 
                WHERE cc.status = 1 and (pcat.name = '{cat[1]}' or ccat.name = '{cat[1]}')'''
        business = sql_q_days(q, 'aidas')
        to_file = '''<rss version="2.0">
                    <channel>
                        <title>''' + cat[1] + '''</title>
                        <link>''' + url + '''</link>
                        <description>''' + sdesc + '''</description>
                        <language>''' + slang + '''</language>
                        <copyright>Copyright Ethnic Media USA © 2014-2020 All rights reserved.</copyright>
                        <image>
                            <url>''' + slogo + '''</url>
                            <title>''' + cat[1] + '''</title>
                            <link>''' + url + '''</link>
                        </image>
                    ''' + '<lastBuildDate>' + datetime.datetime.now().strftime(
            "%d %b %Y %I:%M:%S") + ' +0000' + '</lastBuildDate>\n'
        for item in business:
            title = item[0]
            desc = item[1]
            if item[2]:
                image = image_url + item[2]
            else:
                image = ''
            alias = item[3]
            to_file += '<item>'
            to_file += '<title>' + title.replace('&', '&amp;').replace(' ', ' ').strip() + '</title>'
            to_file += '<link>' + url + cat[0] + '/' + alias + '</link>'
            to_file += '<guid>' + url + cat[0] + '/' + alias + '</guid>'
            to_file += '<description>' + '<![CDATA[<img align="left" hspace="5" src="' + image + '"/> ' + \
                       desc.strip() + ' ]]>' + '</description>'
            to_file += '<pubDate>' + datetime.datetime.now().strftime("%d %b %Y %I:%M:%S") + '</pubDate>'
            to_file += '</item>\n'
        to_file += '</channel>\n </rss>'
        with open('/var/www/aidas_files/digital/business/'+cat[0]+'.xml', 'w', encoding="utf-8") as f:
            f.write(to_file)


def get_7days_business():
    url = 'https://7days.us/ethnic-ads/'
    sdesc = 'Бизнес компании Чикаго.'
    slang = 'ru-ru'
    slogo = 'https://7days.us/vendor/img/logo7.png'
    image_url = 'https://7days.us/backend/web/uploads/chicago/'
    for cat in category_list_7days:
        q = f'''SELECT cc.name, cc.description, cc.image, cc.alias FROM chicago_companies as cc
                LEFT JOIN chicago_categories as ccat on cc.chicago_categories_id = ccat.id
                LEFT JOIN chicago_categories as pcat on ccat.parent_id = pcat.id 
                WHERE cc.status = 1 and (pcat.name = '{cat[1]}' or ccat.name = '{cat[1]}')'''
        business = sql_q_days(q, '7days')
        to_file = '''<rss version="2.0">
                    <channel>
                        <title>''' + cat[1] + '''</title>
                        <link>''' + url + '''</link>
                        <description>''' + sdesc + '''</description>
                        <language>''' + slang + '''</language>
                        <copyright>Copyright Ethnic Media USA © 2014-2020 All rights reserved.</copyright>
                        <image>
                            <url>''' + slogo + '''</url>
                            <title>''' + cat[1] + '''</title>
                            <link>''' + url + '''</link>
                        </image>
                    ''' + '<lastBuildDate>' + datetime.datetime.now().strftime(
            "%d %b %Y %I:%M:%S") + ' +0000' + '</lastBuildDate>\n'
        for item in business:
            title = item[0]
            desc = item[1]
            if item[2]:
                image = image_url + item[2]
            else:
                image = ''
            alias = item[3]
            to_file += '<item>'
            to_file += '<title>' + title.replace('&', '&amp;').replace(' ', ' ').strip() + '</title>'
            to_file += '<link>' + url + cat[0] + '/' + alias + '</link>'
            to_file += '<guid>' + url + cat[0] + '/' + alias + '</guid>'
            to_file += '<description>' + '<![CDATA[<img align="left" hspace="5" src="' + image + '"/> ' + \
                       desc.strip() + ' ]]>' + '</description>'
            to_file += '<pubDate>' + datetime.datetime.now().strftime("%d %b %Y %I:%M:%S") + '</pubDate>'
            to_file += '</item>\n'
        to_file += '</channel>\n </rss>'
        with open('/var/www/7days_files/digital/business/' + cat[0] + '.xml', 'w', encoding="utf-8") as f:
            f.write(to_file)


def init():
    get_aidas_business()
    get_7days_business()
