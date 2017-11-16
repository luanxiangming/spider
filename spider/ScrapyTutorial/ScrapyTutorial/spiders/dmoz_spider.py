import scrapy

from ..items import DmozItem


class DmozSpider(scrapy.Spider):
	""" name: 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。"""
	name = 'dmoz'
	allowed_domains = ['dmoztools.net']

	'''start_urls: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。
	后续的URL则从初始的URL获取到的数据中提取。'''
	start_urls = [
		"http://dmoztools.net/Computers/Programming/Languages/Python/",
	]

	''' parse() 是spider的一个方法。 被调用时，每个初始URL完成下载后生成的 Response 对象将会作为唯一的参数传递给该函数。 
	该方法负责解析返回的数据(response data)，提取数据(生成item)以及生成需要进一步处理的URL的 Request 对象。
	'''

	def parse(self, response):
		for href in response.xpath("//div[@class='cat-item']/a/@href"):
			url = response.urljoin(href.extract())
			yield scrapy.Request(url, callback=self.parse_dir_contents)

	def parse_dir_contents(self, response):
		for sel in response.xpath("//div[@class='site-item ']"):
			item = DmozItem()
			item['title'] = sel.xpath("div[@class='title-and-desc']/a/div[@class='site-title']/text()").extract()
			item['link'] = sel.xpath("div[@class='title-and-desc']/a/@href").extract()
			item['desc'] = sel.xpath("div[@class='title-and-desc']/div[@class='site-descr ']/text()").extract()
			yield item
