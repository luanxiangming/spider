import unittest
import sys

from selenium import webdriver

from utils import LogUtil
from utils import common
from utils.TestCaseInfo import TestCaseInfo
from utils.TestReport import TestReport

# sys.path.append("..")
from page import page_lu as page


class TestLu(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome()
		self.base_url = 'http://www.lu.com'
		self.testCaseInfo = TestCaseInfo(id='2', name=self.__str__(), owner='Oliver')
		self.testReport = TestReport()
		LogUtil.create_logger_file(__name__)

		self.testCaseInfo.starttime = common.get_current_time()
		LogUtil.log('Open base url: %s' % self.base_url)

	# @unittest.skip("skip test_login")
	def test_login(self):
		driver = self.driver
		try:
			main_page = page.MainPage(driver)
			main_page.open(self.base_url)
			main_page.goto_login_page()
			login_page = page.LoginPage(page)
			login_page.authenticate()
			main_page.verify_login()
		except Exception as e:
			self.testCaseInfo.errorinfo = str(e)
		else:
			self.testCaseInfo.result = 'Pass'

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
		self.testCaseInfo.endtime = common.get_current_time()
		self.testCaseInfo.secondsDuration = common.get_time_diff(self.testCaseInfo.starttime, self.testCaseInfo.endtime)

		self.testReport.WriteHTML(self.testCaseInfo)


if __name__ == '__main__':
	unittest.main()
