# خواندن فایل قبلی
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
    else:
        saved_data = {}