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





def getuserurl(userurl, headers):
    time.sleep(6)
    request = urllib2.Request(userurl, headers=headers)
    html = urllib2.urlopen(request).read()
    info = re.findall('私信</a>&nbsp;<a href="(.*?)">资料</a>', html)
    url = 'http://weibo.cn/' + info[0]
    return url

def getuserinfo(userid, headers):
    time.sleep(6)
    userurl = 'http://weibo.cn/' + userid
    userurl = getuserurl(userurl=userurl, headers=headers)
    print userurl
    request = urllib2.Request(userurl, headers=headers)
    html = urllib2.urlopen(request).read()
    username = re.findall('昵称:(.*?)<br/>', html)
    usersex = re.findall('性别:(.*?)<br/>', html)
    userregion = re.findall('地区:(.*?)<br/>', html)
    userbri = re.findall('生日:(.*?)<br/>', html)
    if not username:
        userbri.append('NONE')
    if not usersex:
        userbri.append('NONE')
    if not userregion:
        userbri.append('NONE')
    if not userbri:
        userbri.append('NONE')
    print username[0], usersex[0], userregion[0], userbri[0]
    userinfo = {'username':username[0], 'usersex':usersex[0], 'userregion':userregion[0], 'userbri':userbri[0]}
    return userinfo


def download(keyword, starttime, endtime, cookievalue, cache):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'cookie': cookievalue}

    preurl = "http://weibo.cn/search/mblog?hideSearchFrame=&keyword=" + keyword + '&advancedfilter=1&hasori=1&starttime=' + starttime + '&endtime=' + endtime + '&sort=time&page='
    data = []
    trynum = 2
    i = 0

    while (1):
        try:
            if trynum == 0:
                break
            time.sleep(6)
            i += 1
            finallyurl = preurl + str(i)
            print '当前关键词为：' + keyword
            print "当前微博日期为:" + starttime + "   开始爬取第" + str(i) + "个网页："
            print finallyurl
            request = urllib2.Request(finallyurl, headers=headers)
            html = urllib2.urlopen(request).read()
            datas = []
            # datas = re.findall('<span class="ctt">:(.*?)</span>&nbsp;', html)
            buseridlist = []
            buseridlist = re.findall('<div><a class="nk" href="http://weibo.cn/(.*?)">', html)
            selector = etree.HTML(html)
            content = selector.xpath('//span[@class="ctt"]')
            for it in content:
                datas.append(unicode(it.xpath('string(.)')).replace('http://', ''))
            useridlist = []
            for item in buseridlist:
                if item[1] == '/':
                    useridlist.append(item[2:])
                else:
                    useridlist.append(item)
            # print 'userid lenght', len(userid)
            # print 'datas lenght', len(datas)

            if not datas:
                trynum -= 1
                continue
            for it in datas:
                userid = useridlist[datas.index(it)]
                userinfo = {}
                userinfo = getuserinfo(userid=userid, headers=headers)
                sub1 = re.compile("<.*?>")
                sub2 = re.compile("【.*?】")
                sub3 = re.compile("\d|、")
                it = sub1.sub('', it)
                it = sub2.sub('', it)
                it = sub3.sub('', it)
                # f.write(it)
                # f.write('\n')
                post = {'cotent': it, 'time': starttime, 'userinfo': userinfo}
                cache.insert(post)
                # f.write('this is a line')
                # f.write('\n')
                print "爬取完成"
        except urllib2.HTTPError:
            print "糟糕，账号被封！"
            exit()
        except:
            print "其他错误"
            trynum -= 1


def startscrape(cookie, db, keyword, starttime, endtime):
    my_collection = db['SinaWeiBoData']
    download(keyword=keyword, starttime=starttime, endtime=endtime, cookievalue=cookie, cache=my_collection)
