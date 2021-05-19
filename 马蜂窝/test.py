#!/usr/bin/env python
# coding:utf-8


import sys
import re


import requests
import execjs
from fake_useragent import UserAgent



class YiDaiYiLuSpider(object):
    """
    中国一带一路网（521反爬）
    """

    USER_AGENT = UserAgent()
    ua = USER_AGENT.random
    url = r'https://www.yidaiyilu.gov.cn/xwzx/gnxw/87373.htm'
    headers = {
        "Host": "www.yidaiyilu.gov.cn",
        "User-Agent": ua
    }

    @classmethod
    def get_text521(cls):
        """

        :return:
        """

        rs = requests.session()
        resp = rs.get(url=cls.url, headers=cls.headers)
        text_521 = ''.join(re.findall('<script>(.*?)</script>', resp.text))
        cookie_id = '; '.join(['='.join(item) for item in resp.cookies.items()])
        return cookie_id, text_521

    @classmethod
    def generate_cookies(cls, func):
        """

        :param func:
        :return:
        """

        func_return = func.replace('eval', 'return')
        content = execjs.compile(func_return)
        eval_func = content.call('f')
        var = str(eval_func.split('=')[0]).split(' ')[1]
        rex = r">(.*?)</a>"
        rex_var = re.findall(rex, eval_func)[0]
        mode_func = eval_func.replace('document.cookie=', 'return ').replace(';if((function(){try{return !!window.addEventListener;}', ''). \
            replace("catch(e){return false;}})()){document.addEventListener('DOMContentLoaded'," + var + ",false)}", ''). \
            replace("else{document.attachEvent('onreadystatechange'," + var + ")}", '').\
            replace(r"setTimeout('location.href=location.pathname+location.search.replace(/[\?|&]captcha-challenge/,\'\')',1500);", '').\
            replace('return return', 'return').\
            replace("document.createElement('div')", '"https://www.yidaiyilu.gov.cn/"').\
            replace(r"{0}.innerHTML='<a href=\'/\'>{1}</a>';{0}={0}.firstChild.href;".format(var, rex_var), '')

        content = execjs.compile(mode_func)
        cookies_js = content.call(var)
        __jsl_clearance = cookies_js.split(';')[0]
        return __jsl_clearance

    @classmethod
    def crawler(cls):
        """

        :return:
        """

        url = r'https://www.yidaiyilu.gov.cn/zchj/sbwj/87255.htm'
        cookie_id, text_521 = cls.get_text521()
        __jsl_clearance = cls.generate_cookies(text_521)
        cookies = "{0};{1};".format(cookie_id, __jsl_clearance)
        cls.headers["Cookie"] = cookies
        print(cls.headers)
        res = requests.get(url=url, headers=cls.headers)
        res.encoding = 'utf-8'
        print(res.text)


if __name__ == '__main__':

    YiDaiYiLuSpider.crawler()