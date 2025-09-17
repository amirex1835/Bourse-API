import requests
from statistics import mean

# API_KEY = "B5zgBWpp87rDlVHmL6Rx963abdhRaNhT"
url = f"https://BrsApi.ir/Api/Tsetmc/AllSymbols.php?key=B5zgBWpp87rDlVHmL6Rx963abdhRaNhT"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Accept": "application/json"
}

response = requests.get(url, headers=headers)
data = response.json()  # لیست سهم‌ها
# 1. گروه‌بندی بر اساس cs_id
groups = {}
for item in data:
    group_id = item.get("cs_id", "UNKNOWN")
    
    # حذف گروه 68
    if group_id == 68:
        continue

    symbol = item.get("l18", "UNKNOWN")
    plc = item.get("plc", 0)   # تغییر آخرین قیمت
    plp = item.get("plp", 0)   # درصد تغییر آخرین قیمت
    pc = item.get("pc", 0)     # قیمت پایانی
    tvol = item.get("tvol", 0) # حجم معاملات

    # تبدیل به float
    try:
        plc = float(plc)
    except:
        plc = 0
    try:
        plp = float(plp)
    except:
        plp = 0
    try:
        pc = float(pc)
    except:
        pc = 0
    try:
        tvol = float(tvol)
    except:
        tvol = 0

    # فقط سهم‌های معامله شده
    if tvol <= 1000000:
        continue

    if group_id not in groups:
        groups[group_id] = []
    groups[group_id].append({"symbol": symbol, "plc": plc, "plp": plp, "pc": pc})

# 2. محاسبه میانگین و نمایش سهم‌ها بالاتر از میانگین
count=0
for g, items in groups.items():
    if not items:
        continue

    mean_plp = mean([it["plp"] for it in items])

    # فقط سهم‌هایی که بالاتر از میانگین هستند
    above_mean = [it for it in items if it["plp"] > mean_plp]

    if not above_mean:
        continue  # گروهی که هیچ سهمی بالاتر از میانگین ندارد چاپ نشود

    print(f"Group ID: {g}, Mean Last Price Change %: {mean_plp:.2f}%")
    print("Symbols above mean:")
    for it in above_mean:
        count+=1
        print(f"Namad: {it['symbol']}, Last Change: {it['plc']}, Last % Change: {it['plp']}%, Close Price: {it['pc']}")
    print("------")
print(count)