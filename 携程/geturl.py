# coding=utf-8
# python3

import urllib.request
import urllib.parse
import re
import time
import io
import gzip
import random

#页数范围
min = 1
max = 1097

headerS={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,en-US;q=0.7,en;q=0.3',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'mfw_uuid=5c84cb93-758a-762e-0127-ea70f6cb3e64; _r=bing; _rp=a%3A2%3A%7Bs%3A1%3A%22p%22%3Bs%3A12%3A%22cn.bing.com%2F%22%3Bs%3A1%3A%22t%22%3Bi%3A1552206739%3B%7D; oad_n=a%3A5%3A%7Bs%3A5%3A%22refer%22%3Bs%3A20%3A%22https%3A%2F%2Fcn.bing.com%2F%22%3Bs%3A2%3A%22hp%22%3Bs%3A11%3A%22cn.bing.com%22%3Bs%3A3%3A%22oid%22%3Bi%3A1029%3Bs%3A2%3A%22dm%22%3Bs%3A15%3A%22www.mafengwo.cn%22%3Bs%3A2%3A%22ft%22%3Bs%3A19%3A%222019-03-10+16%3A32%3A19%22%3B%7D; __mfwlv=1552358747; __mfwvn=3; __mfwlt=1552363839; uva=s%3A144%3A%22a%3A4%3A%7Bs%3A13%3A%22host_pre_time%22%3Bs%3A10%3A%222019-03-10%22%3Bs%3A2%3A%22lt%22%3Bi%3A1552206739%3Bs%3A10%3A%22last_refer%22%3Bs%3A20%3A%22https%3A%2F%2Fcn.bing.com%2F%22%3Bs%3A5%3A%22rhost%22%3Bs%3A11%3A%22cn.bing.com%22%3B%7D%22%3B; __mfwurd=a%3A3%3A%7Bs%3A6%3A%22f_time%22%3Bi%3A1552206739%3Bs%3A9%3A%22f_rdomain%22%3Bs%3A11%3A%22cn.bing.com%22%3Bs%3A6%3A%22f_host%22%3Bs%3A3%3A%22www%22%3B%7D; __mfwuuid=5c84cb93-758a-762e-0127-ea70f6cb3e64; UM_distinctid=16966bb483d45-0f494e03ad41f4-4c312f7f-144000-16966bb483e2ab; CNZZDATA30065558=cnzz_eid%3D1199525799-1552206059-null%26ntime%3D1552353780; PHPSESSID=madinq41vdjrvfvsk97bhp7cf0; all_ad=1',
'Host':'www.mafengwo.cn',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'
}
for i in range(min,max):
    try:
        url="http://www.mafengwo.cn/yj/10208/2-0-"+str(i)+".html"
        request = urllib.request.Request(url,data=None,headers=headerS)
        response = urllib.request.urlopen(request)
        page = response.read()
        iopage=io.BytesIO(page)
        depage = gzip.GzipFile(fileobj=iopage, mode="rb")
        #gzip解压缩
        html=depage.read().decode('utf-8')
        print(i)
        pattern = re.compile('/i/.*?.html', re.S)
        #查找其中形如/i/…….html的链接
        result = re.findall(pattern, html)
        print(result)
        with open("pages.txt", 'a') as file:
            for item in result[::2]:
                file.write(item+'\n')
        time.sleep(random.random()*3)
    except urllib.request.URLError as e:
        if hasattr(e, 'reason'):
            print('出错：' + str(e.reason))
        print('pass')