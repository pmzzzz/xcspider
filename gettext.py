# coding=utf-8
# author=zhangjingyuan
# python3
from html.parser import HTMLParser
import lxml
import requests
from lxml import etree
import urllib.request
import urllib.parse
import re
import time
import io
import gzip
import random
import codecs

from bs4 import BeautifulSoup
#
# min = 50
# max = 500

headerS={
# 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
# 'Cache-Control':'max-age=0',
# 'Cache-Control': 'no-cache',
# 'Connection':'keep-alive',
'Cookie':'PHPSESSID=no8cfndeh0c9em1l6kcj0th7n6; mfw_uuid=60a32a48-f89b-c07d-e2ef-687fc39404d1; oad_n=a%3A3%3A%7Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222021-05-18+10%3A45%3A28%22%3B%7D; __jsluid_h=21ef339d6f7e54e7971273d1ad3d4fe2; __omc_chl=; __mfwa=1621305929740.66696.1.1621305929740.1621305929740; __mfwlv=1621305929; __mfwvn=1; uva=s%3A78%3A%22a%3A3%3A%7Bs%3A2%3A%22lt%22%3Bi%3A1621305929%3Bs%3A10%3A%22last_refer%22%3Bs%3A6%3A%22direct%22%3Bs%3A5%3A%22rhost%22%3Bs%3A0%3A%22%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1621305929%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A0%3A%22%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=60a32a48-f89b-c07d-e2ef-687fc39404d1; UM_distinctid=1797d5d315df8-0f9cf6df7fb218-7e697a60-1fa400-1797d5d315e9fd; CNZZDATA30065558=cnzz_eid%3D1225936449-1621304750-%26ntime%3D1621304750; bottom_ad_status=0; __jsl_clearance=1621306003.897|0|ICBJ4vfvd%2B6tf7bC9BAMe25sxuA%3D; c=v97wCVbO-1621307043651-75adb11ece3d8-839299655; TDpx=112; __mfwothchid=referrer%7Copen.weixin.qq.com; __mfwc=referrer%7Copen.weixin.qq.com; Hm_lvt_8288b2ed37e5bc9b4c9f7008798d2de0=1621305930,1621307061; __omc_r=; _fmdata=ovAVjnzC3sFQttVr8XEdyTmlLm9SM6qlMuZ9VrXN9xpVCn6rJj8Rr6U3SBs53VHIYY5Jc6VDC%2B%2BaHFn%2FrbYllTcc1fBS9emjymXAr8%2FZsf4%3D; _xid=cA8pXdKl5Rwr%2Fg%2B%2B%2BE73ahMvmveu3MmBhu7HSkxIE7FuPgL%2BndV8cV%2Fk%2FRd4c85QpRtP1nKISkAZF%2F8Qahmp4g%3D%3D; login=mafengwo; mafengwo=ad7bfd5401e5a03bfefcf5e9befa9b7d_57600275_60a32f3779a030.12792043_60a32f3779a0b3.27210905; uol_throttle=57600275; mfw_uid=57600275; __mfwb=96a6da8afc5b.18.direct; __mfwlt=1621307200; Hm_lpvt_8288b2ed37e5bc9b4c9f7008798d2de0=1621307201',
'Host':'www.mafengwo.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
'Referer': 'http://www.mafengwo.cn/i/21275650.html'
}
#
# headerS={
# 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
# 'Accept-Encoding':'gzip, deflate',
# 'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
# 'Cache-Control':'max-age=0',
# 'Connection':'keep-alive',
# 'Cookie':'mfw_uuid=5c84cb93-758a-762e-0127-ea70f6cb3e64; _r=bing; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A12%3A%22cn.bing.com%2F%22%3Bs%3A1%3A%22t%22%3Bi%3A1552206739%3B%7D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A20%3A%22https%3A%2F%2Fcn.bing.com%2F%22%3Bs%3A2%3A%22hp%22%3Bs%3A11%3A%22cn.bing.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-03-10+16%3A32%3A19%22%3B%7D; __mfwlv=1552358747; __mfwvn=3; __mfwlt=1552363839; uva=s%3A144%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222019-03-10%22%3Bs%3A2%3A%22lt%22%3Bi%3A1552206739%3Bs%3A10%3A%22last_refer%22%3Bs%3A20%3A%22https%3A%2F%2Fcn.bing.com%2F%22%3Bs%3A5%3A%22rhost%22%3Bs%3A11%3A%22cn.bing.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1552206739%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A11%3A%22cn.bing.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5c84cb93-758a-762e-0127-ea70f6cb3e64; UM_distinctid=16966bb483d45-0f494e03ad41f4-4c312f7f-144000-16966bb483e2ab; CNZZDATA30065558=cnzz_eid%3D1199525799-1552206059-null%26ntime%3D1552353780; PHPSESSID=madinq41vdjrvfvsk97bhp7cf0; all_ad=1',
# 'Host':'www.mafengwo.cn',
# 'Upgrade-Insecure-Requests':'1',
# 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
#
# }
list=open(".//pages.txt",'r')
file=codecs.open(".//rsult.csv",'a','utf-8')

line  = list.readlines()[1]
content=""
print(line)
url="http://www.mafengwo.cn"+line
print(url)
# request = urllib.request.Request(url,data=None,headers=headerS)
# response = urllib.request.urlopen(request)
# page = response.read()
#
#
#
# # iopage=io.BytesIO(page)
# # depage = gzip.GzipFile(fileobj=iopage, mode="rb")
# # html=depage.read().decode('utf-8')
#
html = requests.get(url=url,headers=headerS).content.decode('utf8')
print(html)
# soup = BeautifulSoup(html,'html.parser')
# print(soup)
# # print(html)
# Htree = etree.HTML(html)
# print(etree.tostring(Htree))
#
# body=Htree[1]
# print(etree.tostring(body))
# # main=body[1]
#
# main = Htree.xpath('/html/body/div[2]')
# print(etree.tostring(main[0]))
# print(etree.tostring(main))
# view=main[3]
#此处使用etree以获取游记正文部分
# content = content + etree.tostring(view).decode('utf-8')
# content=HTMLParser().unescape(content)
m = soup.find_all('div',class_='main')





print(m)
dr = re.compile(r'<[^>]+>', re.S)

dd = dr.sub('', content)

dr = re.compile('\n', re.S)

dd = dr.sub('', dd)

dr = re.compile(' ', re.S)

res = dr.sub('', dd)
#去除富文本标签、换行符、空格等
print(res)
file.write(str(res)+'\n')

file.close()
