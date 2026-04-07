from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class BasketPage(BasePage):
    BASKET_URL = "https://www.idefix.com/sepetim"
    
    
    CHECKOUT_BTN = (By.XPATH, "//button[contains(., 'Alışverişi Tamamla')]")

    def go_to_basket(self):
        """Sepet sayfasına gider."""
        self.driver.get(self.BASKET_URL)
        print("[DEBUG] Sepet sayfasına gidildi.")
        time.sleep(3)

    def checkout(self):
        """Ödeme adımına geçer."""
        print("[DEBUG] 'Alışverişi Tamamla' butonuna basılıyor...")
        try:
            
            btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            time.sleep(1)
            btn.click()
            print("[DEBUG]  Ödemeye Geçiliyor.")
            time.sleep(4)
        except Exception as e:
            print(f"[HATA] Buton tıklanamadı: {e}")
            raise e