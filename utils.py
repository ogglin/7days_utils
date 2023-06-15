import sys
import datetime
import cssutils
import mariadb
import requests
from bs4 import BeautifulSoup as bs

from env import *


def sql_q(q):
    results = []
    try:
        conn = mariadb.connect(
            user=CORE_USER,
            password=CORE_PASS,
            host=CORE_HOST,
            port=3306,
            database=CORE_DB

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


def sql_q_days(q, site):
    results = []
    try:
        if site == '7days':
            conn = mariadb.connect(
                user=SEVENDAYS_USER,
                password=SEVENDAYS_PASS,
                host=SEVENDAYS_HOST,
                port=3306,
                database=SEVENDAYS_DB
            )
        if site == 'aidas':
            conn = mariadb.connect(
                user=AIDAS_USER,
                password=AIDAS_PASS,
                host=AIDAS_HOST,
                port=3306,
                database=AIDAS_DB
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
