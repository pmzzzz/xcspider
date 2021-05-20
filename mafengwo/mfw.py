#!usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time     : 2021/2/5
# @Author   : Shufei Lei
# @Software : PyCharm
import hashlib
import requests
import execjs
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4144.2 Safari/537.36'
}


def encrypt(value, _mode):
    _hash = eval(f"hashlib.{_mode}(value.encode('utf-8')).hexdigest()")
    return _hash


def get_item(url):
    resp = session.get(url)
    print(resp.text)
    js_code = re.findall('\.(cookie=.+?);loc', resp.text)[0]
    x = execjs.eval(js_code)
    cookie = re.search('__jsl_clearance=(.*?);', execjs.eval(js_code)).group(1)
    session.cookies.update({'__jsl_clearance': cookie})

    resp2 = session.get(url)
    # print(resp2.text)
    xxx = re.search(r'go\(({"bts":.*?,"chars":".*?","ct":".*?","ha":".*?","tn":".*?","vt":".*?","wt":".*?"})\)', resp2.text)

    yyy = xxx.group(1)
    item = eval(re.search(r'go\(({"bts":.*?,"chars":".*?","ct":".*?","ha":".*?","tn":".*?","vt":".*?","wt":".*?"})\)', resp2.text).group(1))
    # print(item)
    return item


def get_cookie(url):
    item = get_item(url)
    ct = item['ct']
    bts = item['bts']
    chars = item['chars']
    hash_mode = item['ha']
    chars_length = len(chars)
    for i in range(chars_length):
        for j in range(chars_length):
            value = bts[0] + chars[i] + chars[j] + bts[1]
            ccc = encrypt(value,hash_mode)
            if encrypt(value, hash_mode) == ct:
                print('__jsl_clearance=' + value)
                return value


def get_html(url):
    global session
    session = requests.Session()
    session.headers = headers
    cookie = get_cookie(url)
    print(session.cookies)
    session.cookies.update({'__jsl_clearance': cookie})
    print(session.cookies)
    resp = session.get(url)
    html = resp.text
    # print(html)
    return html
 
#
def parse_html(html):
    print(html)


if __name__ == '__main__':

    url = 'http://www.mafengwo.cn/i/21452824.html'
    get_html(url)
    parse_html(get_html(url))