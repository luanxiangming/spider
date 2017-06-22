import smtplib
from datetime import datetime
from os.path import basename

from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


smtp_info = {
		"hostname": "smtp.qq.com",
		"username": "82740301@qq.com",
		"password": "xpagwzokxmdzbjcb"  # 使用第三方SMTP服务发送, 获取授权码登录
	}
mail_info = {
	"from": "82740301@qq.com",
	"to": "oliver19830714@gmail.com",
	"mail_encoding": "utf-8"
}

smtpobj = smtplib.SMTP_SSL(smtp_info["hostname"], timeout=5)
smtpobj.set_debuglevel(1)
smtpobj.ehlo(smtp_info["hostname"])
smtpobj.login(smtp_info["username"], smtp_info["password"])


def send_email(format, subject, content, attach=None):
	# 三个参数：第一个为文本内容，第二个设置文本格式，第三个 utf-8 设置编码
	msg = MIMEText(content, format, mail_info["mail_encoding"])
	msg["Subject"] = Header(subject, mail_info["mail_encoding"])
	msg["from"] = mail_info["from"]
	msg["to"] = mail_info["to"]

	# if attach:
	# 	with open(attach, "rb") as f:
	# 		part = MIMEApplication(f.read(), Name=basename(attach))
	# 		msg.attach(part)

	try:
		smtpobj.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
		smtpobj.quit()
		print("邮件发送成功")
	except smtplib.SMTPException:
		print("Error: 无法发送邮件")


def send_report():
	html_report = 'report/report.html'
	with open(html_report) as f:
		text = f.read()
	subject = 'Web Automation Test Report_' + str(datetime.today())
	send_email('html', subject, text)
