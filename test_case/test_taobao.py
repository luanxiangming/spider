import unittest

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from page import page_taobao as page


class TestTaobao(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome()

	# self.driver = webdriver.PhantomJS(service_args=config.SERVICE_ARGS)

	@unittest.skip("skip search test")
	def test_search(self):
		driver = self.driver
		driver.get("http://www.taobao.com")
		self.assertIn("淘宝", driver.title)
		elem = driver.find_element_by_css_selector('#q')
		elem.send_keys("手机")
		elem.send_keys(Keys.RETURN)
		assert "No results found" not in driver.page_source

	@unittest.skip("skip dropdown test")
	def test_dropdown(self):
		driver = self.driver
		driver.get("https://www.w3.org/")
		# element = driver.find_element_by_css_selector('#region_form > div > select')
		# all_options = element.find_elements_by_tag_name("option")
		# for option in all_options:
		# 	print("Value is: %s" % option.get_attribute("value"))
		# 	option.click()
		select = Select(driver.find_element_by_name('region'))
		options_number = len(select.options)
		print(str(options_number))
		for i in range(1, options_number):
			print(select.options[i].get_attribute('value'))
			select.select_by_index(i)

	@unittest.skip("skip switch_window test")
	def test_switch_window(self):
		driver = self.driver
		driver.get("http://www.qq.com/")
		# driver.switch_to_window("_self")
		for handle in driver.window_handles:
			driver.switch_to.window(handle)

	@unittest.skip("skip popup test")
	def test_popup(self):
		driver = self.driver
		driver.get("http://www.qq.com/")
		driver.find_element_by_class_name("login").click()
		# driver.switch_to.alert()
		print(Alert(driver).text)
		driver.find_element_by_id('switcher_plogin').click()

	@unittest.skip("skip forward_back test")
	def test_forward_back(self):
		driver = self.driver
		driver.get("http://www.baidu.com")
		input = driver.find_element_by_css_selector("#kw")
		input.clear()
		input.send_keys("电影")
		input.send_keys(Keys.RETURN)
		driver.back()
		driver.forward()

	""" A sample test class to show how page object works """
	def test_search_in_taobao(self):
		driver = self.driver
		driver.get("http://www.taobao.com")

		# Load the main page. In this case the home page of taobao.com.
		main_page = page.MainPage(driver)
		# Checks if the word "淘宝" is in title
		assert main_page.is_title_matches(), "taobao.com title not match"
		# Sets the text of search textbox to "手机"
		main_page.search_text_element = "手机"
		main_page.click_go_button()
		search_results_page = page.SearchResultsPage(driver)
		assert search_results_page.is_results_found(), "No results found"

	def test_login(self):
		driver = self.driver
		driver.get("http://www.taobao.com")
		main_page = page.MainPage(driver)
		main_page.goto_login_page()
		login_page = page.LoginPage(driver)
		login_page.password_login()
		login_page.authenticate()
		main_page.verify_login()

	def tearDown(self):
		self.driver.close()


if __name__ == '__main__':
	print("\n__name__ == '__main__'")
	unittest.main()
