import unittest

from selenium import webdriver

from page import page_selenium_python as page
from utils import LogUtil
from utils import common
from utils.TestCaseInfo import TestCaseInfo
from utils.TestReport import TestReport


class TestSeleniumPython(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
        self.base_url = "http://selenium-python.readthedocs.io/"
        self.testCaseInfo = TestCaseInfo(id='3', name=self.__str__(), owner='Oliver')
        self.testReport = TestReport()
        LogUtil.create_logger_file(__name__)

        self.testCaseInfo.starttime = common.get_current_time()
        LogUtil.log('Open base url: %s' % self.base_url)

    def test_repeat_next(self):
        try:
            driver = self.driver
            main_page = page.MainPage(driver)
            main_page.open(self.base_url)
            assert 'Selenium with Python' in main_page.page_source()
            main_page.repeat_next()
        except Exception as e:
            self.testCaseInfo.errorinfo = repr(e)
            LogUtil.log(('Got error: ' + repr(e)))
        else:
            self.testCaseInfo.result = 'Pass'

    def tearDown(self):
        self.driver.close()
        self.testCaseInfo.endtime = common.get_current_time()
        self.testCaseInfo.secondsDuration = common.get_time_diff(self.testCaseInfo.starttime, self.testCaseInfo.endtime)

        self.testReport.WriteHTML(self.testCaseInfo)


if __name__ == '__main__':
    unittest.main()
