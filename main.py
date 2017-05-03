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
import os


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
    keywords = ['Great+Barrier+Reef', '大堡礁', 'Cairns', '凯恩斯', 'Townsville', '汤斯维尔', 'Cooktown', '库克镇', 'Daintree', '戴恩树', 'Mission+Beach', '使命海滩', 'Rockhampton',
                'Whitsunday+Islands', '圣灵岛', 'Hamilton+Island', '汉密尔顿岛', 'Lady+Musgrave+Island', 'Whitehaven+Beach', '白天堂沙滩',
                'Airlie+Beach', '艾尔利海滩', 'Coral', '珊瑚', 'Gold+Coast', '黄金海岸', 'Magnetic+Island', '磁岛',
                'Daydream+Island', '白日梦岛', 'Lady+Elliot+Island', '埃里奥特夫人岛', 'Heron+Island', 'Green+Island', '绿岛', 'Fitzroy+Island', '费兹罗岛']
    keywords2 = ['Great+Barrier+Reef']
    bday = 0
    path = os.getcwd()
    path += '\Diary.txt'

    if os.path.exists(path):
        print "Diary.txt exist"
        with open('Diary.txt', 'r') as f:
            bday = int(f.read())
            f.close()

    startup_time = datetime.datetime.now()
    flag_time = datetime.datetime.now()
    while(1):
        now_time = datetime.datetime.now()
        if (now_time.day - flag_time.day) == 2:
            flag_time = now_time + datetime.timedelta(days=-1)
            update_time = flag_time.strftime('%Y%m%d')
            print "更新昨天的微博数据：", update_time
            for keyword in keywords:
                keywordscrape.startscrape(cookie=cookie, db=db, keyword=keyword, starttime=update_time, endtime=update_time)

        yes_time = startup_time + datetime.timedelta(days=-bday)
        starttime = yes_time.strftime('%Y%m%d')
        bday += 1

        with open('Diary.txt', 'w') as f:
            f.write(str(bday))
            f.close()

        print "日期：", starttime
        for keyword in keywords2:
            keywordscrape.startscrape(cookie=cookie, db=db, keyword=keyword, starttime=starttime, endtime=starttime)


if __name__ == '__main__':
    main()
