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
import sys
reload(sys)
sys.setdefaultencoding('utf8')




def get_userurl(userurl, headers):
    time.sleep(6)
    request = urllib2.Request(userurl, headers=headers)
    html = urllib2.urlopen(request).read()
    info = re.findall('私信</a>&nbsp;<a href="(.*?)">资料</a>', html)
    url = 'http://weibo.cn' + info[0]
    return url

def get_userinfo(userid, headers):
    time.sleep(6)
    userurl = 'http://weibo.cn/' + userid
    if str.isalpha(userid[0]):
        userurl = get_userurl(userurl=userurl, headers=headers)
    else:
        userurl += '/info'
    print userurl

    request = urllib2.Request(userurl, headers=headers)
    html = urllib2.urlopen(request).read()

    username = re.findall('昵称:(.*?)<br/>', html)
    usersex = re.findall('性别:(.*?)<br/>', html)
    userregion = re.findall('地区:(.*?)<br/>', html)
    userbri = re.findall('生日:(.*?)<br/>', html)

    if not username:
        print "用户url构建错误，重新构建："
        userurl = 'http://weibo.cn/' + userid
        userurl = get_userurl(userurl=userurl, headers=headers)
        print userurl
        request = urllib2.Request(userurl, headers=headers)
        html = urllib2.urlopen(request).read()
        username = re.findall('昵称:(.*?)<br/>', html)
        usersex = re.findall('性别:(.*?)<br/>', html)
        userregion = re.findall('地区:(.*?)<br/>', html)
        userbri = re.findall('生日:(.*?)<br/>', html)
    if not username:
        username.append('NONE')
    if not usersex:
        usersex.append('NONE')
    if not userregion:
        userregion.append('NONE')
    if not userbri:
        userbri.append('NONE')

    print username[0], usersex[0], userregion[0], userbri[0]
    userinfo = {'name': username[0], 'gender': usersex[0], 'location': userregion[0], 'birthdate': userbri[0]}
    return userinfo

def get_text(html):
    datas = []
    selector = etree.HTML(html)
    content = selector.xpath('//span[@class="ctt"]')
    for it in content:
        datas.append(unicode(it.xpath('string(.)')).replace('http://', ''))
    return datas

def get_time(html, starttime):
    now_time = datetime.datetime.now()
    btimes = []
    times = []
    selector = etree.HTML(html)
    bbtime = selector.xpath('//span[@class="ct"]')
    for it in bbtime:
        btimes.append(unicode(it.xpath('string(.)')).replace('http://', ''))
    for it in btimes:
        if '分钟' in it:
            num = re.findall('\d+', it)[0]
            yes_time = now_time + datetime.timedelta(minutes=-int(num))
            yes_time = yes_time.strftime('%Y-%m-%d %H:%M')
            print yes_time
        else:
            if '今天' in it:
                rtime = starttime[0:4] + '-' + starttime[4:6] + '-' + starttime[-2:] + ' ' + it[3:8]
                times.append(rtime)
            else:
                rtime = starttime[0:4] + '-' + starttime[4:6] + '-' + starttime[-2:] + ' ' + it[7:12]
                times.append(rtime)
    return times

def get_idlist(html):
    buseridlist = re.findall('<div><a class="nk" href="http://weibo.cn/(.*?)">', html)
    return buseridlist

def get_transpond_like_comment(html):
    transponds = re.findall('>转发\[(.*?)]</a>', html)
    likes = re.findall('>赞\[(.*?)\]</a>', html)
    comments = re.findall('>评论\[(.*?)\]</a>', html)
    return transponds, likes, comments


def get_comments(url, headers):
    time.sleep(6)
    datas = []
    url += str(1)
    print "    当前评论网页：", url
    request = urllib2.Request(url, headers=headers)
    html = urllib2.urlopen(request).read()
    try:
        totalpage = re.findall('<input name="mp" type="hidden" value="(.*?)" />', html)[0]
    except:
        totalpage = '1'
    print "    评论总页数：", totalpage
    selector = etree.HTML(html)
    content = selector.xpath('//span[@class="ctt"]')
    for it in content:
        if content.index(it) == 0:
            continue
        datas.append(unicode(it.xpath('string(.)')))
    for item in range(2, int(totalpage) + 1):
        url += str(item)
        print "    当前评论网页：", url
        request = urllib2.Request(url, headers=headers)
        html = urllib2.urlopen(request).read()
        selector = etree.HTML(html)
        content = selector.xpath('//span[@class="ctt"]')
        for it in content:
            datas.append(unicode(it.xpath('string(.)')))
    return datas

def get_comments_urllist(html):
    comments_urllist = []
    bcomments_urllist = re.findall('<a href="http://weibo.cn/comment/(.*?)#cmtfrm" class="cc">评论', html)
    for it in bcomments_urllist:
        comments_urllist.append('https://weibo.cn/comment/' + it + '&page=')
    return comments_urllist


def get_islocation(html):
    locations = []
    selector = etree.HTML(html)
    location = selector.xpath('//div[@class="c"]/div/a[1]')

    for it in location:
        locations.append(unicode(it.xpath('string(.)')))
    return locations


def download(keyword, starttime, endtime, cookievalue, cache):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'cookie': cookievalue}

    preurl = "http://weibo.cn/search/mblog?hideSearchFrame=&keyword=" + keyword + '&advancedfilter=1&hasori=1&starttime=' + starttime + '&endtime=' + endtime + '&sort=time&page='
    data = []
    trynum = 1
    webpagenum = 0
    while (1):
        try:
            if trynum == 0:
                break
            time.sleep(6)
            webpagenum += 1
            finallyurl = preurl + str(webpagenum)
            print '当前关键词为：' + keyword
            print "当前微博日期为:" + starttime + "   开始爬取第" + str(webpagenum) + "个网页："
            print finallyurl

            request = urllib2.Request(finallyurl, headers=headers)
            html = urllib2.urlopen(request).read()

            datas = get_text(html=html)
            buseridlist = get_idlist(html=html)
            transponds, likes, comments_counts = get_transpond_like_comment(html=html)
            times = get_time(html=html, starttime=starttime)
            comments_urlist = get_comments_urllist(html=html)
            islocations = get_islocation(html=html)
            if not datas:
                trynum -= 1
                continue

            useridlist = []
            for item in buseridlist:
                if item[1] == '/':
                    useridlist.append(item[2:])
                else:
                    useridlist.append(item)
            i = 0
            for text in datas:
                userid = useridlist[i]
                transpond = transponds[i]
                like = likes[i]
                comments_count = comments_counts[i]
                time1 = times[i]
                userinfo = get_userinfo(userid=userid, headers=headers)
                if comments_count != '0':
                    print "    开始爬取评论"
                    comments = get_comments(url=comments_urlist[datas.index(text)], headers=headers)
                    print "    评论爬取完成"
                else:
                    comments = 'NONE'

                if islocations[i] == '显示地图':
                    location = text.split(' ')[-2]
                else:
                    location = 'NONE'
                try:
                    post = {'text': text, 'reposts_count': transpond, 'likes_count': like, 'comments_count': comments_count, 'comments': comments, 'location': location, 'date': time1, 'userinfo': userinfo}
                    cache.insert(post)
                except:
                    print "导入数据库出错，请检查数据库是否开启"
                print "爬取完成"
                i += 1
        except urllib2.HTTPError:
            print "糟糕，账号被封！"
            exit()
        except:
            print "其他错误"
            trynum -= 1


def startscrape(cookie, db, keyword, starttime, endtime):
    my_collection = db['SinaWeiBoData']
    download(keyword=keyword, starttime=starttime, endtime=endtime, cookievalue=cookie, cache=my_collection)
