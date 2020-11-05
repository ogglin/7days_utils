import math
import re

from utils import *

main_url_aidas = 'https://aidas.us/private-ads/'
file_url_aidas = '/var/www/aidas_files/digital/'
main_url_7days = 'https://7days.us/chastnye-obyavleniya/'
file_url_7days = '/var/www/7days_files/digital/'
categories = [
    ('Purchase-Sale', 'purchase_sale'),
    ('Business for sale', 'business_sale'),
    ('Offer Job', 'offer_job'),
    ('Seek Job', 'seek_job'),
    ('Service', 'service'),
    ('Lessons', 'lessons'),
    ('Rent', 'rent'),
    ('Miscellaneous', 'miscellaneous'),
    ('Dating', 'dating'),
    ('Looking for roommate', 'roommate'),
    ('Real Estate', 'real_estate'),
    ('Looking for rent', 'looking_rent'),
    ('Real Estate abroad', 'real_estate_abroad'),
    ('Cars sale', 'cars_sale'),
    ('Repair and service', 'repair_service'),
]


def get_classy(adv_id1, adv_id2, place):
    now_date = datetime.datetime.now().strftime("%Y-%m-%d")
    q = f'''SELECT adv.id, cat.name, adv.format, adv.newspaper_content FROM advertise adv
            LEFT JOIN categories cat ON cat.id = adv.categories_id WHERE adv.active = 1 and adv.end_date > '{now_date}' 
            and (adv.advertise_template_id = {adv_id1} or adv.advertise_template_id = {adv_id2}) ORDER BY cat.name'''
    classys = sql_q(q)
    temp_classy = []
    for category in categories:
        for classy in classys:
            cid = classy[0]
            cat = classy[1]
            formats = classy[2]
            if category[0] == cat:
                text = re.sub(r'[*]', '', classy[3], 0, re.I).strip()
                temp_classy.append((cid, text, cat))
        if len(temp_classy) > 0:
            to_files(place, category[1], category[0], temp_classy)
        temp_classy = []


def to_files(place, filename, category, classys):
    stitle = ''
    sdesc = ''
    slang = ''
    slogo = ''
    url = ''
    path = ''
    if place == '7days':
        stitle = 'Частные объявления'
        sdesc = '''Ищете работу? Хотите познакомиться? Хотите снять квартиру? Просмотрите наши объявления. 
        Ищете сотрудников? Хотите сдать квартиру в рент? Разместите свое объявление.'''
        slang = 'ru'
        slogo = 'https://7days.us/vendor/img/logo7.png'
        url = 'https://7days.us/chastnye-obyavleniya'
        path = '/var/www/7days_files/digital/'
    if place == 'aidas':
        stitle = 'Asmeniniai skelbimai'
        sdesc = '''Ieškote darbo? Norėtumėte susipažinti? Išsinuomoti butą? Peržiūrėkite mūsų skelbimus. 
        Ieškote darbuotojų? Nuomojate butą? Įdėkite savo skelbimą.'''
        slang = 'lt'
        slogo = 'https://aidas.us/vendor/img/logo_aidas.png'
        url = 'https://aidas.us/private-ads'
        path = '/var/www/aidas_files/digital/'
    to_file = '''<rss version="2.0">
                <channel>
                    <title>''' + stitle + '''</title>
                    <link>''' + url + '''</link>
                    <description>''' + sdesc + '''</description>
                    <language>''' + slang + '''</language>
                    <copyright>Copyright Ethnic Media USA © 2014-2020 All rights reserved.</copyright>
                    <image>
                        <url>''' + slogo + '''</url>
                        <title>''' + stitle + '''</title>
                        <link>''' + url + '''</link>
                    </image>
                ''' + '<lastBuildDate>' + datetime.datetime.now().strftime(
        "%d %b %Y %I:%M:%S") + ' +0000' + '</lastBuildDate>\n'
    date = datetime.datetime.now().strftime("%d %b %Y %I:%M:%S") + ' +0000'
    for classy in classys:
        print(classy)
        to_file += '<item>'
        to_file += '<title>' + classy[2] + '</title>'
        to_file += '<link>' + url + '</link>'
        to_file += '<guid>' + url + '</guid>'
        to_file += '<description>' + '<![CDATA[<p>' + classy[1] + '</p>]]>' + '</description>'
        to_file += '<pubDate>' + date + '</pubDate>'
        to_file += '</item>\n'
    to_file += '</channel>\n </rss>'
    print(filename, to_file)
    with open(path + filename + '.xml', 'w', encoding="utf-8") as f:
        f.write(to_file)


def init():
    get_classy(1, 2, '7days')
    get_classy(3, 4, 'aidas')