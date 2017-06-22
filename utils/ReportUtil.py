import os

from config import REPORT_FILE, REPORT_DIR
from utils import HTMLTestRunner
from utils.common import TestCaseInfo


class TestReport:

	def write_html_report(self, ):
		base_dir = os.path.dirname(__file__)
		report_path = os.path.join(base_dir, '../', REPORT_DIR, REPORT_FILE)
		fp = open(report_path, 'wb')
		runner = HTMLTestRunner.HTMLTestRunner(
			stream=fp,
			title=u'测试报告',
			description=u'用例的执行情况'
		)
		print("Report: " + report_path)
		return runner
