from datetime import datetime

"""
公共库模块是为创建测试用例服务的，它主要包括常量、公共函数、日志管理、报表管理以及发送邮件管理等。
"""


def get_current_time():
	""" change time to str """
	format_ = "%a %b %d %H:%M:%S %Y"
	return datetime.now().strftime(format_)


def get_time_diff(start, end):
	format_ = "%a %b %d %H:%M:%S %Y"
	return datetime.strptime(end, format_) - datetime.strptime(start, format_)
