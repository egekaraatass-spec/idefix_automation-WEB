from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time


class HomePage(BasePage):
    SEARCH_BOX   = (By.ID, "headerSearch-d")
    POPUP_REJECT = (By.XPATH, "//button[normalize-space()='Hayır']")

    def go_to(self):
        self.driver.get("https://www.idefix.com")
        time.sleep(3)

    def dismiss_popup_if_present(self):
        try:
            short_wait = WebDriverWait(self.driver, 5)
            btn = short_wait.until(EC.element_to_be_clickable(self.POPUP_REJECT))
            btn.click()
            time.sleep(1)
        except:
            pass

    def search(self, keyword):
        self.dismiss_popup_if_present()
        self.type_text(self.SEARCH_BOX, keyword)
        self.find(self.SEARCH_BOX).send_keys(Keys.ENTER)