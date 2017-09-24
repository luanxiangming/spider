import os
import re

import pymysql.cursors
import xlwt
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import *

# Connect to the database
conn = pymysql.connect(host=MYSQL_URL,
                       port=MYSQL_PORT,
                       user=MYSQL_USER,
                       password=MYSQL_PASSWORD,
                       db=MYSQL_DB,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
# Excel
file_name = 'taobao.xls'
wbook = xlwt.Workbook(encoding='utf-8')
style = xlwt.easyxf('align: vertical center, horizontal center')
wsheet = wbook.add_sheet('1')
wsheet.write(0, 0, 'Deal', style)
wsheet.write(0, 1, 'Image', style)
wsheet.write(0, 2, 'Location', style)
wsheet.write(0, 3, 'Price', style)
wsheet.write(0, 4, 'Shop', style)
wsheet.write(0, 5, 'Title', style)

browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1200, 900)
wait = WebDriverWait(browser, 10)


def get_products():
	wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
	html = browser.page_source
	doc = pq(html)
	items = doc('#mainsrp-itemlist .items .item').items()

	for i, item in enumerate(items):
		product = {
			'image': item.find('.pic .img').attr('src'),
			'price': item.find('.price').text(),
			'deal': item.find('.deal-cnt').text()[:-3],
			'title': item.find('.title').text(),
			'shop': item.find('.shop').text(),
			'location': item.find('.location').text(),
		}
		# print(product)
		# save_to_mysql(product)
		save_to_excel(wsheet, product, i + 1)


def search():
	print("---搜索关键字: " + KEY_WORD_TAOBAO)
	print('os.path: ' + str(os.path))
	try:
		browser.get('https://www.taobao.com')

		input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
		)
		input.send_keys(KEY_WORD_TAOBAO)
		submit.click()
		total = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
		)
		get_products()
		return total.text
	except TimeoutException:
		return search()


def next_page(page_number):
	print("---开始翻页: " + str(page_number))
	try:
		input = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
		)
		confirm = wait.until(
			EC.element_to_be_clickable(
				(By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
		)
		input.clear()
		input.send_keys(page_number)
		confirm.click()
		wait.until(
			EC.text_to_be_present_in_element(
				(By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number))
		)

		global wsheet
		wsheet = wbook.add_sheet(str(page_number))
		wsheet.write(0, 0, 'Deal', style)
		wsheet.write(0, 1, 'Image', style)
		wsheet.write(0, 2, 'Location', style)
		wsheet.write(0, 3, 'Price', style)
		wsheet.write(0, 4, 'Shop', style)
		wsheet.write(0, 5, 'Title', style)

		get_products()
	except TimeoutException:
		next_page()


def save_to_mysql(result):
	values = []
	for k, v in sorted(result.items()):
		values.append(v)
	try:
		with conn.cursor() as cursor:
			sql = 'INSERT INTO ' + MYSQL_TABLE_TAOBAO + '(Deal,Image,Location,Price,Shop,Title) VALUES(%s,%s,%s,%s,%s,%s)'
			cursor.execute(sql, values)
		# connection is not autocommit by default. So you must commit to save your changes.
		conn.commit()
		with conn.cursor() as cursor:
			sql = 'SELECT * FROM ' + MYSQL_TABLE_TAOBAO + ' WHERE ' \
			                                              'Deal=%s AND ' \
			                                              'Image=%s AND ' \
			                                              'Location=%s AND ' \
			                                              'Price=%s AND ' \
			                                              'Shop=%s AND ' \
			                                              'Title=%s'
			cursor.execute(sql, values)

			query = cursor.fetchone()
			print(query)
		# print("Save MYSQL SUCCESS.")
	# cursor.close()
	except Exception:
		print("Save MYSQL FAIL.", result)


def save_to_excel(wsheet, result, i):
	print(i, result)
	wsheet.write(i, 0, result.get('deal'), style)
	wsheet.write(i, 1, result.get('image'), style)
	wsheet.write(i, 2, result.get('location'), style)
	wsheet.write(i, 3, result.get('price'), style)
	wsheet.write(i, 4, result.get('shop'), style)
	wsheet.write(i, 5, result.get('title'), style)

	try:
		wbook.save(file_name)
	except Exception as e:
		print(e)
	else:
		print('write excel file successful')


def main():
	try:
		total = search()
		total = int(re.compile('(\d+)').search(total).group(0))
		print("Total pages: " + str(total))
		for page_number in range(2, 5):
			next_page(page_number)
	except Exception:
		print("ERROR!")
	finally:
		conn.close()
		browser.close()


if __name__ == '__main__':
	main()
