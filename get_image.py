# -*- coding: utf-8 -*-
# 非gevent版本
import os
import requests
import time
from lxml import html

def get_response(url):

    # 填充请求的头部
    headers = {
        "headers" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"
    }
    
    response = requests.get(url, headers = headers)
    return response

# 获得每个页面的url
# 起始url 为 http://girl-atlas.com/
# 我爬的时候网站一共有92个页面
def get_page_urls():

    start_url = 'http://girl-atlas.com/'
    response = get_response(start_url)
    page_urls = []

    page_urls.append(start_url)
    while True:
        parsed_body = html.fromstring(response.text)
        # Xpath 提取访问下个页面的url
        next_url = parsed_body.xpath('//a[@class="btn-form next"]/@href')

        if not next_url:
            break

        next_url = start_url + next_url[0]
        page_urls.append(next_url)
        response = get_response(next_url)

    print "get_page_urls done!!!"

    return page_urls

# 获取每个girl专辑的Url
def get_girl_urls(page_urls):

    girl_urls = []
    
    for url in page_urls:
        response = get_response(url)
        parsed_body = html.fromstring(response.text)

        # Xpath
        girl = parsed_body.xpath('//div[@class="grid_title"]/a/@href')
        girl_urls.extend(girl)

    return girl_urls
    
def get_image_urls(girl_urls):

    girl_list = []
    
    for url in girl_urls:
        # print "in get_image_urls" + url[0]
        response = get_response(url)
        parsed_body = html.fromstring(response.text)

        # 专辑名
        girl_title  = parsed_body.xpath('//title/text()')
        image_urls = parsed_body.xpath('//li[@class="slide "]/img/@src | //li[@class="slide "]/img/@delay')

        girl_dict = {girl_title[0] : image_urls}
        girl_list.append(girl_dict)
        
    print "get_girl_urls done!!!"
    return girl_list

# 开始下载图片
def get_images(girl_list):

    count = 1
    # 图片的默认存储文件夹
    start_dir = '/home/pein/temp/'
    for girl in girl_list:
        dir_name = start_dir + girl.keys()[0]
        urls = girl.values()[0]

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        for url in urls:
            print url
            with open(dir_name + '/' + url.split('/')[-1], 'wb') as f:
                r = get_response(url)
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
