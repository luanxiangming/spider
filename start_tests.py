import unittest

from test_case import test_taobao


def create_suite():
	suite = unittest.TestSuite()
	# suite = unittest.TestLoader().loadTestsFromTestCase(test_lu.TestLu)
	# suite = unittest.TestLoader().loadTestsFromModule(test_taobao)
	suite.addTest(test_taobao.TestTaobao('test_search'))
	suite.addTest(test_taobao.TestTaobao('test_login'))
	print(str(suite.countTestCases()) + " tests in the TestSuite")
	return suite


if __name__ == '__main__':
	runner = unittest.TextTestRunner(verbosity=2)
	# runner = ReportUtil.get_html_report

	runner.run(create_suite())
