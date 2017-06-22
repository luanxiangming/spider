import time

from selenium.webdriver import ActionChains

import auth
from element import BasePageElement
from locators import *
from page.BasePage import BasePage


class SearchTextElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    # The locator for search box where search string is entered
    locator = 'q'


class MainPage(BasePage):
    """Home page action methods come here. i.e. taobao.com"""
    search_text_element = SearchTextElement()

    def __init__(self, browser='chrome'):
        super().__init__(browser)

    def click_search_button(self):
        """Triggers the search"""
        elem = self.waitUntilFindElement(MainPageLocators.SEARCH_BUTTON)
        self.click(elem)

    def goto_login_page(self):
        elem = self.waitUntilFindElement(MainPageLocators.LOGIN)
        self.click(elem)

    def get_nick_name(self):
        elem = self.waitUntilFindElement(MainPageLocators.USER_NICK)
        return elem.text

    def verify_login(self):
        try:
            elem = self.waitUntilFindElement(MainPageLocators.USER_NICK)
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

    def use_password_login(self):
        elem = self.waitUntilFindElement(LoginPageLocators.PASSWORD_LOGIN)
        self.click(elem)

    def get_nick_name(self):
        elem = self.waitUntilFindElement(MainPageLocators.USER_NICK)
        return elem.text

    def authenticate(self):
        username = self.waitUntilFindElement(LoginPageLocators.USERNAME_INPUT)
        password = self.waitUntilFindElement(LoginPageLocators.PASSWORD_INPUT)
        confirm = self.waitUntilFindElement(LoginPageLocators.LOGIN_BUTTON)

        username.clear()
        self.type(username, auth.TAOBAO_USER)

        password.clear()
        self.type(password, auth.TAOBAO_PASS)

        time.sleep(2)

        block = self.is_element_visible(LoginPageLocators.AUTH_BLOCK)
        if block:
            print("出现滑动条")
            actions = ActionChains()
            # actions.click_and_hold(block)
            # actions.move_by_offset(298, 0)
            actions.drag_and_drop_by_offset(self.findElement(LoginPageLocators.AUTH_BLOCK), 298, 0)
            actions.perform()
            time.sleep(2)
            if '验证通过' in self.page_source():
                print("验证通过")
                self.click(confirm)
            else:
                print("出错了")
        else:
            print("没有滑动条，直接登陆")
            self.click(confirm)


