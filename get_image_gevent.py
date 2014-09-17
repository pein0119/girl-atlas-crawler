# -*- coding: utf-8 -*-
# 使用grequests 重写，提高爬图速度

import os
import requests
import grequests
import time
from lxml import html

def get_response(url):

    headers = {
        "headers" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"
    }
    
    response = requests.get(url, headers = headers)
    return response

# 获取每个页面的url
def get_page_urls():

    start_url = 'http://girl-atlas.com/'
    response = get_response(start_url)
    page_urls = []

    page_urls.append(start_url)
    while True:
        parsed_body = html.fromstring(response.text)
        next_url = parsed_body.xpath('//a[@class="btn-form next"]/@href')

        if not next_url:
            break

        next_url = start_url + next_url[0]
        page_urls.append(next_url)
        response = get_response(next_url)

    print "get_page_urls done!!!"

    return page_urls

# 获取每个girl专辑的url
def get_girl_urls(page_urls):

    girl_urls = []

    # 采用grequests，建立5个并发连接
    rs = (grequests.get(url) for url in page_urls)
    responses = grequests.map(rs, size = 5)
    
    for response in responses:
        parsed_body = html.fromstring(response.text)
        girl = parsed_body.xpath('//div[@class="grid_title"]/a/@href')
        girl_urls.extend(girl)
    
    return girl_urls
    
def get_image_urls(girl_urls):

    girl_list = []

    # 建立5个并发连接
    rs = (grequests.get(url) for url in girl_urls)
    responses = grequests.map(rs, size = 5)

    for response in responses:
        parsed_body = html.fromstring(response.text)
        girl_title  = parsed_body.xpath('//title/text()')
        image_urls = parsed_body.xpath('//li[@class="slide "]/img/@src | //li[@class="slide "]/img/@delay')

        # print image_urls
        girl_dict = {girl_title[0] : image_urls}
        girl_list.append(girl_dict)
    
    print "get_girl_urls done!!!"
    return girl_list

def get_images(girl_list):

    count = 1
    # 图片的默认存储目录
    start_dir = '/home/pein/Pictures/'

    for girl in girl_list:
        dir_name = start_dir + girl.keys()[0]
        urls = girl.values()[0]

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        rs = (grequests.get(url) for url in urls)
        responses = grequests.map(rs)

        image_dict = dict(zip(urls, responses))
        for url in image_dict:
            print url
            with open(dir_name + '/' + url.split('/')[-1], 'wb') as f:
                r = image_dict[url]
                f.write(r.content)

        print
        print count, girl.keys()[0] + "  done!!!"

        count += 1
        print 

if __name__ == '__main__':

    page_urls = get_page_urls()
    
    start_time = time.time()
    
    girl_urls = get_girl_urls(page_urls)
    girl_list = get_image_urls(girl_urls)
    print "girl %s" % len(girl_urls)
    get_images(girl_list)

    elapsed_time = time.time() - start_time
    print
    print "elasped %s seconds!!!!" % elapsed_time
