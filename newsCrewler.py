# -*- coding:UTF-8 -*-

'''
Created on 2016-10-11
在网页上抓取目标url的目标网页信息
@author: luoxaing
'''

import requests
import re
import json
import sys
import datetime
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')


#获取评论数
def getCommentCounts(newsURL, commentURL):
    m = re.search('doc-i(.+).shtml', newsURL)
    newsID = m.group(1)
    res = requests.get(commentURL.format(newsID))
    jd = json.loads(res.text.strip('var data='))
    commentCount = jd['result']['count']['total']
    return commentCount


def getNewsDetail(newsURL):
    result = {}
    res = requests.get(newsURL)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    result['title'] = soup.select('#artibodyTitle')[0].text.strip()
    time = soup.select('.time-source')[0].contents[0].strip()
    result['dt'] = datetime.datetime.strptime(time, '%Y年%m月%d日%H:%M')
    result['newsSource'] = soup.select('.time-source span a')[0].text
    result['newsSourceURL'] = soup.select('.time-source span a')[0]['href']
    result['article'] = '\n'.join([p.text.strip() for p in soup.select('#artibody p')[:-1]])
    result['editor'] = soup.select('.article-editor')[0].text.strip('责任编辑：')
    result['commentCount'] = getCommentCounts(newsURL, commentURL)
    return result

if __name__ == '__main__':
    newsURL = 'http://news.sina.com.cn/c/nd/2016-09-30/doc-ifxwkzyh3944561.shtml'
    commentURL = 'http://comment5.news.sina.com.cn/page/info?version=1&format=js' \
                 '&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-8' \
                 '&page=1&page_size=20'
    allDetail = getNewsDetail(newsURL)
    print '新闻标题：', allDetail['title']
    print '评论数：', allDetail['commentCount']
    print '新闻时间：', allDetail['dt']
    print '新闻来源：', allDetail['newsSource'], allDetail['newsSourceURL']
    print '新闻编辑者：', allDetail['editor']
    print '新闻内容：'
    print allDetail['article']