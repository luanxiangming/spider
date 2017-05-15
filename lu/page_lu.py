from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import auth

class BasePage(object):
	def __init__(self, driver):
		self.driver = driver
		self.wait = WebDriverWait(self.driver, 60)


class MainPage(BasePage):
	def goto_login_page(self):
		login = self.wait.until(
			EC.element_to_be_clickable(
				(By.ID, 'header-nolog-login'))
		)
		login.click()

	def verify_login(self):
		self.wait.until(EC.presence_of_element_located(
			(By.ID, 'safe-logout')))

	def goto_account_page(self):
		my_account = self.wait.until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, '#header-body-my-account-panel > ul > li.my-account > a > span:nth-child(1)')))
		my_account.click()
		self.driver.switch_to.window(self.driver.window_handles[-1])

	def get_cookies(self):
		return self.driver.get_cookies()

class LoginPage(BasePage):
	def authenticate(self):
		username_login = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
		                                                             'body > div.login-wrap > div > div > div > div > div.login-tabWrap.clearBoth > div:nth-child(2) > a')))
		username_login.click()
		username = self.wait.until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, '#userNameLogin'))
		)
		password = self.wait.until(EC.presence_of_element_located(
			(By.CSS_SELECTOR, '#pwd')))
		username.clear()
		username.send_keys(auth.LU_USER)
		password.clear()
		password.send_keys(auth.LU_PASS)
		password.send_keys(Keys.RETURN)

class AccountPage(BasePage):
	def skip_guide(self):
		step1 = self.wait.until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="acount_wrap"]/div/div[3]/div[2]/div[1]/a')))
		step1.click()
		step2 = self.wait.until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="acount_wrap"]/div/div[3]/div[2]/div[2]/a')))
		step2.click()
		step3 = self.wait.until(
			EC.presence_of_element_located((By.XPATH, '//*[@id="acount_wrap"]/div/div[3]/div[2]/div[3]/a')))
		step3.click()


	def check_balance(self):
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#acount_wrap > div > div.main-account.account-home.clearfix > div.main-content > div.total-asset-wrapper > div.total-asset > div > span')))
