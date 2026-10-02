import requests
from bs4 import BeautifulSoup

print("=== User-Agent Header & Anti-Blocking Test ===")

# ၁။ Real Browser ၏ Header အချက်အလက်များ အတုဖန်တီးခြင်း
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

# 2. Target URL (HTTP Status / Header စစ်ဆေးပေးသည့် HTTPBin Site)
target_url = "https://httpbin.org/headers"

try:
    # headers=headers ကို ပူးတွဲပေးပို့ခြင်းဖြင့် Browser အစစ်မှ ဝင်ရောက်သည်ဟု ထင်မှတ်စေခြင်း
    response = requests.get(target_url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        print("[✓] Web Page သို့ အောင်မြင်စွာ ချိတ်ဆက်ပြီးပါပြီ!\n")
        print("--- Web Server သို့ ရောက်ရှိသွားသော ကျွန်ုပ်တို့၏ Request Headers ---")
        print(response.text)
    else:
        print(f"[-] Access Denied! Status Code: {response.status_code}")

except Exception as e:
    print(f"[-] Error: {e}")