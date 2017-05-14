from selenium import webdriver
import unittest
import page_lu


class TestLu(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.get("http://www.lu.com/")

	def test_login(self):
		driver = self.driver
		assert "陆金所" in driver.title
		main_page = page_lu.MainPage(driver)
		main_page.goto_login_page()
		login_page = page_lu.LoginPage(driver)
		login_page.authenticate()
		assert "请填写验证码" in driver.page_source
		main_page.verify_login()


	def test_my_account(self):
		driver = self.driver
		assert "陆金所" in driver.title
		main_page = page_lu.MainPage(driver)
		main_page.goto_login_page()
		login_page = page_lu.LoginPage(driver)
		login_page.authenticate()
		assert "请填写验证码" in driver.page_source
		main_page.verify_login()
		main_page.goto_account_page()
		account_page = page_lu.AccountPage(driver)
		account_page.skip_guide()
		account_page.check_balance()

	def tearDown(self):

		self.driver.close()

	if __name__ == '__main__':
		test_login()
		test_my_account()
