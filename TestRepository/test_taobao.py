import time
import unittest

from selenium import webdriver

from page import page_taobao as page
from utils import LogUtil
from utils import common
from utils.TestCaseInfo import TestCaseInfo
from utils.TestReport import TestReport


class TestTaobao(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome()
		self.base_url = 'http://www.taobao.com'
		self.testCaseInfo = TestCaseInfo(id='1', name=self.__str__(), owner='Oliver')
		self.testReport = TestReport()
		LogUtil.create_logger_file(__name__)

		self.testCaseInfo.starttime = common.get_current_time()
		LogUtil.log('Open base url: %s' % self.base_url)

	def tearDown(self):
		self.driver.close()
		self.testCaseInfo.endtime = common.get_current_time()
		self.testCaseInfo.secondsDuration = common.get_time_diff(self.testCaseInfo.starttime, self.testCaseInfo.endtime)

		self.testReport.WriteHTML(self.testCaseInfo)

	# @unittest.skip("search test")
	# def test_search1(self):
	# 	driver = self.driver
	# 	driver.get("http://www.taobao.com")
	# 	self.assertIn("淘宝", driver.title)
	# 	elem = driver.find_element_by_css_selector('#q')
	# 	elem.send_keys("手机")
	# 	elem.send_keys(Keys.RETURN)
	# 	assert "No results found" not in driver.page_source
	#
	# @unittest.skip("dropdown test")
	# def test_dropdown(self):
	# 	driver = self.driver
	# 	driver.get("https://www.w3.org/")
	# 	select = Select(driver.find_element_by_name('region'))
	# 	options_number = len(select.options)
	# 	print(str(options_number))
	# 	for i in range(1, options_number):
	# 		print(select.options[i].get_attribute('value'))
	# 		select.select_by_index(i)
	#
	# @unittest.skip("switch_window test")
	# def test_switch_window(self):
	# 	driver = self.driver
	# 	driver.get("http://www.qq.com/")
	# 	# driver.switch_to_window("_self")
	# 	for handle in driver.window_handles:
	# 		driver.switch_to.window(handle)
	#
	# @unittest.skip("popup test")
	# def test_popup(self):
	# 	driver = self.driver
	# 	driver.get("http://www.qq.com/")
	# 	driver.find_element_by_class_name("login").click()
	# 	# driver.switch_to.alert()
	# 	print(Alert(driver).text)
	# 	driver.find_element_by_id('switcher_plogin').click()
	#
	# @unittest.skip("forward_back test")
	# def test_forward_back(self):
	# 	driver = self.driver
	# 	driver.get("http://www.baidu.com")
	# 	input = driver.find_element_by_css_selector("#kw")
	# 	input.clear()
	# 	input.send_keys("电影")
	# 	input.send_keys(Keys.RETURN)
	# 	driver.back()
	# 	driver.forward()

	""" A sample test class to show how page object works """

	def test_search(self):
		driver = self.driver
		try:
			main_page = page.MainPage(driver)
			main_page.open(self.base_url)
			assert '淘宝' in main_page.getTitle(), 'taobao.com title not match'

			main_page.search_text_element = "手机"
			main_page.click_search_button()

			search_results_page = page.SearchResultsPage(driver)
			assert search_results_page.is_results_found(), "No results found"
		except Exception as e:
			self.testCaseInfo.errorinfo = repr(e)
			LogUtil.log(('Got error: ' + repr(e)))
		else:
			self.testCaseInfo.result = 'Pass'

	def test_login(self, driver=None):
		if driver is None:
			driver = self.driver
		try:
			main_page = page.MainPage(driver)
			main_page.open(self.base_url)
			main_page.goto_login_page()

			login_page = page.LoginPage(driver)
			login_page.use_password_login()
			login_page.authenticate()

			time.sleep(2)
			login_page.refresh()
			assert 'tb_4199328' in login_page.get_nick_name()

		except Exception as e:
			self.testCaseInfo.errorinfo = repr(e)
			LogUtil.log(('Got error: ' + repr(e)))
		else:
			self.testCaseInfo.result = 'Pass'

	def test_checkin(self):
		driver = self.driver
		self.test_login(driver)
		try:
			main_page = page.MainPage(driver)
			main_page.open_checkin_page()

			checkin_page = page.CheckinPage(driver)
			checkin_page.check_in()
			assert '550' in checkin_page.get_coin_balance()
		except Exception as e:
			self.testCaseInfo.errorinfo = repr(e)
			LogUtil.log(('Got error: ' + repr(e)))
		else:
			self.testCaseInfo.result = 'Pass'

	def test_mytaobao(self):
		driver = self.driver
		self.test_login(driver)
		try:
			main_page = page.MainPage(driver)
			main_page.goto_profile_page()
		except Exception as e:
			self.testCaseInfo.errorinfo = repr(e)
			LogUtil.log(('Got error: ' + repr(e)))
		else:
			self.testCaseInfo.result = 'Pass'


if __name__ == '__main__':
	unittest.main()
