import requests
import json
import os
from datetime import datetime

# API برای دریافت همه نمادها
url = "https://BrsApi.ir/Api/Tsetmc/AllSymbols.php?key=B5zgBWpp87rDlVHmL6Rx963abdhRaNhT"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Accept": "application/json"
}

SAVE_FILE = os.path.join(os.path.expanduser("~"), "market_data.json")

# درخواست API و گرفتن داده‌ها
response = requests.get(url, headers=headers)
data = response.json()  # لیست سهم‌ها

# گرفتن زمان API از اولین آیتم (فرض می‌کنیم همه داده‌ها همزمان هستند)
first_item_time_str = data[100].get("time")  # فیلد 'time' موجود است
print(first_item_time_str)
# تبدیل رشته به datetime.time
try:
    api_time = datetime.strptime(first_item_time_str, "%H:%M:%S").time()
except ValueError:
    api_time = datetime.strptime(first_item_time_str, "%H:%M").time()

# بررسی بعد از 12:30
if api_time.hour > 12 or (api_time.hour == 12 and api_time.minute >= 29):
    today = datetime.now().strftime("%Y-%m-%d")

    # خواندن فایل قبلی
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
    else:
        saved_data = {}

    if today not in saved_data:
        saved_data[today] = {}
        count=0
        for item in data:
            symbol = item.get("l18", "UNKNOWN")
            tvol = item.get("tvol", 0)
            plp = item.get("plp", 0)
            pl = item.get("pl", 0)
            pcp = item.get("pcp", 0)
            tmax = item.get("tmax",0)
            name =item.get("l18")

            if(pl==tmax and plp>0 and plp<5 and name[len(name)-1]!='2' and tvol>1000000):
                saved_data[today][symbol] = {
                    "tvol": tvol,
                    "name":name,
                    "plp": plp,
                    "pcp": pcp
                }
                count+=1
            

        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(saved_data, f, ensure_ascii=False, indent=4)
        print(f"✅ Market data for today ({today}) saved based on API time ({first_item_time_str}).")
    else:
        print(f"ℹ️ Market data for today ({today}) was already saved.")
else:
    print(f"⏱ API time ({first_item_time_str}) is before 12:30, data will not be saved.")
