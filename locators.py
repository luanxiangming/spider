class MainPageLocators(object):
    """A class for main page locators. All main page locators should come here"""
    SEARCH_BUTTON = ('CLASS_NAME', r'btn-search')
    LOGIN = ('CSS_SELECTOR', r'#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-sign > a.h')
    USER_NICK = ('CSS_SELECTOR', r'#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick')
    # USER_NICK = ('CLASS_NAME', r'site-nav-login-info-nick')


class SearchResultsPageLocators(object):
    """A class for search results locators. All search results locators should come here"""
    pass


class LoginPageLocators(object):
    AUTH_BLOCK = ('ID', 'nc_1_n1z')
    PASSWORD_LOGIN = ('CSS_SELECTOR', r'#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static')
    USERNAME_INPUT = ('NAME', 'TPL_username')
    PASSWORD_INPUT = ('NAME', 'TPL_password')
    LOGIN_BUTTON = ('ID', 'J_SubmitStatic')
