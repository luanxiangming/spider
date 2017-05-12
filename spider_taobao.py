import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymysql.cursors

# Connect to the database
conn = pymysql.connect(host=MYSQL_URL,
                       port=MYSQL_PORT,
                       user=MYSQL_USER,
                       password=MYSQL_PASSWORD,
                       db=MYSQL_DB,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

# browser = webdriver.Chrome()
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400, 900)
wait = WebDriverWait(browser, 10)


def get_products():
	wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
	html = browser.page_source
	doc = pq(html)
	items = doc('#mainsrp-itemlist .items .item').items()
	for item in items:
		product = {
			'image': item.find('.pic .img').attr('src'),
			'price': item.find('.price').text(),
			'deal': item.find('.deal-cnt').text()[:-3],
			'title': item.find('.title').text(),
			'shop': item.find('.shop').text(),
			'location': item.find('.location').text(),
		}
		# print(product)
		save_to_mysql(product)


def search():
	print("开始搜索---")
	try:
		browser.get('http://www.taobao.com')

		input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
		submit = wait.until(
			EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
		)
		input.send_keys(KEY_WORD)
		submit.click()
		total = wait.until(
			EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
		)
		get_products()
		return total.text
	except TimeoutException:
		return search()


def next_page(page_number):
	print("开始翻页---" + str(page_number))
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
		get_products()
	except TimeoutException:
		next_page(page_number)


def save_to_mysql(result):
	try:
		with conn.cursor() as cursor:
			sql = "INSERT INTO product(Image,Price,Deal,Title,Shop,Location) VALUES(%s,%s,%s,%s,%s,%s)"
			cursor.execute(sql,
			               (result['image'], result['price'], result['deal'], result['title'], result['shop'],
			                result['location'])
			               )
		# connection is not autocommit by default. So you must commit to save your changes.
		conn.commit()
		with conn.cursor() as cursor:
			sql = "SELECT Image,Price,Deal,Title,Shop,Location FROM product WHERE " \
			      "Image=%s AND " \
			      "Price=%s AND " \
			      "Deal=%s AND " \
			      "Title=%s AND " \
			      "Shop=%s AND " \
			      "Location=%s"
			cursor.execute(sql, (result['image'], result['price'], result['deal'], result['title'], result['shop'],
			                result['location']))
			result = cursor.fetchone()
			print(result)
		# print("Save MYSQL SUCCESS.")
	# cursor.close()
	except Exception:
		print("Save MYSQL FAIL.", result)


def main():
	try:
		total = search()
		total = int(re.compile('(\d+)').search(total).group(1))
		for page_number in range(2, total + 1):
			next_page(page_number)
	except Exception:
		print("ERROR")
	finally:
		conn.close()
		browser.close()


if __name__ == '__main__':
	main()
