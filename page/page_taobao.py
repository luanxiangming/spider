import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import auth
import unittest

from element import BasePageElement

from locators import *


class SeachTextElement(BasePageElement):
	"""This class gets the search text from the specified locator"""

	# The locator for search box where search string is entered
	locator = 'q'

class BasePage(object):
	"""Base class to initialize the base page that will be called from all pages"""
	def __init__(self, driver):
		self.driver = driver
		self.wait = WebDriverWait(self.driver, 20)

class MainPage(BasePage):
	"""Home page action methods come here. i.e. taobao.com"""
	search_text_element = SeachTextElement()

	def is_title_matches(self):
		"""Verifies that the hardcoded text "淘宝" appears in page title"""
		return "淘宝" in self.driver.title

	def click_go_button(self):
		"""Triggers the search"""
		elem = self.driver.find_element(*MainPageLocators.GO_BUTTON)
		elem.click()

	def goto_login_page(self):
		elem = self.wait.until(
			EC.presence_of_element_located(
				MainPageLocators.LOGIN
			))
		elem.click()

	def verify_login(self):
		try:
			elem = self.wait.until(
				EC.presence_of_element_located(
					MainPageLocators.USER_NICK
				)
			)
			print(elem.text)
		except Exception:
			print("Authentication Failure")

class SearchResultsPage(BasePage):
	"""Search results page action methods come here"""
	def is_results_found(self):
		# Probably should search for this text in the specific page
		# element, but as for now it works fine
		return "No results found" not in self.driver.page_source

class LoginPage(BasePage):

	def password_login(self):
		elem = self.wait.until(
			EC.presence_of_element_located(
				LoginPageLocators.PASSWORD_LOGIN
			))
		elem.click()

	def authenticate(self):
		username = self.wait.until(
			EC.presence_of_element_located(
				LoginPageLocators.USERNAME_INPUT
			)
		)
		password = self.wait.until(
			EC.presence_of_element_located(
				LoginPageLocators.PASSWORD_INPUT
			)
		)
		confirm = self.wait.until(
			EC.element_to_be_clickable(
				LoginPageLocators.LOGIN_BUTTON
			)
		)

		username.clear()
		username.send_keys(auth.TAOBAO_USER)
		password.clear()
		password.send_keys(auth.TAOBAO_PASS)
		time.sleep(2)

		block = self.is_element_visible(LoginPageLocators.AUTH_BLOCK)
		if block:
			print("出现滑动条")
			actions = ActionChains(self.driver)
			# actions.click_and_hold(block)
			# actions.move_by_offset(298, 0)
			actions.drag_and_drop_by_offset(self.driver.find_element(*LoginPageLocators.AUTH_BLOCK), 298, 0)
			actions.perform()
			time.sleep(2)
			if '验证通过' in self.driver.page_source:
				print("验证通过")
				confirm.click()
			else:
				print("出错了")
		else:
			print("没有滑动条，直接登陆")
			confirm.click()

	def is_element_visible(self, element):
		try:
			the_element = EC.visibility_of_element_located(element)
			assert the_element(self.driver)
			flag = True
		except:
			flag = False
		return flag