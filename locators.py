from selenium.webdriver.common.by import By


class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    GO_BUTTON = (By.CLASS_NAME, 'btn-search')
    LOGIN = (By.CSS_SELECTOR, '#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-sign > a.h')
    USER_NICK = (By.CSS_SELECTOR, '#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick')


class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""
    pass


class LoginPageLocators(object):
    AUTH_BLOCK = (By.ID, 'nc_1_n1z')
    PASSWORD_LOGIN = (By.CSS_SELECTOR, '#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
    USERNAME_INPUT = (By.NAME, 'TPL_username')
    PASSWORD_INPUT = (By.NAME, 'TPL_password')
    LOGIN_BUTTON = (By.ID, 'J_SubmitStatic')

