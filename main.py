import requests
import cssutils
import datetime
from bs4 import BeautifulSoup as bs

count = 96


def get_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        return None


def get_month(m):
    if m == 1:
        return 'Jan'
    elif m == 2:
        return 'Feb'
    elif m == 3:
        return 'Mar'
    elif m == 4:
        return 'Apr'
    elif m == 5:
        return 'May'
    elif m == 6:
        return 'Jun'
    elif m == 7:
        return 'Jul'
    elif m == 8:
        return 'Aug'
    elif m == 9:
        return 'Sep'
    elif m == 10:
        return 'Oct'
    elif m == 11:
        return 'Nov'
    elif m == 12:
        return 'Dec'


def to_files(item, url, to_file):
    link = url + item.find("a").get('href')
    title = item.find("div", {"class": "article-exert"}).find("strong").text
    exert = item.find("div", {"class": "article-exert"}).find("p").text.replace(title, '')
    try:
        div_style = item.find('div', {"class": "article-tumb"})['style']
        style = cssutils.parseStyle(div_style)
        image_url = url + style['background-image'].replace('url(', '').replace('"', '')[:-1]
    except:
        image_url = url + '/vendor/img/logo_aidas.png'
    try:
        sdate = item.find('span', {'class': 'label-date'}).text
        date = sdate[:5][-2:] + ' ' + get_month(int(sdate[:2])) + ' ' + sdate[-4:] + ' 12:00:00  +0000'
    except:
        date = datetime.datetime.now().strftime("%d %b %Y %I:%M:%S") + ' +0000'
    to_file += '<item>'
    to_file += '<title>' + title.replace(' ', ' ').strip() + '</title>'
    to_file += '<link>' + link + '</link>'
    to_file += '<guid>' + link + '</guid>'
    to_file += '<description>' + '<![CDATA[<img align="left" hspace="5" src="' + image_url + '"/> ' + \
               exert.replace(' ', ' ').strip() + ' ]]>' + '</description>'
    to_file += '<pubDate>' + date + '</pubDate>'
    to_file += '</item>\n'
    return to_file


def get_items(url):
    page = get_url(url)
    soup = bs(page.content, 'lxml')
    return soup.find_all("div", {"class": "article-item"})


def parse(url, stitle, slogo, sdesc, slang, pages):
    global count
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
    for i in range(pages):
        print(i)
        items = get_items(url+'/?page='+str(i+1))
        for item in items:
            count -= 1
            to_file = to_files(item, url, to_file)
            # print(100/96 * (96 - count))
    to_file += '</channel>\n </rss>'
    return to_file


if __name__ == '__main__':
    days_file = parse('https://7days.us', stitle='7 Дней – новости Чикаго на русском',
                      sdesc='Издание русскоязычного сообщества в Chicago. RU новости, статьи, аналитика событий в США '
                            'и мире с точки зрения русскоязычных американцев.',
                      slogo='https://7days.us/vendor/img/logo7.png',
                      slang='ru-ru', pages=3)
    with open('7days.xml', 'w', encoding="utf-8") as f:
    # with open('/var/www/7days_files/digital/7days.xml', 'w', encoding="utf-8") as f:
        f.write(days_file)

    aidas_file = parse('https://aidas.us', stitle='Aidas - Čikaga naujienos, Čikagos lietuviai',
                       sdesc='Nepriklausomas leidinys, skirtas Čikagos ir visos JAV lietuvių  bendruomenei. Svarbiausi '
                             'įvykiai iš pasaulio, JAV ir Čikagos lietuvių gyvenimo, aktualiausios naujienos '
                             'iš Amerikos, Lietuvos, Europos ir viso pasaulio.',
                       slogo='https://aidas.us/vendor/img/logo_aidas.png',
                       slang='lt-lt', pages=3)
    with open('aidas.xml', 'w', encoding="utf-8") as f:
    # with open('/var/www/aidas_files/digital/aidas.xml', 'w', encoding="utf-8") as f:
        f.write(aidas_file)

    detroit_days_file = parse('https://detroit7days.com',
                              stitle='7 Дней Детройт – новости Детройта на русском',
                              sdesc='Издание русскоязычного сообщества в Detroit. RU новости, статьи, аналитика событий'
                                    ' в США и мире с точки зрения русскоязычных американцев.',
                              slogo='https://detroit7days.com/vendor/img/logo7.png',
                              slang='ru-ru', pages=3)
    with open('detroit7days.xml', 'w', encoding="utf-8") as f:
    # with open('/var/www/detroit_files/digital/detroit7days.xml', 'w', encoding="utf-8") as f:
        f.write(detroit_days_file)
