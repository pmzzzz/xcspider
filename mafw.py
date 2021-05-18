import os
import time
import random

# import pymysql
import requests
from lxml import etree
import pandas as pd
# from sqlalchemy import create_engine


def page(url):
    # ua伪装
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62'}

    response = requests.get(url=url, headers=headers)
    page_text = response.text
    return page_text


def notes_detail(city_id):

    note_id = 1
    # 新建空dataframe用来存放爬到的数据
    note_detail_dataframe = pd.DataFrame([], columns=['id', 'title', 'user_name', 'date', 'read_number', 'decision'])

    url = 'http://www.mafengwo.cn/yj/%s/'
    url_1 = format(url % city_id)
    url_2 = url_1 + 's-0-0-%s'
    for i in range(1, 5):
        url_3 = format(url_2 % str(i))
        # 第一页
        url_4 = url_3 + '-0-1-0.html'
        page_text = page(url_4)
        tree = etree.HTML(page_text)
        # 页数
        page_number = int(tree.xpath('//div[@class="_pagebar"]/div/span[1]/span[1]/text()')[0])
        for num in range(1, page_number + 1):
            url_5 = url_3 + '-0-%s-0.html'
            url_6 = format(url_5 % str(num))
            page_ = page(url_6)
            tree_ = etree.HTML(page_)
            li_list = tree_.xpath('//div[@class="_notelist"]/div/ul/li')
            for li in li_list:
                try:
                    title = li.xpath('.//a[@class="title-link"]/text()')[0]
                    user_name = li.xpath('./div[3]/span/a[2]/text()')[0]
                    date_ = li.xpath('./div[3]/span[2]/span/text()')[0]
                    date = "20" + date_
                    read_number = li.xpath('./span/text()[1]')[0]
                    decision = li.xpath('./span/text()[2]')[0]
                except Exception as e:
                    print(e)
                    break

                note_detail_dataframe.loc[note_id - 1, 'id'] = note_id
                note_detail_dataframe.loc[note_id - 1, 'title'] = title
                note_detail_dataframe.loc[note_id - 1, 'user_name'] = user_name
                note_detail_dataframe.loc[note_id - 1, 'date'] = date
                note_detail_dataframe.loc[note_id - 1, 'read_number'] = read_number
                note_detail_dataframe.loc[note_id - 1, 'decision'] = decision
                note_id += 1
                print(note_id, title, user_name, date, read_number, decision)

            # 随机生成0.2-1秒的一位小数
            random_sleep_time = float(round(random.uniform(0.2, 1.0), 1))
            # 休眠随机数秒
            time.sleep(random_sleep_time)
            # 只爬前三页
            if num == 3:
                break
        # 随机生成0.2-1秒的一位小数
        random_sleep_time = float(round(random.uniform(0.2, 1.0), 1))
        # 休眠随机数秒
        time.sleep(random_sleep_time)

    if city_id == '10065':
        check_csv("beijing")
        note_detail_dataframe.set_index('id', inplace=True)
        note_detail_dataframe.to_csv('./CSV/beijing.csv')
    elif city_id == '10099':
        check_csv("shanghai")
        note_detail_dataframe.set_index('id', inplace=True)
        note_detail_dataframe.to_csv('./CSV/shanghai.csv')
    elif city_id == '10208':
        check_csv("chongqing")
        note_detail_dataframe.set_index('id', inplace=True)
        note_detail_dataframe.to_csv('./CSV/chongqing.csv')
    else:
        check_csv("tianjin")
        note_detail_dataframe.set_index('id', inplace=True)
        note_detail_dataframe.to_csv('./CSV/tianjin.csv')

# 检查csv文件是否存在
def check_csv(csv_name):
    path = './CSV'
    file = path + '/' + csv_name + '.csv'
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(file):
        # os.mknod(file)
        f = open(file, 'w')
        f.close()

def beijing_detail():
    city_id_list = ['10065', '10099', '10208', '10320']
    city_id = city_id_list[0]
    notes_detail(city_id)


def shanghai_detail():
    city_id = '10099'
    notes_detail(city_id)


def chongqing_detail():
    city_id = '10208'
    notes_detail(city_id)


def tianjin_detail():
    city_id = '10320'
    notes_detail(city_id)


if __name__ == '__main__':
    # chongqing_detail()

    print(page('http://www.mafengwo.cn/i/17150068.html'))
