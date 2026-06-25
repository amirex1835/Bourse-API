import json
import os
import requests
import time

SAVE_FILE = "/storage/emulated/0/Download/market_data.json"

while True:
    try:
        # خواندن فایل
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        # گرفتن اولین کلید (تاریخ)
        first_date = list(json_data.keys())[0]

        # داده‌های آن تاریخ
        data_for_date = json_data[first_date]

        # API برای دریافت همه نمادها
        url = "https://BrsApi.ir/Api/Tsetmc/AllSymbols.php?key=B5zgBWpp87rDlVHmL6Rx963abdhRaNhT"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
            "Accept": "application/json"
        }

        # درخواست API و گرفتن داده‌ها
        response = requests.get(url, headers=headers)
        data = response.json()  # لیست سهم‌ها

        # بررسی شرایط
        for namad in data_for_date:
            for item in data:
                if namad == item['l18']:
                    if item['qo1'] == item['pd1'] and item['pd1'] < item['py']:
                        print(namad)

    except Exception as e:
        print("خطا رخ داد:", e)

    # هر 12 ثانیه یک بار
    time.sleep(12)
