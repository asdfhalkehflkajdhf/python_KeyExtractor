# coding: utf-8

import re
import requests
from bs4 import BeautifulSoup as soup
from pprint import pprint
import xml.etree.ElementTree as et
import time


'''
南方周末网站的文章抽取，构建关键词、标签抽取的测试集合
'''


def extract_article_links(url='http://www.infzm.com/news.shtml'):
    '''
    抽取南方周末的报道列表
    '''
    links = ""
    try:
        response = requests.get(url)
    except Exception as e:
        print("Exception: {}".format(e))
        time.sleep(60)
    else:
        doc = soup(response.text, 'html5lib')
        links = set([a['href'] for a in
                     doc.find_all('a', href=re.compile('infzm.com/content/\d+$'))])
    return links


def collect_article_links(start_url='http://www.infzm.com/news.shtml',
                          filename='links.txt', pageNum=2000):
    '''
    收集南方周末网站的文章链接
    '''
    collected = set()
    visited = set()
    current = extract_article_links(start_url)
    collected = collected.union(current)
    while len(current) > 0 and len(collected) < pageNum:
        url = current.pop()
        visited.add(url)
        links = extract_article_links(url)
        collected = collected.union(links)
        print('access: ', url)
        print('collected: ', len(collected))
        unvisited = [a for a in links if a not in visited]
        current = current.union(unvisited)

    print('Write collected links to ' + filename + '...')
    lst = list(collected)
    lst.sort()
    fout = open(filename, 'wt')
    fout.writelines([x + '\n' for x in lst])
    fout.close()


def collect_articles(link_file, article_file='articles.xml'):
    '''
    读取保存文章链接的文件，访问每一个文章链接，构建文章数据集
    '''
    fin = open(link_file, 'r')
    links = [a.strip() for a in fin.readlines()]
    fin.close()
    tree = et.ElementTree()
    root = et.Element('articles')
    tree._setroot(root)

    count = 0
    for url in links:
        count += 1
        print(count, '\t', url)
        try:
            title, content, tags = extract_article(url)
            print(title)
            if len(tags)<3:
                continue
            item = et.Element("article")
            root.append(item)
            et.SubElement(item, 'url').text = url
            et.SubElement(item, 'title').text = title
            et.SubElement(item, 'tags').text = ','.join(tags)
            et.SubElement(item, 'content').text = content
        except:
            print('Error:', url, '...')
            
    tree.write(article_file, 'utf-8')

    print('finished.')

  
def extract_article(url):
    '''
    只进行页面内容提取，不进行链接采集
    南方周末的抽取：例如：http://www.infzm.com/content/117747
    '''
    headers = {'User-Agent': "BingBot (Bing's spider)"}
    response = requests.get(url, headers=headers)
    doc = soup(response.text, 'html5lib')
    title = doc.title.text[7:]
    content = doc.find_all("section", id="articleContent")[0].text.strip()
    tags = [tag.text for tag in doc.find_all("li", class_="tagContent")]
    return title, content, tags

'''add_option用来加入选项，action是有store，store_true，store_false等，dest是存储的变量，default是缺省值，help是帮助提示
store 也有其它的两种形式： store_true 和 store_false 
'''
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-u', '--url', dest='url', help='url to fetch article', default='http://www.infzm.com/news.shtml')

    parser.add_option('--link-file', dest='link_file', help='file to store links',default="links.txt")
    parser.add_option('--link-num', dest='link_num', help='file to store links', type="int", default=2000) #多个以后不让爬取了
    parser.add_option('--link', action='store_true', dest='link',  help='collect links', default=False)
    
    parser.add_option('--article-file', dest='article_file', help='file to store articles')
    parser.add_option('--article', action='store_true', dest='article', help='collect articles', default=False)

    parser.add_option('--test-url', dest='test_url', help='eg:http://www.infzm.com/content/117747')
    (options, args) = parser.parse_args()
    print(options)

    if options.link and options.link_file:
        if options.url:
            '''开始的url list'''
            collect_article_links(start_url= options.url, filename=options.link_file, pageNum=options.link_num)
        else:
            '''默认为新闻页面'''
            collect_article_links(filename=options.link_file)

    if options.article and options.link_file and options.article_file:
        collect_articles(link_file=options.link_file, article_file = options.article_file)

    if options.test_url:
        url = options.url  # 'http://www.infzm.com/content/117747'
        title, content, tags = extract_article(url)
        print(title)
        print('----------------')
        pprint(tags)
        print('----------------')
        pprint(content)

    print("end")