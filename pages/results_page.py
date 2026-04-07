from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import time

class ResultsPage(BasePage):
    
    def add_items_to_basket(self, count=2):
        
        print(f"\n[DEBUG] {count} farklı ürün sepete ekleniyor...")
        time.sleep(4) 
        
        added_count = 0
        
        for i in range(15):
            if added_count >= count:
                break
                
            try:
                
                cards = self.driver.find_elements(By.XPATH, "//section/div/div")
                if i >= len(cards):
                    break
                    
                card = cards[i]
                
                
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", card)
                time.sleep(1)
                
                
                ActionChains(self.driver).move_to_element(card).perform()
                time.sleep(1)

                
                btns = self.driver.find_elements(By.XPATH,
                    "//button[.//*[contains(text(),'Sepete Ekle')] or contains(text(),'Sepete Ekle')]"
                )
                
                
                visible_btns = [b for b in btns if b.is_displayed()]
                
                if visible_btns:
                    visible_btns[0].click()
                    added_count += 1
                    print(f"[DEBUG] {added_count}. ürün eklendi (Kart İndeksi: {i}).")
                    time.sleep(4) 
                else:
                    print(f"[DEBUG] Kart {i} üzerinde buton görünür olmadı, atlanıyor...")
                    
            except Exception as e:
                
                print(f"[DEBUG] Kart {i} hataya düştü, atlanıyor. Hata: {type(e).__name__}")
                continue

        if added_count < count:
            raise Exception(f"Sadece {added_count} ürün eklenebildi, hedef {count} idi!")