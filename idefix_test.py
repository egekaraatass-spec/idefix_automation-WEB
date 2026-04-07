import time
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.results_page import ResultsPage
from pages.basket_page import BasketPage
from pages.payment_page import PaymentPage


TEST_EMAIL    = "egekaraatass@gmail.com"
TEST_PASSWORD = "Gs123456!"

def test_login_search_and_checkout(driver):
    
    home = HomePage(driver)
    home.go_to()
    home.dismiss_popup_if_present()

   
    login = LoginPage(driver)
    login.go_to()
    login.dismiss_popup_if_present()

    
    login.enter_email(TEST_EMAIL)
    login.click_continue()

    
    login.enter_password(TEST_PASSWORD)
    login.click_login()
    time.sleep(3)

    
    assert "giris" not in driver.current_url, "Giriş başarısız, hâlâ login sayfasındasın."

   
    home.search("kitap")

    
    results = ResultsPage(driver)
    results.add_items_to_basket(2)

    
    basket = BasketPage(driver)
    basket.go_to_basket()
    basket.checkout()

   
    payment = PaymentPage(driver)
    
    
    payment.open_credit_card_section()
    
   
    payment.fill_fake_card_details()
    
   
    payment.check_agreements_and_pay()

    print("\n[DEBUG] başarıyla tamamlandı!")
    time.sleep(5)