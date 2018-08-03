# -*- coding:utf-8 -*-
import requests
import json
import time
import random
from lxml import etree
from newspaper import Article

def jiqizhixin_analyzer(url):
	# 伪装成Mozilla浏览器，解决反爬虫
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	# 生成属性字典
	headers = {'User-Agent': user_agent}
	# 获取目标网站的HTML页面
	response = requests.get(url, headers=headers)
	# print(response.text)
	selector = etree.HTML(response.text)
	jiqizhixin = []

	# 作爬取者名称
	ID = ' 爬虫小分队 '

	# 站点名称
	# website_name = selector.xpath('//title/text()')[0][-3:-1]
	website_name = selector.xpath('//title/text()')[0][-4:]
	print(website_name)

	# 版块
	website_block = selector.xpath('//*[@id="header"]/div/div[1]/div[2]/span/text()')[0]
	print(website_block)

	# 新闻链接
	news_url = url

	# 作者
	news_author = selector.xpath('//a[@class = "article-author__name"]/text()')[0]
	print(news_author)

	# 发布时间
	publish_time = selector.xpath('//time[@class = "article__published"]/text()')[0].lstrip().rstrip()
	year = publish_time[:4]
	month = publish_time[5:7]
	# print(month)
	day = publish_time[8:10]
	hour_time = publish_time[-5:-4]
	if hour_time == ' ':
		hour_time = '0' + publish_time[-4:-3]
	# print(hour_time)
	else:
		hour_time = publish_time[-5:-3]
	sec_time = random.randint(0, 60)
	if sec_time >= 0 and sec_time < 10:
		sec_time = '0' + str(sec_time)
	else:
		sec_time = str(sec_time)
	publish_time = year + month + day + ' ' + hour_time + ':' + publish_time[-2:] + ':' + sec_time
	print(publish_time)

	# 爬取时间
	date = str(time.strftime("%Y%m%d"))
	currentTime = str(time.strftime("%H:%M:%S"))
	crawl_time = date + ' ' + currentTime
	print(crawl_time)

	# 标签
	news_tag = selector.xpath('//*[@id="js-article-inline"]/div[3]/div[1]/a/text()')
	news_tags = ','.join(news_tag)
	print(news_tags)

	# 新闻标题
	news_title = selector.xpath('//h1[@class = "article__title"]/text()')[0].lstrip().rstrip()
	print(news_title)

	# 正文
	'''可以考虑下使用文章密度算法来快速解析文章正文'''
	a = Article(url, language='zh')  # Chinese
	a.download()
	a.parse()
	news_content = a.text
	print(news_content)
	# news_contents = selector.xpath('//*[@id="js-article-content"]/blockquote/p/text()|//*[@id="js-article-content"]/p/strong/text()|//*[@id="js-article-inline"]/p/text()|//*[@id="js-article-content"]/p/text()|//*[@id="js-article-content"]/section/section/section/section/section/section/section/section/section/section/section/section/text()|//*[@id="js-article-content"]/section/section/section/section/section/section/section/section/section/section/section/section/mark/text()|//*[@id="js-article-content"]/ul/li/p/text()')
	# for news_content in news_contents:
	# 	print(news_content)
	# news_content = ''.join(news_contents)
	# print(news_content)

	# # 数据源链接
	request_url = url

	# 图片名称
	img_titles = selector.xpath('//span[@class = "fr-inner"]/text()|//p[@style = "text-align: center;"]/text()|//span[@class = "fr-inner"]/em/text()|//*[@id="js-article-content"]/p[5]/em/text()')
	# print(img_titles)
	# print(len(img_titles))
	img_urls = selector.xpath('//span[@class = "fr-img-wrap"]/img/@src|//img[@class = "fr-fic fr-dib"]/@src')
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
				jiqizhixin.append(item)
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
					jiqizhixin.append(item)
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
			jiqizhixin.append(item)

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

	jiqizhixin.append(txt_item)
	print(jiqizhixin)

if __name__ == '__main__':
	try:
		jiqizhixin_analyzer('https://www.jiqizhixin.com/articles/2018-07-22')
	except:
		print('有个地方出错了')