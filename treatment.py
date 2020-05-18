#!/usr/bin/python
# -*- coding: utf-8 -*-
# __author__ = "Albin TCHOPBA"
# __copyright__ = "Copyright 2020 Albin TCHOPBA and contributors"
# __credits__ = ["Albin TCHOPBA and contributors"]
# __license__ = "GPL"
# __version__ = "3"
# __maintainer__ = "Albin TCHOPBA"
# __email__ = "Albin TCHOPBA <atchopba @ gmail dot com"
# __status__ = "Production"

import requests 

import sqlite3
import random, string
from collections import namedtuple

DB_URL = "static/data/urls.db"

TURL = namedtuple("TURL", "url_source url_target")
RURL = namedtuple("RURL", "id url_source url_target")

root_url = "http://bit.ly/"

N = 7

def is_url_exists(url_):
    r = requests.get(url_)
    print("=> url : {} avec {}".format(url_, r.status_code))
    return r.status_code == 200

def generate_url():
    url_dict = UrlClass().get_all_urls()
    while True:
        # Source : https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/
        res = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k = N)) 
        url_res = root_url + res
        if not is_url_exists(url_res) and url_res not in url_dict:
            return url_res


class UrlClass(object):
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_URL)
        self.cur = self.conn.cursor()
        
    def reinit_db(self):
        self.cur.execute("DROP TABLE IF EXISTS urls")
        self.cur.execute(''' CREATE TABLE urls ( 
            id integer PRIMARY KEY,    
            url_source text UNIQUE,
            url_target text UNIQUE
            )''')
        
    def get_last_row_id(self):
        cursor = self.cur.execute("SELECT max(id) FROM urls")
        res = cursor.fetchone()[0]
        return res
    
    def insert_url(self, turl):
        r = "INSERT INTO urls (url_source, url_target) VALUES (?, ?)"
        try:
            self.conn.execute(r, turl)
            self.conn.commit()
            res = self.get_last_row_id()
            return res
        except sqlite3.IntegrityError:
            return None
    
    def delete_url(self, id_):
        r = "DELETE FROM urls WHERE id='{}'".format(id_)
        self.conn.execute(r)
        self.conn.commit()
        #conn.close()
    
    def get_all_urls(self):
        self.cur.execute("SELECT  * FROM urls ORDER BY id ASC")
        rows = self.cur.fetchall()
        return [RURL(row[0], row[1], row[2]) for row in rows]
