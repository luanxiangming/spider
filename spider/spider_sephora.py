from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import xlwt

browser = webdriver.Chrome()
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1200, 900)
wait = WebDriverWait(browser, 10)

# Excel
file_name = 'sephora.xls'
wbook = xlwt.Workbook(encoding='utf-8')
style = xlwt.easyxf('align: vertical center, horizontal center')
wsheet = wbook.add_sheet('brands')
wsheet.write(0, 0, 'Brand', style)
wsheet.write(0, 1, 'Image', style)
wsheet.write(0, 2, 'Width', style)
wsheet.write(0, 3, 'Height', style)


def all_brands():
	try:
		browser.get('http://www.sephora.cn/brand/')
		html = browser.page_source
		doc = pq(html)
		items = doc('#main > ul.letterBrandList.mb32 .letterBrandItem .brandItem').items()
		for i, item in enumerate(items):
			brand = {
				'title': item.find('a').attr('title'),
				'image': item.find('img').attr('src'),
				'width': item.find('img').attr('width'),
				'height': item.find('img').attr('height')
			}
			brand_to_excel(wsheet, brand, i + 1)

	except Exception:
		all_brands()


def brand_to_excel(wsheet, result, i):
	print(i, result)
	wsheet.write(i, 0, result.get('title'), style)
	wsheet.write(i, 1, result.get('image'), style)
	wsheet.write(i, 2, result.get('width'), style)
	wsheet.write(i, 3, result.get('height'), style)

	try:
		wbook.save(file_name)
	except Exception as e:
		print(e)
	else:
		print('write excel file successful')


def main():
	try:
		all_brands()
	except Exception:
		print("ERROR!")
	finally:
		browser.close()


if __name__ == '__main__':
	main()
