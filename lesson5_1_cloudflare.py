from curl_cffi import requests

print("=== Cloudflare Bypass Test with curl_cffi ===")

# Cloudflare ခံထားသော သို့မဟုတ် Browser Fingerprint စစ်ဆေးသော ဝဘ်ဆိုက်
url = "https://nowsecure.nl" 

try:
    # impersonate="chrome120" ဟု ထည့်ပေးလိုက်ခြင်းဖြင့် 
    # Python က Chrome Browser အစစ်အတိုင်း တရားဝင် ယောင်ဆောင်ပေးသွားမည်ဖြစ်ပါသည်
    response = requests.get(url, impersonate="chrome120", timeout=15)
    
    if response.status_code == 200:
        print("[✓] Cloudflare Security ကို အောင်မြင်စွာ ရှောင်ကွင်း (Bypass) ပြုလုပ်နိုင်ခဲ့ပါပြီ!")
        print(f"[+] Status Code: {response.status_code}")
        print(f"[+] Web Title/Content snippet: {response.text[:200]}")
    else:
        print(f"[-] Block ထိနေပါသေးသည်။ Status Code: {response.status_code}")

except Exception as e:
    print(f"[-] Connection Error: {e}")