# -*- coding: utf-8 -*-
from configparser import ConfigParser
from urllib.parse import quote
import socket
import os
import math
import urllib.request
from bs4 import BeautifulSoup
import time
import requests
import lxml
import json
import re


# https://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&filename=JJYJ201412008

doi_file = open('doi_list.txt', 'w')
file = open('article_info_json.txt', 'w')

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'www.cnki.net',
    'Referer':'http://search.cnki.net/search.aspx?q=%E4%BD%9C%E8%80%85%E5%8D%95%E4%BD%8D%3a%E6%AD%A6%E6%B1%89%E5%A4%A7%E5%AD%A6&rank=relevant&cluster=zyk&val=CDFDTOTAL',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}


def deal_with_detailed_page(href):

    # https://www.cnki.com.cn/Article/CJFDTOTAL-GLSJ201907008.htm
    if re.match(r'^(//www.cnki.com.cn/Article/CJFDTOTAL)-\w{4}(\w*)', href):
        year = href[-13:-9]
        name = href[-17:-4]
        # 含关键词的详情页链接
        paper_url = "http://kns.cnki.net/KCMS/detail/detail.aspx?dbcode=CJFQ&dbname=CJFDLAST" + year + "&filename=" + name
        try:

            html = requests.get(paper_url, headers=headers, timeout=500)
            soup = BeautifulSoup(html.text, 'html.parser')

            doi = soup.select('body > div.wrapper > div.main > div.container > div > div > div > ul > li:nth-child(1) > p')
            doi_text = doi[0].get_text()
            if doi_text[0].isdigit():
                print("get doi_txt info: " + doi_text)
                doi_file.writelines(doi_text+'\n')

        except Exception as e:
            print("No result,reason: " + str(e))

def deal_artile_list_page(keyword):

    if os.path.exists('article_info.txt'):
        print('存在输出文件，删除该文件')
        os.remove('article_info.txt')

    search_url = 'https://search.cnki.com.cn/Search/Result'

    full_json_dict={}


    for page in range(100):


        query_data = {'searchType': 'MulityTermsSearch',
                    'Content': keyword,
                    'Page':page,  # 第几页
                    'ArticleType':1 # 期刊
                    }
        r = requests.post(search_url, data=query_data)
        #获取最大页数
        soup = BeautifulSoup(r.content, 'lxml')
        list_items = soup.find(name='div',attrs={'id':'article_result'}).find_all(name='div',attrs={'class':'list-item'})
        idx = 0
        for artile in list_items:
            p = artile.find_all(name='p',attrs={'class':'tit clearfix'})[0]
            url = p.find_all(name='a')[0]
            href = url.get('href')
            title = url.get('title')

            artile_json = {}
            artile_json['href'] = href
            artile_json['title'] = title
            print("article info：### " + str(artile_json))
            full_json_dict[idx] = json.dumps(artile_json)
            idx += 1
            deal_with_detailed_page(href)
            # full_json_dict(artile_json)
    file.writelines(json.dumps(full_json_dict))
    # with open('article_info.txt','w') as f:
    #     json.dump(full_json_dict, f)
    #     print("加载入文件完成...")

def search_allsorts_article():

    keywords_file = open('keywords','r')
    for keyword in keywords_file.readlines():
        full_keyword = keyword.strip('\n')
        deal_artile_list_page(full_keyword)


if __name__ == '__main__':



    # test_url = 'https://www.cnki.com.cn/Article/CJFDTOTAL-GLSJ201907008.htm'
    # deal_with_detailed_page(test_url)

    # deal_artile_list_page()
    search_allsorts_article()