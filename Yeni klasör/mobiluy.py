from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Appium'un Ayarları
options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name = "Pixel 7"
options.platform_version = "14.0"
options.app_package = "tr.com.idefix.android"
options.app_activity = ".MainActivity"
options.no_reset = True
options.auto_grant_permissions = False
options.print_page_source_on_find_failure = True

APPIUM_SERVER_URL = "http://localhost:4723"

EMAIL = "sena.aruk9@gmail.com"
PASSWORD = "İdefix.."

def wait_and_click(driver, by, value, timeout=10):
    print(f"[DENENİYOR] click -> {by} | {value}")
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()
    print(f"[TIKLANDI] {by} | {value}")

def is_present(driver, by, value, timeout=5): #elemanın ekranda var olup olmadığını kontrol eder
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False

def click_first(driver, locator_list, timeout=10, name="element"):
    last_error = None
    for by, value in locator_list:
        try:
            print(f"[DENENİYOR] {name} -> {by} | {value}")
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            print(f"[tıklandı] {name}")
            return element
        except Exception as e:
            last_error = e
            print(f"[bulunamadı] {name} -> {by} | {value}")
    raise Exception(f"{name} bulunamadı. Son hata: {last_error}")

def type_first(driver, locator_list, text, timeout=10, name="element"):
    last_error = None
    for by, value in locator_list:
        try:
            print(f"[deneniyor] {name} -> {by} | {value}")
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            element.clear()
            element.send_keys(text)
            print(f"[şifre yazıldı] {name}")
            return element
        except Exception as e:
            last_error = e
            print(f"[bulunamadı] {name} -> {by} | {value}")
    raise Exception(f"{name} bulunamadı. Son hata: {last_error}")

def ensure_idefix_open(driver): #uygualama gerçekten açıldı mı kontrolü
    print("0) idefix uygulaması açılıyor")

    try:
        driver.activate_app("tr.com.idefix.android")
        print("idefix uygulaması açıldı")
        time.sleep(5)
    except Exception as e:
        print("uygulama açılması başarısız", e)
        time.sleep(8)
        print("idefix açıldı")

    idefix_open = False
    try:
        if is_present(driver, AppiumBy.XPATH, "//*[contains(@text,'Hesab')]", timeout=3):
            idefix_open = True
    except Exception:
        pass

    if idefix_open:
        print("idefix açık görünüyor")
        return

    time.sleep(5)
    print("idefix açılma tamamlandı")

def main():
    driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)

    try:
        print("Test başladı")

        # Önce uygulamayı gerçekten aç
        ensure_idefix_open(driver)

        # 1. Popup kontrol
        print("1) Popup kontrolü yapılıyor")
        popup_locators = [
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"),
            (AppiumBy.ID, "android:id/button1"),
            (AppiumBy.XPATH, "//*[@text='İzin ver']"),
        ]

        for by, value in popup_locators:
            if is_present(driver, by, value, timeout=2):
                print("Popup bulundu")
                wait_and_click(driver, by, value)
                break

        # 2. Hesabım tıklanıyor
        print("2) Hesabım'a tıklanıyor")
        click_first(driver, [
            (AppiumBy.ACCESSIBILITY_ID, "Hesabım, sekme 5/5"),
            (AppiumBy.XPATH, '//*[@content-desc="Hesabım, Sekme 5/5"]'),
            (AppiumBy.XPATH, '//*[contains(@content-desc,"Hesabım")]'),
            (AppiumBy.XPATH, '//*[contains(@content-desc,"Sekme 5/5")]'),
        ], timeout=12, name="Hesabım")

        # 3. Email
        print("3) Email giriliyor")
        type_first(driver, [
            (AppiumBy.XPATH, '//android.widget.EditText[1]'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)'),
        ], EMAIL, name="Email")

        # 4. Devam
        print("4) Devam et'e tıklanıyor")
        click_first(driver, [
            (AppiumBy.ACCESSIBILITY_ID, "Devam Et"),
            (AppiumBy.XPATH, '//*[contains(@text,"Devam")]'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Devam")'),
        ], name="Devam")

        # 5. Şifre
        print("5) Şifre giriliyor")
        type_first(driver, [
            (AppiumBy.XPATH, '//android.widget.EditText[1]'),
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)'),
        ], PASSWORD, name="Şifre")

        # Klavyeyi kapat
        try:
            driver.hide_keyboard()
            print("Klavye kapatıldı")
        except Exception as e:
            print("Klavye kapatılamadı:", e)

        time.sleep(2)

        # 6. Giriş
        print("6) Giriş yapılıyor")
        print("giriş yap tıklanıyor")

        driver.execute_script("mobile: clickGesture", {
            "x": 540,
            "y": 1172
        })

        time.sleep(3)
        print("giriş yap tamamlandı")

    except Exception as e:
        print("HATA:", e)
        try:
            print(driver.page_source)
        except Exception as inner_e:
            print("page_source alınamadı:", inner_e)

    finally:
        try:
            driver.terminate_app("tr.com.idefix.android")
            print("Uygulama kapatıldı")
            time.sleep(2)
        except Exception as e:
            print("Uygulama kapatılamadı:", e)

        try:
            driver.quit()
            print("Driver kapandı")
        except Exception as e:
            print("Driver kapatılamadı:", e)

if __name__ == "__main__":
    main()