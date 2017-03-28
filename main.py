#-*- coding:utf-8 -*-
import re
import urlparse
import urllib
import urllib2
import time
from datetime import datetime
import datetime
import robotparser
import Queue
import time
from lxml import etree
import cookieget
from pymongo import MongoClient
import dabaojiao
import Great_Barrier_Reef
import aierlihaitan
import Airlie_Beach


def get_db():
    client = MongoClient('localhost', 27017)
    db =client.weibodata
    return db

def main():
    db = get_db()
    cookie = ''
    cookie = cookieget.LoginWeibo()
    print cookie
    dabaojiao.startscrpe(cookie=cookie, db=db)
    # Great_Barrier_Reef.startscrpe(cookie=cookie, db=db)
    # aierlihaitan.startscrpe(cookie=cookie, db=db)
    # Airlie_Beach.startscrpe(cookie=cookie, db=db)


if __name__ == '__main__':
    main()
