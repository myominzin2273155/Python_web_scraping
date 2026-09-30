from playwright.sync_api import sync_playwright
import pandas as pd
import time

print("=== Playwright Auto Login Scraping လေ့ကျင့်ခန်း ===\n")

with sync_playwright() as p:
    # ဘရောက်ဆာကို မျက်မြင် ပွင့်ပြအောင် headless=False ထားပါသည်
    browser = p.chromium.launch(headless=False, slow_mo=800)
    page = browser.new_page()
    
    # 1. Login Page သို့ သွားခြင်း
    login_url = "https://the-internet.herokuapp.com/login"
    print(f"၁။ Login စာမျက်နှာသို့ သွားနေပါသည်: {login_url}")
    page.goto(login_url)
    
    # 2. Username နှင့် Password ဖြည့်ခြင်း
    # (ဝဘ်ဆိုက်မှ သတ်မှတ်ထားသော စမ်းသပ် Username: tomsmith / Password: SuperSecretPassword!)
    print("၂။ Username နှင့် Password များကို အလိုအလျောက် ရိုက်ထည့်နေပါသည်...")
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    
    # 3. Login Button ကို Click နှိပ်ခြင်း
    print("၃။ Login ခလုတ်ကို နှိပ်လိုက်ပါပြီ...")
    page.locator("button[type='submit']").click()
    
    # စာမျက်နှာ Load ဖြစ်သည်အထိ ခဏစောင့်ခြင်း
    page.wait_for_load_state("networkidle")
    
    # 4. Login အောင်မြင် မအောင်မြင် စစ်ဆေးခြင်း
    # Login ဝင်သွားပါက စာမျက်နှာတွင် flash message ပေါ်လာပါမည်
    message_element = page.locator("#flash")
    message_text = message_element.inner_text().strip() if message_element else ""
    
    if "You logged into a secure area!" in message_text:
        print("\n--> 🎉 အောင်မြင်ပါသည်! Login အောင်မြင်စွာ ဝင်ရောက်သွားပါပြီဗျာ။")
        
        # 5. Secure Area ထဲမှ Data များ ဆွဲယူခြင်း
        header_text = page.locator("h2").inner_text()
        sub_heading = page.locator("h4.subheader").inner_text()
        
        print(f"တွေ့ရှိသော ခေါင်းစဉ်: {header_text}")
        print(f"တွေ့ရှိသော စာသား: {sub_heading}")
        
        # Login ဝင်ထားသော စာမျက်နှာအား Screenshot ရိုက်ယူခြင်း
        page.screenshot(path="logged_in_dashboard.png")
        print("--> Dashboard Screenshot ကို 'logged_in_dashboard.png' အဖြစ် သိမ်းဆည်းလိုက်ပါပြီ။")
        
        # Data ကို Excel သို့ ထုတ်ယူခြင်း
        data = [{
            "အခြေအနေ": "Login Success",
            "ခေါင်းစဉ်": header_text,
            "အသေးစိတ်စာသား": sub_heading
        }]
        df = pd.DataFrame(data)
        df.to_excel("login_result.xlsx", index=False)
        print("--> Data များကို 'login_result.xlsx' ထဲသို့ သိမ်းဆည်းပြီးပါပြီ။")
        
    else:
        print("\n--> ❌ Login ဝင်ရောက်ခြင်း မအောင်မြင်ပါဗျာ။")
    
    time.sleep(2)
    browser.close()

print("\nLesson 4.5 Auto Login သင်ခန်းစာ ပြီးဆုံးပါပြီဗျာ!")