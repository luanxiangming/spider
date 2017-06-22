from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from page.BasePage import BasePage


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
                    ("\n" + page.get_attribute('text'))
                self.click(next_button)
            except NoSuchElementException:
                print("End of page")
                break
            except TimeoutException:
                print("Timeout error...")
                break
