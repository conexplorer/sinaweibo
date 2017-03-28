
import datetime
import urllib2

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'cookie': '_T_WM=90347fdd3f00b6a129cac368d985aab2; ALF=1493037479; SCF=Ata3E7hSqS6TCs8OPT5h_D9ZdI89qgpqPjGJzZ1M1SLiN8b0yGD8HDjJ_sV_h9tsrgitEYPJyAJRf5qF8uX3jGA.; SUB=_2A2510hT6DeRxGeNO41MY8ynPwj2IHXVXPLyyrDV6PUJbktAKLVTjkW2dQBelKG8b7mMzxeESt_c7wJVc6A..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5_rDkDu3miHaUUWzjQQwMI5JpX5o2p5NHD95Qfehnp1KeNe0.pWs4Dqcjdi--fiKnRiK.Ri--fi-zRiKnfPX9DdJxSdNiL; SUHB=079jd6jHY-GvGc; SSOLoginState=1490445482'}

headers2 = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'cookie': 'SUB=_2A2510horDeRxGeNJ61cW8C3EzD6IHXVXPKZjrDV9PUJbkdANLU3VkW0b8GULdz3kEIF1sVk9Kq-LC6OmGA..;SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF_uZjn44-uOD5e632C0x1G5NHD95QfS05fS0501hME;ustat=__120.194.3.186_1490446971_0.43475500;genTime=1490446971;PHPSESSID=9c28a18aed628af8d272e6b89163c6a3;historyRecord={"href":"http://my.sina.cn/?vt=4&pos=108&m=5d8e26c4c5cfd2c3722073a0399f8db5","refer":""};sina_ucode=YcaYcaMIcX;SINAGLOBAL=;Apache=9328530565486.77.1490446974249;ULV=1490446974249:1:1:1:9328530565486.77.1490446974249:;'}
try:
        finallyurl = 'http://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%A4%A7%E5%A0%A1%E7%A4%81&advancedfilter=1&hasori=1&starttime=20170317&endtime=20170317&sort=time&page=1'
        request = urllib2.Request(finallyurl, headers=headers2)
        html = urllib2.urlopen(request).read()
        print htm
except urllib2.HTTPError:
        print "httperror"
        exit()
except:
        print "others error"