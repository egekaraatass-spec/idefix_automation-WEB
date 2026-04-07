from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class LoginPage(BasePage):
    URL = "https://www.idefix.com/giris"

    EMAIL_INPUT     = (By.NAME, "emailOrPhone")
    PASSWORD_INPUT  = (By.NAME, "password")

    CONTINUE_BUTTON = (By.XPATH, "//button[@type='submit']")
    LOGIN_BUTTON    = (By.XPATH, "//button[@type='submit']")  

    POPUP_CLOSE = (By.XPATH, (
        "//button[contains(@class,'modal-close')]"
        " | //button[contains(@class,'close-button')]"
        " | //button[@aria-label='Kapat']"
        " | //button[@aria-label='Close']"
        " | //*[contains(@class,'popup')]//button[contains(@class,'close')]"
    ))

    def go_to(self):
        self.driver.get(self.URL)
        time.sleep(2)

    def dismiss_popup_if_present(self, timeout: int = 5):
        try:
            short_wait = WebDriverWait(self.driver, timeout)
            btn = short_wait.until(EC.element_to_be_clickable(self.POPUP_CLOSE))
            self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(1)
        except Exception:
            pass

    def enter_email(self, email: str):
        field = self.wait.until(EC.element_to_be_clickable(self.EMAIL_INPUT))
        field.clear()
        field.send_keys(email)

    def click_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        #DOM
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        time.sleep(1)

    def enter_password(self, password: str):
        field = self.wait.until(EC.element_to_be_clickable(self.PASSWORD_INPUT))
        field.clear()
        field.send_keys(password)

    def click_login(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(4) 
