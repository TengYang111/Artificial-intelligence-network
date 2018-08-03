# -*- coding:utf-8 -*-
import requests
import json
import time
import random
import newspaper
from lxml import etree
from newspaper import Article

def leiphone_analyzer(url):
	# 伪装成Mozilla浏览器，解决反爬虫
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	# 生成属性字典
	headers = {'User-Agent': user_agent}
	# 获取目标网站的HTML页面
	response = requests.get(url, headers=headers)
	# print(response.text)
	selector = etree.HTML(response.content)
	leifeng = []

	# 作爬取者名称
	ID = ' 爬虫小分队 '

	# 站点名称
	# website_name = selector.xpath('//title/text()')[0][-3:-1]
	website_name = selector.xpath('//title/text()')[0][-3:]
	print(website_name)

	# 版块
	website_block = selector.xpath('/html/body/div[2]/div/a[2]/text()')[0]
	print(website_block)

	# 新闻链接
	news_url = url

	# 作者
	news_author = selector.xpath('//div[@class = "title"]/span/text()')[0]
	print(news_author)

	# 发布时间
	a = random.randint(1, 61)
	if a >= 0 and a < 10:
		a = '0' + str(a)
	else:
		a = str(a)
	publish_time = selector.xpath('//td[@class = "time"]/text()')[0].lstrip().rstrip()
	# print(publish_time)
	year = publish_time[:4]
	month = publish_time[5:7]
	day = publish_time[8:11]
	hour = publish_time[11:13]
	minute = publish_time[14:16]
	publish_time = year + month + day + '' + hour + ':' + minute + ':' + a
	print(publish_time)

	# 爬取时间
	date = str(time.strftime("%Y%m%d"))
	currentTime = str(time.strftime("%H:%M:%S"))
	crawl_time = date + ' ' + currentTime
	print(crawl_time)

	# 标签
	news_tag = selector.xpath('//div[@class = "related-link clr"]/a/text()')
	news_tags = ','.join(news_tag)
	print(news_tags)

	# 新闻标题
	news_title = selector.xpath('/html/body/div[5]/div[1]/div[1]/div/h1/text()')[0].lstrip().rstrip()
	print(news_title)

	# 正文
	'''可以考虑下使用文章密度算法来快速解析文章正文'''
	a = Article(url, language='zh')  # Chinese
	a.download()
	a.parse()
	news_content = a.text
	print(news_content)
	# news_contents = selector.xpath('//*[@id="9b24"]/span[2]/a/text()|//div[@class = "lph-article-comView"]/p/span/text()|//*[@id="77c6"]/span/span/text()|//*[@id="77c6"]/span/span[2]/strong/span/text()|//*[@id="f493"]/span/text()')
	# news_content = ''.join(news_contents)
	# print(news_content)

	# # 数据源链接
	request_url = url

	# 图片名称
	img_titles = selector.xpath('//p[@style = "text-align: center;"]/text()')
	# print(img_titles)
	# print(len(img_titles))
	img_urls = selector.xpath('//img[@alt = "%s"]/@src'%news_title)
	# print(img_urls)
	# print(len(img_urls))
	for a in range(len(img_urls)):
		if len(img_titles) != 0:
			if a >= 0 and a <= len(img_titles) - 1:
				# 'item' + str(i) = {}
				item = {}
				item['img_title'] = img_titles[a]
				item['img_url'] = img_urls[a]
				print(item)
				leifeng.append(item)
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
					print(item)
					leifeng.append(item)
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
				item['img_url'] = img_urls[a]
			# print(item)
			leifeng.append(item)

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

	leifeng.append(txt_item)
	print(leifeng)

if __name__ == '__main__':
	try:
		leiphone_analyzer('https://www.leiphone.com/news/201806/puk2y8oSPdiEFFrW.html')
	except:
		print('有个地方出错了')