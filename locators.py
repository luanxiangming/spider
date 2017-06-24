from selenium.webdriver.common.by import By

class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    SEARCH_BUTTON = ('CLASS_NAME', r'btn-search')
    LOGIN = ('CSS_SELECTOR', r'#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-sign > a.h')
    USER_NICK = ('CSS_SELECTOR', r'#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick')
    CHECK_IN = ('CSS_SELECTOR', r'body > div.screen-outer.clearfix > div.col-right > div.tbh-member.J_Module > div > div.member-bd > p > a.J_MemberPunch.h')


class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""
    pass


class LoginPageLocators(object):
    AUTH_BLOCK = ('ID', 'nc_1_n1z')
    PASSWORD_LOGIN = ('CSS_SELECTOR', r'#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
    USERNAME_INPUT = ('NAME', 'TPL_username')
    PASSWORD_INPUT = ('NAME', 'TPL_password')
    LOGIN_BUTTON = ('ID', 'J_SubmitStatic')


class CheckinPageLocators(object):
    COIN = ('CSS_SELECTOR', r'#content > div.coin-layout > div.coin-wrapper > div.side-bar > div > div.coin-panel > div.tjb-wrapper.tjb-login > div.my-coin > p.lg-2.info.J_Coin > a')
    BLOCK = ('CSS_SELECTOR', '#nc_1_n1z')
    CLOSE = (By.CSS_SELECTOR, '#ks-content-ks-component126 > div.coin-overlay-content > span')
    CHECK = (By.CSS_SELECTOR, r'#content > div.coin-layout > div.coin-wrapper > div.side-bar > div > div.coin-panel > div.tjb-wrapper.tjb-login > div.my-btns > a.btn.login-btn.J_GoTodayBtn')
