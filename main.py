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
import keywordscrape



def get_db():
    client = MongoClient('localhost', 27017)
    db =client.SinaWeiBoDB
    return db

def main():
    db = get_db()
    username = ''
    password = ''
    cookie = ''
    cookie = cookieget.LoginWeibo(username=username, password=password)
    keywords = ['Cairns', '凯恩斯', 'Townsville', '汤斯维尔', 'Cooktown', '库克镇', 'Daintree', '戴恩树', 'Mission+Beach', '使命海滩', 'Rockhampton',
                'Whitsunday+Islands', '圣灵岛', 'Hamilton+Island', '汉密尔顿岛', 'Lady+Musgrave+Island', 'Whitehaven+Beach', '白天堂沙滩',
                'Airlie+Beach', '艾尔利海滩', 'Great+Barrier+Reef', '大堡礁', 'Coral', '珊瑚', 'Gold+Coast', '黄金海岸', 'Magnetic+Island', '磁岛',
                'Daydream+Island', '白日梦岛', 'Lady+Elliot+Island', '埃里奥特夫人岛', 'Heron+Island', 'Green+Island', '绿岛', 'Fitzroy+Island', '费兹罗岛']
    bday = 0
    while(1):
        now_time = datetime.datetime.now()
        yes_time = now_time + datetime.timedelta(days=-bday)
        yes_time = yes_time.strftime('%Y%m%d')
        starttime = endtime = yes_time

        print "日期：", yes_time
        for keyword in keywords:
            keywordscrape.startscrape(cookie=cookie, db=db, keyword=keyword, starttime=yes_time, endtime=yes_time)
        bday += 1



if __name__ == '__main__':
    main()
