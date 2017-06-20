import unittest
import os
import HTMLTestRunner
from test_case import test_lu, test_taobao, test_selenium_python
from config import REPORT_DIR, REPORT_FILE


def create_suite():
	suite = unittest.TestSuite()
	# suite = unittest.TestLoader().loadTestsFromTestCase(test_lu.TestLu)
	# suite = unittest.TestLoader().loadTestsFromModule(test_taobao)
	suite.addTest(test_taobao.TestTaobao('test_search_in_taobao'))
	suite.addTest(test_taobao.TestTaobao('test_login'))
	print(str(suite.countTestCases()) + " tests in the TestSuite")
	return suite


if __name__ == '__main__':
	# runner = unittest.TextTestRunner(verbosity=2)
	base_dir = os.path.dirname(__file__)
	report_path = os.path.join(base_dir, REPORT_DIR, REPORT_FILE)
	fp = open(report_path, 'wb')
	runner = HTMLTestRunner.HTMLTestRunner(
		stream=fp,
		title=u'测试报告',
		description=u'用例的执行情况'
	)
	runner.run(create_suite())
	print("Report: " + report_path)
