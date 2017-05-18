import unittest
from selenium import webdriver
import sys

sys.path.append("..")
from page import page_lu as page


class TestLu(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.get("http://www.lu.com/")

	# @unittest.skip("skip test_login")
	def test_login(self):
		driver = self.driver
		assert "陆金所" in driver.title
		main_page = page.MainPage(driver)
		main_page.goto_login_page()
		login_page = page.LoginPage(driver)
		login_page.authenticate()
		main_page.verify_login()

	# @unittest.skip("skip test_my_account")
	def test_my_account(self):
		driver = self.driver
		self.test_login()
		main_page = page.MainPage(driver)
		main_page.goto_account_page()
		account_page = page.AccountPage(driver)
		account_page.skip_guide()
		account_page.check_balance()

	def tearDown(self):
		pass


if __name__ == '__main__':
	print("\n__name__ == '__main__'")
	unittest.main()


