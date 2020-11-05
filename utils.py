import cssutils
import datetime
import requests
import mariadb
import sys
from bs4 import BeautifulSoup as bs


def sql_q(q):
    results = []
    try:
        conn = mariadb.connect(
            user="core_api",
            password="timAnoch",
            host="148.72.172.127",
            port=3306,
            database="core"

        )
        # Get Cursor
        cur = conn.cursor()
        try:
            cur.execute(q)
            results = cur.fetchall()
        except mariadb.Error as e:
            print(f"Error: {e}")
        # conn.commit()
        # conn.close()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return results


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


def get_page(url):
    page = get_url(url)
    return bs(page.content, 'lxml')
