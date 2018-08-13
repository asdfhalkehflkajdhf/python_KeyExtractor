# coding: utf-8

import requests
from bs4 import BeautifulSoup as soup
import time
import os

'''
南方周末网站的文章抽取，构建关键词、标签抽取的测试集合
'''


def extract_time(url):
    '''
    只进行页面内容提取，不进行链接采集
    南方周末的抽取：例如：http://www.infzm.com/content/117747
    '''
    headers = {'User-Agent': "BingBot (Bing's spider)"}
    response = requests.get(url, headers=headers)
    doc = soup(response.text, 'html5lib')
    try:
        content = doc.select("em[class=pubTime]")[0].text.strip().split()[0]
    except:
        print(url)
        content = "0000-00-00"

    return content


'''add_option用来加入选项，action是有store，store_true，store_false等，dest是存储的变量，default是缺省值，help是帮助提示
store 也有其它的两种形式： store_true 和 store_false 
'''
if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-u', '--url', dest='test_url', help='url to fetch time', default='http://www.infzm.com/content/102003')

    parser.add_option('--link-file', dest='link_file', help='file read url link', default="links.txt")
    parser.add_option('--out-file', dest='out_file', help='file to store time list', default="link_time.csv")

    (options, args) = parser.parse_args()
    print(options)

    if options.link_file and os.path.exists(options.link_file):
        # 读取文件url
        in_f = open(options.link_file, 'r', encoding='utf8')
        out_f = open(options.out_file, 'w', encoding='utf8')
        for url in in_f.readlines():
            articles_time = extract_time(url.strip())
            print(articles_time, file=out_f, flush=True)
        out_f.close()
        in_f.close()

    if options.test_url:
        url = options.test_url  # 'http://www.infzm.com/content/117747'
        articles_time = extract_time(url)
        print(articles_time)

    print("end")