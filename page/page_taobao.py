from element import BasePageElement

from locators import MainPageLocators


class SeachTextElement(BasePageElement):
	"""This class gets the search text from the specified locator"""

	# The locator for search box where search string is entered
	locator = 'q'

class BasePage(object):
	"""Base class to initialize the base page that will be called from all pages"""
	def __init__(self, driver):
		self.driver = driver


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

class SearchResultsPage(BasePage):
	"""Search results page action methods come here"""
	def is_results_found(self):
		# Probably should search for this text in the specific page
		# element, but as for now it works fine
		return "No results found" not in self.driver.page_source
