from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time

class PaymentPage(BasePage):
   
    CREDIT_CARD_TAB_BTN = (By.XPATH, "//button[contains(., 'Kredi Kartı / Banka Kartı ile Öde')] | //*[contains(text(), 'Kredi Kartı / Banka Kartı ile Öde')]/following::button[1]")
    
  
    CARD_NUMBER_INPUT = (By.XPATH, "//*[contains(text(), 'Kart Numarası')]/parent::*//input | //input[contains(@name, 'cardNumber')]")
    CARD_NAME_INPUT   = (By.XPATH, "//*[contains(text(), 'İsim-Soyisim')]/parent::*//input | //input[contains(@name, 'cardHolderName')]")
    EXPIRY_DATE_INPUT = (By.XPATH, "//*[contains(text(), 'Kullanma Tarihi')]/parent::*//input | //input[contains(@name, 'expireDate')]")
    CVV_INPUT         = (By.XPATH, "//*[contains(text(), 'Güvenlik Kodu')]/parent::*//input | //input[contains(@name, 'cvv')]")

   
    SECURE_3D_CHECKBOX = (By.XPATH, "//*[contains(text(), '3D secure')]/ancestor::label//input | //*[contains(text(), '3D secure')]/preceding-sibling::input")
    TERMS_CHECKBOX     = (By.XPATH, "//*[contains(text(), 'Ön Bilgilendirme')]/ancestor::label//input | //*[contains(text(), 'Ön Bilgilendirme')]/preceding-sibling::input")
    FINAL_PAY_BTN      = (By.XPATH, "//button[contains(normalize-space(), 'Onayla ve Bitir')]")

    def open_credit_card_section(self):
        """Kredi Kartı / Banka Kartı ile Öde sekmesini açar."""
        print("\n[DEBUG] Kredi Kartı ödeme alanı açılıyor...")
        try:
            time.sleep(4)
            tab_btn = self.wait.until(EC.element_to_be_clickable(self.CREDIT_CARD_TAB_BTN))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_btn)
            time.sleep(1)
            tab_btn.click()
            print("[DEBUG]  Kredi kartı sekmesine başarıyla tıklandı.")
            time.sleep(2) 
            
            # Formun görünmesi için hafif aşağı kaydır
            self.driver.execute_script("window.scrollBy(0, 350);")
            time.sleep(1)
        except Exception as e:
            self.driver.save_screenshot("kredi_karti_sekmesi_hatasi.png")
            print(f"[HATA] Kredi kartı sekmesi açılamadı: {e}")
            raise e

    def fill_fake_card_details(self):
        """Kart bilgilerini doldurur."""
        print("[DEBUG] Kart bilgileri giriliyor...")
        try:
            self.type_text(self.CARD_NUMBER_INPUT, "4545454545454545")
            time.sleep(0.5)
            self.type_text(self.CARD_NAME_INPUT, "EGE KARAATA")
            time.sleep(0.5)
            self.type_text(self.EXPIRY_DATE_INPUT, "1228") 
            time.sleep(0.5)
            self.type_text(self.CVV_INPUT, "999")
            time.sleep(1)
            print("[DEBUG] Kart bilgileri dolduruldu.")
        except Exception as e:
            print(f"[HATA] Kart verileri girilemedi: {e}")
            raise e

    def check_agreements_and_pay(self):
        """Sözleşmeleri onaylar ve Onayla ve Bitir butonuna basar."""
        print("[DEBUG] Sözleşmeler onaylanıp kasaya vuruluyor...")
        try:
            # 3D Secure Tikle 
            try:
                secure_cb = self.wait.until(EC.presence_of_element_located(self.SECURE_3D_CHECKBOX))
                self.driver.execute_script("arguments[0].click();", secure_cb)
                print("[DEBUG]  3D Secure onaylandı.")
            except Exception as e:
                print(f"[DEBUG] 3D Secure checkbox bulunamadı veya zorunlu değil: {e}")

            time.sleep(0.5)

            # Ön Bilgilendirme / Sözleşme Tikla
            try:
                
                REVERSE_TERMS_XPATH = "//button[contains(normalize-space(), 'Onayla ve Bitir')]/preceding::input[@type='checkbox'][1]"
                
                terms_cb = self.wait.until(EC.presence_of_element_located((By.XPATH, REVERSE_TERMS_XPATH)))
                
                
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", terms_cb)
                time.sleep(1)
                
                
                self.driver.execute_script("arguments[0].click();", terms_cb)
                print("[DEBUG] Ön Bilgilendirme formları onaylandı.")
            except Exception as e:
                self.driver.save_screenshot("sozlesme_bulunamadi.png")
                print(f"[HATA] Sözleşme checkbox bulunamadı: {e}")
                raise e
            
            time.sleep(1)

           
            print("[DEBUG] 'Onayla ve Bitir' butonuna aslanlar gibi basılıyor...")
            pay_btn = self.wait.until(EC.element_to_be_clickable(self.FINAL_PAY_BTN))
            
            
            pay_btn.click()
            print("[DEBUG] Ödeme isteği gönderildi!")
            
        except Exception as e:
            self.driver.save_screenshot("final_odeme_hatasi.png")
            print(f"[HATA] Onayla ve bitir işleminde patladık: {e}")
            raise e