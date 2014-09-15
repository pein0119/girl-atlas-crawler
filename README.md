girl-atlas-crawler
==================

图片爬虫，爬 [http://www.girl-atlas.com ](http://www.girl-atlas.com) 整个网站的图片

## 依赖库 ##

* requests 发送http请求，下载图片
* lxml 解析html文件
* grequests 基于gevent的异步http请求库，加快爬取速度

## 源文件 ##

* get_image.py 每次发送一个请求
* get_image_gevent.py 每次发送五个请求

**注：可以在get_images函数中修改图片存放目录**
