import re

from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import xlwt
import time

browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1200, 900)
wait = WebDriverWait(browser, 10)

# Excel
file_name = 'sephora.xls'
wbook = xlwt.Workbook(encoding='utf-8')
style = xlwt.easyxf('align: vertical center, horizontal center')
brand_sheet = wbook.add_sheet('所有品牌', cell_overwrite_ok=False)


def add_sheet(name):
	wsheet = wbook.add_sheet(name)
	return wsheet


def all_brands():
	try:
		browser.get('http://www.sephora.cn/brand/')
		html = browser.page_source
		doc = pq(html)
		items = doc('#main > ul.letterBrandList.mb32 .letterBrandItem .brandItem').items()

		brand_sheet.write(0, 0, 'Brand', style)
		brand_sheet.write(0, 1, 'Image', style)
		brand_sheet.write(0, 2, 'Width', style)
		brand_sheet.write(0, 3, 'Height', style)
		brand_sheet.write(0, 4, 'URL', style)
		brand_sheet.write(0, 5, 'Products', style)

		for i, item in enumerate(items):
			brand = {
				'title': item.find('a').attr('title'),
				'image': item.find('img').attr('src'),
				'width': item.find('img').attr('width'),
				'height': item.find('img').attr('height'),
				'url': item.find('a').attr('href')
			}
			brands_to_excel(brand_sheet, brand, i + 1)
	except Exception:
		all_brands()


def all_products():
	try:
		browser.get('http://www.sephora.cn/brand/')
		html = browser.page_source
		doc = pq(html)
		items = doc('#main > ul.letterBrandList.mb32 .letterBrandItem .brandItem').items()

		for i, item in enumerate(items):
			url = item.find('a').attr('href')
			total = get_brand_products(i + 1, url)
			if total is None:
				total = 'No products found for this brand'
			print(total)

	except Exception as e:
		# all_products()
		print(e)


def get_brand_products(i, url):
	try:
		print("\nAccessing URL: " + url)
		browser.get(url)
		# wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#toolBar > ul:nth-child(1) > li > div > h2 > a')))
		time.sleep(2)
		html = browser.page_source
		doc = pq(html)
		items = doc('#searchResultListDiv .productBox .proBox').items()
		total = browser.find_element_by_css_selector(
			'#globalFilterFacetProductDIV > div.filterSearch > div.filterTit > div').text
		count = re.compile('\d+').search(total).group(0)
		brand = {
			'products': count
		}
		brands_to_excel(brand_sheet, brand, i)

		brand_result = browser.find_element_by_css_selector(
			'#breadCrumb > span').text
		brand_name = re.sub('/', '', brand_result)

		sheet = add_sheet(brand_name)
		sheet.write(0, 0, 'Brand', style)
		sheet.write(0, 1, 'Title', style)
		sheet.write(0, 2, 'Image', style)
		sheet.write(0, 3, 'Price', style)
		sheet.write(0, 4, 'URL', style)
		sheet.write(0, 5, 'Comment', style)

		for i, item in enumerate(items):
			product = {
				'image': item.find('img').attr('src'),
				'brand': item.find('.proBrand').text(),
				'title': item.find('.proTit').text(),
				'price': item.find('.proPrice .proPrice').text(),
				'url': item.find('a').attr('href'),
				'comment': item.find('.proComment').text()
			}

			products_to_excel(sheet, product, i + 1)

		return total
	except Exception as e:
		print(e)
		brands_to_excel(brand_sheet, {'products': 0}, i)
		return None


def brands_to_excel(sheet, result, i):
	print(i, result)
	if 'products' in result.keys():
		sheet.write(i, 5, result.get('products', 0), style)
		return
	sheet.write(i, 0, result.get('title'), style)
	sheet.write(i, 1, result.get('image'), style)
	sheet.write(i, 2, result.get('width'), style)
	sheet.write(i, 3, result.get('height'), style)
	sheet.write(i, 4, result.get('url'), style)
	try:
		wbook.save(file_name)
	except Exception as e:
		print(e)
	else:
		print('品牌 {} 成功写入文件'.format(result.get('title')))


def products_to_excel(sheet, result, i):
	print(i, result)
	sheet.write(i, 0, result.get('brand'), style)
	sheet.write(i, 1, result.get('title'), style)
	sheet.write(i, 2, result.get('image'), style)
	sheet.write(i, 3, result.get('price'), style)
	sheet.write(i, 4, result.get('url'), style)
	sheet.write(i, 5, result.get('comment'), style)
	try:
		wbook.save(file_name)
	except Exception as e:
		print(e)
	else:
		print('品牌商品 {} 成功写入文件'.format(result.get('title')))


def main():
	try:
		all_brands()
		all_products()
	except Exception:
		print("ERROR!")
	finally:
		browser.close()


if __name__ == '__main__':
	main()
