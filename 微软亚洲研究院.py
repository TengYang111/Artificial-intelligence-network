# -*- coding:utf-8 -*-
import requests
import json
import time
import random
from lxml import etree
from newspaper import Article

def msra_analyzer(url):
	# 伪装成Mozilla浏览器，解决反爬虫
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	# 生成属性字典
	headers = {'User-Agent': user_agent}
	# 获取目标网站的HTML页面
	response = requests.get(url, headers=headers)
	# print(response.text)
	selector = etree.HTML(response.text)
	# print(selector)
	msra = []

	# 作爬取者名称
	ID = ' 爬虫小分队 '

	# 站点名称
	'''找版块'''
	website_name = selector.xpath('//*[@id="uhfCatLogo"]/span/text()')[0]
	print(website_name)

	# 版块
	website_block = selector.xpath('/html/body/div[2]/div/div/div/div[1]/div/ul/li[2]/a/text()')[0]
	print(website_block)

	# 新闻链接
	news_url = url

	# 作者
	news_author = selector.xpath('/html/body/div[2]/div/div/div/div[2]/div/article[1]/div/p/span[2]/text()')[0][3:]
	print(news_author)

	# 发布时间
	publish_time = selector.xpath('/html/body/div[2]/div/div/div/div[2]/div/article[1]/div/p/span[1]/text()')[
		0].lstrip().rstrip()
	# print(publish_time)
	year = publish_time[:4]
	month = publish_time[5:7]
	day = publish_time[8:10]
	hour = random.randint(0, 24)
	if hour < 10 and hour >= 0:
		hour = '0' + str(hour)
	else:
		hour = str(hour)
	# print(a)
	minute = random.randint(1, 60)
	if minute < 10 and minute >= 0:
		minute = '0' + str(minute)
	else:
		minute = str(minute)
	sec = random.randint(1, 60)
	if sec < 10 and sec >= 0:
		sec = '0' + str(sec)
	else:
		sec = str(sec)
	publish_time = year + month + day + ' ' + hour + ':' + minute + ':' + sec
	print(publish_time)

	# 爬取时间
	date = str(time.strftime("%Y%m%d"))
	currentTime = str(time.strftime("%H:%M:%S"))
	crawl_time = date + ' ' + currentTime
	print(crawl_time)

	# 标签
	news_tag = selector.xpath('/html/body/div[2]/div/div/div/div[2]/div/article[2]/ul/a/li/text()')
	# print(news_tag)
	if len(news_tag) == 0:
		print('no tags')
	news_tags = ','.join(news_tag)
	print(news_tags)

	# 新闻标题
	news_title = selector.xpath('/html/body/div[2]/div/div/div/div[2]/div/article[1]/h2/text()')[0].lstrip().rstrip()
	print(news_title)

	# 正文
	'''可以考虑下使用文章密度算法来快速解析文章正文'''
	a = Article(url, language='zh')  # Chinese
	a.download()
	a.parse()
	news_content = a.text
	print(news_content)
	# news_contents = selector.xpath('/html/body/div[2]/div/div/div/div[2]/div/article[1]/section[2]/ul/li/text()|/html/body/div[2]/div/div/div/div[2]/div/article[1]/section[2]/h2[1]/text()|/html/body/div[2]/div/div/div/div[2]/div/article/section/p/text()|/html/body/div[2]/div/div/div/div[2]/div/article/section/p/a/text()|/html/body/div[2]/div/div/div/div[2]/div/article/section/p/b/text()')
	# for news_content in news_contents:
	# 	print(news_content)
	# news_content = ''.join(news_contents)
	# print(news_content)

	# # 数据源链接
	request_url = url

	# 图片名称
	img_titles = selector.xpath('/html/body/div[2]/div/div/div/div[2]/div/article[1]/section[2]/p/em/text()')
	# print(img_titles)
	# print(len(img_titles))
	img_urls = selector.xpath('/html/body/div[2]/div/div/div/div[2]/div/article[1]/section[2]/p/img/@src')
	# print(img_urls)
	# print(len(img_urls))
	for a in range(len(img_urls)):
		if len(img_titles) != 0:
			if a >= 0 and a <= len(img_titles) - 1:
				# 'item' + str(i) = {}
				item = {}
				item['img_title'] = img_titles[a]
				item['img_url'] = img_urls[a]
				# print(item)
				msra.append(item)
			else:
				for b in range(len(img_titles), len(img_urls)):
					# print(b)
					item = {}
					c = b - len(img_titles)
					if c < 10 and c >= 0:
						item['img_title'] = news_title + '图片标题000' + str(c)
						item['img_url'] = img_urls[b]
					elif c < 100 and c >= 10:
						item['img_title'] = news_title + '图片标题00' + str(c)
						item['img_url'] = img_urls[b]
					elif c < 1000 and c >= 100:
						item['img_title'] = news_title + '图片标题0' + str(c)
						item['img_url'] = img_urls[b]
					else:
						item['img_title'] = news_title + '图片标题' + str(c)
						item['img_url'] = img_urls[b]
					# print(item)
					msra.append(item)
		else:
			item = {}
			if a < 10 and a >= 0:
				item['img_title'] = news_title + '图片标题000' + str(a)
				item['img_url'] = img_urls[a]
			elif a < 100 and a >= 10:
				item['img_title'] = news_title + '图片标题00' + str(a)
				item['img_url'] = img_urls[a]
			elif a < 1000 and a >= 100:
				item['img_title'] = news_title + '图片标题0' + str(a)
				item['img_url'] = img_urls[a]
			else:
				item['img_title'] = news_title + '图片标题' + str(a)
				item['img_url'] =img_urls[a]
			# print(item)
			msra.append(item)

	txt_item = {}
	txt_item['ID'] = ID
	txt_item['website_name'] = website_name
	txt_item['website_block'] = website_block
	txt_item['news_url'] = news_url
	txt_item['news_author'] = news_author
	txt_item['publish_time'] = publish_time
	txt_item['crawl_time'] = crawl_time
	txt_item['news_tags'] = news_tags
	txt_item['news_title'] = news_title
	txt_item['news_content'] = news_content
	txt_item['request_url'] = request_url

	msra.append(txt_item)
	print(msra)

if __name__ == '__main__':
	try:
		msra_analyzer('https://www.msra.cn/zh-cn/news/features/bma-20170207')
	except:
		print('有个地方出错了')