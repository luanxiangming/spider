class TestCaseInfo(object):
	""" 测试用例信息类用来标识测试用例，并且包括执行用例执行结果信息 """

	def __init__(self, id="", name="", owner="", result="Failed", starttime="", endtime="", secondsDuration="", errorinfo=""):
		self.id = id
		self.name = name
		self.owner = owner
		self.result = result
		self.starttime = starttime
		self.endtime = endtime
		self.secondsDuration = secondsDuration
		self.errorinfo = errorinfo
