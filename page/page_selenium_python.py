from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)


class MainPage(BasePage):
    def repeat_next(self):
        while True:
            try:
                next_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.CLASS_NAME, 'float-right'))
                )
                pages = self.driver.find_elements(By.CSS_SELECTOR, '.current.reference.internal')
                for page in pages:
                    print("\n" + page.get_attribute('text'))
                next_button.click()
            except NoSuchElementException:
                print("End of page")
                break
            except TimeoutException:
                print("Timeout error...")
                break
