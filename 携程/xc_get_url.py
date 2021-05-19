import time

import requests
from bs4 import BeautifulSoup
import random
# 第一页url
base_url = 'https://you.ctrip.com/travels/chongqing158.html'
# 请求头
headerS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
    'referer': base_url,
}
# 获取第一页url
res = requests.get(url=base_url, headers=headerS)
print(res.text)
soup = BeautifulSoup(res.text, 'html.parser')
aaa = soup.find_all('a', class_="journal-item cf")
# 写入文件-->清空文件重新写入
with open('xc_urls_最新.txt', 'w') as f:
    for i in aaa:
        print(i['href'])
        f.write(i['href'] + '\n')


def get(url):
    """
    获取有页码的url列表
    :param url:
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
        'referer': url,
    }
    res = requests.get(url=url, headers=headers)
    print(res.status_code)
    soup = BeautifulSoup(res.text, 'html.parser')
    aaa = soup.find_all('a', class_="journal-item cf")
    with open('xc_urls_最新.txt', 'a') as f:
        for i in aaa:
            print(i['href'])
            f.write(i['href'] + '\n')

MAX_PAGE = 501

if __name__ == '__main__':
    for i in range(2, MAX_PAGE + 1):
        print('当前第-{}-页'.format(i))
        url = 'https://you.ctrip.com/travels/chongqing158/t2-p{}.html'.format(i)
        get(url)
        time.sleep(random.random()*3)
    # print(random.random()*3)
