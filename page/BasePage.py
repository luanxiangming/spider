from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    """ Base class to initialize the base page that will be called from all pages """

    ''' webdriver instance '''

    def __init__(self, driver, browser='chrome'):
        """
        initialize selenium webdriver, use chrome as default webdriver
        """
        if not driver:
            if browser == "firefox" or browser == "ff":
                driver = webdriver.Firefox()
            elif browser == "chrome":
                driver = webdriver.Chrome()
            elif browser == "internet explorer" or browser == "ie":
                driver = webdriver.Ie()
            elif browser == "opera":
                driver = webdriver.Opera()
            elif browser == "phantomjs":
                driver = webdriver.PhantomJS()
            try:
                self.driver = driver
                self.wait = WebDriverWait(self.driver, 20)
            except Exception:
                raise NameError("Not found %s browser,You can enter 'ie', 'ff' or 'chrome'." % browser)
        else:
            self.driver = driver
            self.wait = WebDriverWait(self.driver, 20)

    def findElement(self, element):
        """
        Find element

        element is a set with format (identifier type, value), e.g. ('id','username')

        Usage:
        self.findElement(element)
        """

        try:
            type = element[0]
            value = element[1]
            if type == "ID":
                elem = self.driver.find_element_by_id(value)

            elif type == "NAME":
                elem = self.driver.find_element_by_name(value)

            elif type == "CLASS_NAME":
                elem = self.driver.find_element_by_class_name(value)

            elif type == "LINK_TEXT":
                elem = self.driver.find_element_by_link_text(value)

            elif type == "XPATH":
                elem = self.driver.find_element_by_xpath(value)

            elif type == "CSS_SELECTOR":
                elem = self.driver.find_element_by_css_selector(value)
            else:
                raise NameError("Please correct the type in function parameter")
        except Exception:
            raise ValueError("No such element found" + str(element))
        return elem

    def waitUntilFindElement(self, element):
        """
        http://selenium-python.readthedocs.io/api.html?highlight=wait.until
        """

        try:
            type = element[0]
            value = element[1]
            if type == "ID":
                elem = self.wait.until(
                    EC.presence_of_element_located(
                        (By.ID, value)
                    ))

            elif type == "NAME":
                elem = self.wait.until(
                    EC.presence_of_element_located(
                        (By.NAME, value)
                    ))

            elif type == "CLASS_NAME":
                elem = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, value)
                    ))

            elif type == "LINK_TEXT":
                elem = self.wait.until(
                    EC.presence_of_element_located(
                        (By.LINK_TEXT, value)
                    ))

            elif type == "XPATH":
                elem = self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, value)
                    ))

            elif type == "CSS_SELECTOR":
                elem = self.wait.until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, value)
                    ))

            else:
                raise NameError("Please correct the type in function parameter")
        except Exception:
            raise ValueError("No such element found" + str(element))
        return elem

    def findElements(self, element):
        """
        Find elements

        element is a set with format (identifier type, value), e.g. ('id','username')

        Usage:
        self.findElements(element)
        """
        try:
            type = element[0]
            value = element[1]
            if type == "ID":
                elem = self.driver.find_elements_by_id(value)

            elif type == "NAME":
                elem = self.driver.find_elements_by_name(value)

            elif type == "CLASS_NAME":
                elem = self.driver.find_elements_by_class_name(value)

            elif type == "LINK_TEXT":
                elem = self.driver.find_elements_by_link_text(value)

            elif type == "XPATH":
                elem = self.driver.find_elements_by_xpath(value)

            elif type == "CSS_SELECTOR":
                elem = self.driver.find_elements_by_css_selector(value)
            else:
                raise NameError("Please correct the type in function parameter")
        except Exception:
            raise ValueError("No such element found" + str(element))
        return elem

    def waitUntilFindElements(self, element):
        """
        http://selenium-python.readthedocs.io/api.html?highlight=wait.until
        """

        try:
            type = element[0]
            value = element[1]
            if type == "ID":
                elem = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.ID, value)
                    ))

            elif type == "NAME":
                elem = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.NAME, value)
                    ))

            elif type == "CLASS_NAME":
                elem = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, value)
                    ))

            elif type == "LINK_TEXT":
                elem = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.LINK_TEXT, value)
                    ))

            elif type == "XPATH":
                elem = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, value)
                    ))

            elif type == "CSS_SELECTOR":
                elem = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, value)
                    ))

            else:
                raise NameError("Please correct the type in function parameter")
        except Exception:
            raise ValueError("No such element found" + str(element))
        return elem

    def open(self, url):
        """
        Open web url

        Usage:
        self.open(url)
        """
        if url != "":
            self.driver.get(url)
        else:
            raise ValueError("please provide a base url")

    def type(self, element, text):
        """
        Operation input box.

        Usage:
        self.type(element,text)
        """
        element.send_keys(text)

    def enter(self, element):
        """
        Keyboard: hit return

        Usage:
        self.enter(element)
        """
        element.send_keys(Keys.RETURN)

    def click(self, element):
        """
        Click page element, like button, image, link, etc.
        """
        element.click()

    def quit(self):
        """
        Quit webdriver
        """
        self.driver.quit()

    def getAttribute(self, element, attribute):
        """
        Get element attribute
        """
        return element.get_attribute(attribute)

    def getText(self, element):
        """
        Get text of a web element

        """
        return element.text

    def getTitle(self):
        """
        Get window title
        """
        return self.driver.title

    def getCurrentUrl(self):
        """
        Get current url
        """
        return self.driver.current_url

    def getScreenshot(self, targetpath):
        """
        Get current screenshot and save it to target path
        """
        self.driver.get_screenshot_as_file(targetpath)

    def maximizeWindow(self):
        """
        Maximize current browser window
        """
        self.driver.maximize_window()

    def back(self):
        """
        Goes one step backward in the browser history.
        """
        self.driver.back()

    def forward(self):
        """
        Goes one step forward in the browser history.
        """
        self.driver.forward()

    def getWindowSize(self):
        """
        Gets the width and height of the current window.
        """
        return self.driver.get_window_size()

    def refresh(self):
        """
        Refresh current page
        """
        self.driver.refresh()
        # self.driver.switch_to()
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)

    def is_element_visible(self, element):
        try:
            the_element = EC.visibility_of_element_located(element)
            assert the_element(self.driver)
            flag = True
        except:
            flag = False
        return flag

    def page_source(self):
        return self.driver.page_source
