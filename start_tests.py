import subprocess

from utils import EmailUtil
from utils import LogUtil


class RunTests(object):
	"""description of class"""

	def __init__(self):
		self.test_suite = "TestRepository/TestSuite.txt"

	# def create_suite():
	# 	suite = unittest.TestSuite()
	# 	suite = unittest.TestLoader().loadTestsFromTestCase(test_lu.TestLu)
	# 	suite = unittest.TestLoader().loadTestsFromModule(test_taobao)
	# 	suite.addTest(test_taobao.TestTaobao('test_search'))
	# 	suite.addTest(test_taobao.TestTaobao('test_login'))
	# 	print(str(suite.countTestCases()) + " tests in the TestSuite")
	# 	return suite

	def LoadAndRunTestCases(self):
		try:
			f = open(self.test_suite)
			tests = [test for test in f.readlines() if not test.startswith("#")]
			f.close()
			for item in tests:
				subprocess.call("nosetests TestRepository/" + str(item).replace("\n", ""), shell=True)
		except Exception as err:
			LogUtil.log("Failed running test cases, error message: {}".format(str(err)))
		finally:
			EmailUtil.send_report()


if __name__ == '__main__':
	# runner = unittest.TextTestRunner(verbosity=2)
	# runner = ReportUtil.get_html_report
	# runner.run(create_suite())

	run = RunTests()
	run.LoadAndRunTestCases()
