# -*- coding: utf-8 -*-
import csv

import requests
from bs4 import BeautifulSoup
import re
import random
import time

url = 'https://you.ctrip.com/travels/chongqing158/3965033.html'
base_url = 'https://you.ctrip.com'
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
}

# 评论分隔符
SPLIT = 'y7qEE#Ri99'

def get_xc_detail(url: str) -> dict:
    """
    :param url: 文章地址
    :return:
    """
    # 初始化数据，未获取则为 -1
    userurl, pub_time, username, fallow, fans, title, style, texts, img_count, tianshu, shijian, renjun, heshui, wanfa, VisitCount, LikeCount, FavouriteCount, CommentCount, ShareCount = [
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    # 获取响应
    res = requests.get(url=url, headers=headers)
    # 解析内容
    soup = BeautifulSoup(res.text, 'html.parser')

    # 获取标题
    try:
        title = soup.title.string.split(' - ')[0]
    except:
        print('title')

    # 获取发布时间
    try:
        pub_time = soup.find_all('div', class_="time")[0].string
    except:
        # print(url)
        # print(soup.text)
        pub_time = re.findall(r'发表.*?(\d{4}-\d{2}-\d{2})', res.text)[0]
    # 获取文章类型
    try:
        ctd_head_left = soup.find_all('div', class_='ctd_head_left')[0]
        style = ctd_head_left.find_all('i')[0]['class'][0]
    except:
        print('style')
        pass

    # 获取文章信息--》天数、时间、人均、和谁、玩法
    try:
        ctd_content_controls = soup.find_all('div', class_='ctd_content_controls cf')[0]
        head = str(ctd_content_controls)
    except:
        pass
    print('head')
    # 天数
    try:
        tianshu = re.findall('<span><i class="days"></i>天数：(.*?)</span>', head)[0]
        # print(tianshu)
    except:
        print('天数')
        pass
    # 时间
    try:
        shijian = re.findall('<span><i class="times"></i>时间：(.*?)</span>', head)[0]
        # print(shijian)
    except:
        print('时间')
        pass
    # 人均
    try:
        renjun = re.findall('<span><i class="costs"></i>人均：(.*?)</span>', head)[0]
        # print(renjun)
    except:
        print('人均')
        pass
    # 和谁
    try:
        heshui = re.findall('<span><i class="whos"></i>和谁：(.*?)</span>', head)[0]
        # print(heshui)
    except:
        print('和谁')
        pass
    # 玩法
    try:
        wanfa = re.findall('<span><i class="plays"></i>玩法：(.*?)</span>', head)[0]
        # print(wanfa)
    except:
        print('玩法')
        pass

    # 获取带有富文本标签的正文
    ctd_content = soup.find_all('div', class_='ctd_content')[0]
    try:
        ctd_content_controls = soup.find_all('div', class_='ctd_content_controls cf')[0]
        # print(ctd_content_controls)
        ctd_content = str(ctd_content).replace(str(ctd_content_controls), '')
        texts = re.sub('<div class="ctd_content">.*?发表于.*?</h\d>|<div class="ctd_content">', '', str(ctd_content))
    except:
        # print(ctd_content)
        texts = re.sub('<div class="ctd_content">.*?发表于.*?</h\d>|<div class="ctd_content">', '', str(ctd_content))

    # 处理富文本标签,正文内容
    body = get_body(texts)

    # 统计图片数量
    try:
        # 定位正文标签
        ctd_content = soup.find_all('div', class_='ctd_content')[0]
        # 获取图片标签
        imgs = ctd_content.find_all('div', class_="img")
        # 获取图片数量
        img_count = len(imgs)
    except:
        pass

    # 统计互动数量
    try:
        VisitCount, FavouriteCount, LikeCount, CommentCount, ShareCount = get_hudong(int(url.split('/')[-1][:-5]))
    except:
        pass

    # 获取用户数据
    # try:
    member = soup.find_all('a', id='authorDisplayName')[0]
    # print(member)
    # a 标签分情况
    try:
        username = member['title']
    except:
        username = member.string
    userurl = base_url + member['href']
    fallow, fans = get_user_info(userurl)

    # 获取评论
    comments = get_comment(url)
    if comments:
        comments = SPLIT.join(comments)
    else:
        comments = ''


    # 构建数据
    data = {
        '文章标题': title,
        '发布时间': pub_time,
        'url': url,
        '用户名称': username,
        '用户主页': userurl,
        '关注': fallow,
        '粉丝': fans,
        '文章类型': style,
        '正文': body,
        '图片数量': img_count,
        '游玩天数': tianshu,
        '游玩时间': shijian,
        '人均消费': renjun,
        '和谁': heshui,
        '玩法': wanfa,
        '浏览量': VisitCount,
        '收藏量': FavouriteCount,
        '点赞数': LikeCount,
        '评论数': CommentCount,
        '分享数': ShareCount,
        '评论': comments
    }

    return data


def get_hudong(num: int):
    """
    获取互动信息
    :param num:文章id
    :return:
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
    }
    url = 'https://you.ctrip.com/TravelSite/Home/GetBusinessData'
    params = {
        'random': random.random(),
        'arList[0].RetCode': 0,
        'arList[0].Html': num,
        'arList[1].RetCode': 1,
        'arList[1].Html': num,
        'arList[2].RetCode': 2,
        'arList[2].Html': num,
        'arList[3].RetCode': 3,
        'arList[3].Html': 158,
    }
    res = requests.get(url=url, headers=headers, params=params)
    # 获取数据所在str
    Html = dict(res.json()[1])['Html']

    # print(Html, 'hhhhhhhhhhhhhhhhhhhh')

    # 初始化数据
    VisitCount, FavouriteCount, LikeCount, CommentCount, ShareCount = (-1, -1, -1, -1, -1)

    # 获取数据
    try:
        # 浏览量
        VisitCount = re.findall('"VisitCount":(\d*?),', Html)[0]
    except:
        pass
        # 收藏量
    try:
        FavouriteCount = re.findall('"FavouriteCount":(.*?),', Html)[0]
    except:
        pass
    # 点赞数
    try:
        LikeCount = re.findall('"LikeCount":(\d*?),', Html)[0]
    except:
        pass
    # 评论数
    try:
        CommentCount = re.findall('"CommentCount":(\d*?),', Html)[0]
    except:
        pass
    # 分享数
    try:
        ShareCount = re.findall('"ShareCount":(\d*?),', Html)[0]
    except:
        pass
    return VisitCount, FavouriteCount, LikeCount, CommentCount, ShareCount


def get_body(texts: str) -> str:
    # 去除图片
    x = re.sub(r'<p><div class="img".*?</a></div></p>', '', texts)
    # 去除<p><br/></p>
    y = re.sub(r'<p><br/></p>', '', x)
    # 去除<p><strong><br/></strong></p>
    z = re.sub(r'<p><strong><br/></strong></p>', '', y)
    # 去除 a标签
    a = re.sub(r'<a class="gs_a_poi.*?target="_blank">', '', z)
    a = re.sub(r'</a>|<a .*?>', '', a)
    # 去除其它富文本标签
    clear = re.sub(
        r'推荐住宿.*?\d{2}:\d{2}|发表于.*?\d{2}:\d{2}|<video.*?>.*?</video>|<p><strong>|</strong></p>|<p>|</p>|<br/>|<strong.*?>|</strong.*?>|\xa0|<span class="price">|<em>|</em>|<h\d class.*?>|</h\d>|<h\d>|<div class="img" data-likecategory="1".*?>|<div class="img_blk.*?</div>|</div>|<div .*?>|<img .*?>|<iframe .*?</iframe>',
        '', a)

    # clear = re.sub(r'<video.*?>.*? </video>','',clear)
    return clear


def get_user_info(userpage):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
    }
    res = requests.get(userpage, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    info = soup.find_all('div', class_="info-side")[0]
    aa = info.find_all('a')
    # print(aa)
    return int(aa[0].string), int(aa[1].string)


def get_comment(url):
    '''
    返回所有评论的列表
    :param url: 游记主页
    :return:
    '''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.62',
        'cookie': 'ASP.NET_SessionSvc=MTAuMTQuMjA2LjExNnw5MDkwfG91eWFuZ3xkZWZhdWx0fDE2MTYwNjIzMjcxMDE; _RSG=4JqGnD5Rjj12ku4cENTvs9; _RDG=28742dd98685862ee10dc595c4bff445a5; _RGUID=1b6d6c53-7143-44c4-9db9-7573a6138b82; _ga=GA1.2.498492006.1621307965; _gid=GA1.2.595663286.1621307965; MKT_Pagesource=PC; _RF1=14.106.97.51; MKT_CKID=1621319297460.5220p.4nxp; MKT_CKID_LMT=1621319297461; Session=smartlinkcode=U130727&smartlinklanguage=zh&SmartLinkKeyWord=&SmartLinkQuary=&SmartLinkHost=; Union=AllianceID=4902&SID=130727&OUID=&createtime=1621325424&Expires=1621930224400; appFloatCnt=40; _bfa=1.1621304906781.390si2.1.1621325338916.1621334756177.5.64; _bfs=1.4; _jzqco=%7C%7C%7C%7C1621319297651%7C1.1547692190.1621319297488.1621334963847.1621336439769.1621334963847.1621336439769.undefined.0.0.57.57; __zpspc=9.3.1621334759.1621336439.4%234%7C%7C%7C%7C%7C%23; _bfi=p1%3D0%26p2%3D0%26v1%3D64%26v2%3D63',
    }

    comments = []
    TravelId = url.split('/')[-1][:-5]
    comment_url = 'https://you.ctrip.com/TravelSite/Home/TravelReplyListHtml'
    MAX_PAGE = 100
    i = 1
    while(i<MAX_PAGE):
        time.sleep(random.random()*4)
        params = {
            'TravelId': TravelId,
            'IsReplyRefresh': 0,
            'ReplyPageNo': i,
            'ReplyPageSize': 10,
            '_': 1621334974243,
        }
        try:
            res = dict(requests.get(url=comment_url, headers=headers, params=params).json())
            text = res['Html']
            if text:
                soup = BeautifulSoup(text, 'html.parser')
                comments_one_page = [i.string.strip().replace('\xa0','') for i in soup.find_all('p', class_="ctd_comments_text")]
                comments.extend(comments_one_page)
                i += 1
            else:
                break
        except:
            break
    print(comments)
    return comments

    # params = {
    #     'TravelId': TravelId,
    #     'IsReplyRefresh': 0,
    #     'ReplyPageNo': 100,
    #     'ReplyPageSize': 10,
    #     '_': 1621334974243,
    # }
    # res = dict(requests.get(url=comment_url,headers=headers,params=params).json())
    # text = res['Html']
    # soup = BeautifulSoup(text,'html.parser')
    # comments_one_page = [i.string for i in soup.find_all('p',class_="ctd_comments_text")]
    # comments.extend(comments_one_page)
    # print(text)
    # return comments


if __name__ == '__main__':
    with open('xc_urls_最新.txt', 'r') as f:
        urls = list(map(lambda x: x.strip(), f.readlines()[:5000]))
    print(urls)

    csv_head = ['文章标题', '发布时间', 'url', '用户名称', '用户主页', '关注', '粉丝', '文章类型', '正文', '图片数量', '游玩天数', '游玩时间', '人均消费', '和谁',
                '玩法', '浏览量',
                '收藏量', '点赞数', '分享数',
                '评论数','评论']
    with open('携程.csv', 'a', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=csv_head)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
        writer.writeheader()  # 写入列名
        j = 0
        for i in urls[:100]:
            time.sleep(random.random() * 3)

            print('--' * 40)
            data = get_xc_detail(base_url + i)
            print(i)
            print(f'当前爬到第-{j}-个了')
            j += 1
            print(data)
            print('*' * 80)
            writer.writerows([data])  # 写入数据

    # get_comment('https://you.ctrip.com/travels/chongqing158/3967831.html')
