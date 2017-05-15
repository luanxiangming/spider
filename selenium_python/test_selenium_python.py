import unittest

from selenium_python import page_selenium_python as page
from selenium import webdriver
from config import *

class TestSeleniumPython(unittest.TestCase):
	def setUp(self):
		# self.driver = webdriver.Chrome()
		self.driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
		self.driver.get("http://selenium-python.readthedocs.io/")

	def test_repeat_next(self):
		driver = self.driver
		assert 'Selenium with Python' in driver.page_source
		main_page = page.MainPage(driver)
		main_page.repeat_next()

	def tearDown(self):
		self.driver.close()

	if __name__ == '__main__':
		test_repeat_next()

