"""Beautiful Soup 4.4.0 文档
http://beautifulsoup.readthedocs.io/zh_CN/latest/#id8
"""
from urllib import request
from bs4 import BeautifulSoup

url = 'http://www.136book.com/huaqiangu/'
print(dir(BeautifulSoup))
f = open('book.txt', 'w')


def crawl_chapters():
	# head = {}
	# # 使用代理
	# head[
	# 	'User-Agent'] = 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'
	# req = request.Request(url, headers=head)
	req = request.Request(url)
	response = request.urlopen(req)
	html = response.read()
	soup = BeautifulSoup(html, 'lxml')
	soup_texts = soup.find('div', id='book_detail').find_next('div')

	for link in soup_texts.ol.children:
		if link != '\n':
			print(link.text, link.a.get('href'))


def crawl_contents():
	req = request.Request(url)
	response = request.urlopen(req)
	html = response.read()
	soup = BeautifulSoup(html, 'lxml')
	soup_texts = soup.find('div', id='book_detail').find_next('div')

	for link in soup_texts.ol.children:
		if link != '\n':
			chapter = request.Request(link.a.get('href'))
			chapter_response = request.urlopen(chapter)
			chapter_html = chapter_response.read()
			chapter_soup = BeautifulSoup(chapter_html, 'lxml')
			chapter_text = chapter_soup.find('div', id='content')
			f.write(link.text + '\n')
			for paragraph in chapter_text.find_all('p'):
				if paragraph != '\n':
					f.write(paragraph.text + '\n')
	f.close()


if __name__ == '__main__':
	# crawl_chapters()
	crawl_contents()
