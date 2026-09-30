from playwright.sync_api import sync_playwright
import time

print("Playwright Interaction Test အား စတင်နေပါသည်...\n")

with sync_playwright() as p:
    # ဘရောက်ဆာ ဖွင့်မည်
    browser = p.chromium.launch(headless=False, slow_mo=1000) # slow_mo=1000 ထည့်ထားသဖြင့် လှုပ်ရှားမှုများကို ၁ စက္ကန့် စီ ဖြေးဖြေးချင်း မြင်ရပါမည်
    page = browser.new_page()
    
    # Python ပေါ်တိုဆိုက်သို့ သွားမည်
    page.goto("https://www.python.org")
    print("Python.org သို့ ရောက်ရှိပါပြီ။")
    
    # 1. Search Box ထဲသို့ 'playwright' ဟု စာရိုက်ထည့်ခြင်း
    # CSS Selector id="id-search-field" ကို သုံးထားသည်
    search_input = page.locator("#id-search-field")
    search_input.fill("playwright")
    print("Search Box ထဲတွင် 'playwright' ဟု ရိုက်ထည့်လိုက်ပါပြီ။")
    
    # 2. Go ခလုတ် (Button) ကို နှိပ်ခြင်း
    go_button = page.locator("#submit")
    go_button.click()
    print("GO ခလုတ်ကို Click နှိပ်လိုက်ပါပြီ။")
    
    # စာမျက်နှာ လင်းလာသည်အထိ ခဏစောင့်ခြင်း
    page.wait_for_load_state("networkidle")
    
    # ရလဒ် စာမျက်နှာ ခေါင်းစဉ်နှင့် ရလဒ်များ တွေ့မတွေ့ စစ်ဆေးခြင်း
    print(f"လက်ရှိ ရောက်ရှိနေသော စာမျက်နှာ Title: {page.title()}")
    
    # Search Results Screenshot ရိုက်ယူခြင်း
    page.screenshot(path="python_search_results.png")
    print("--> ရှာဖွေမှုရလဒ် Screenshot ကို 'python_search_results.png' ဟု သိမ်းဆည်းလိုက်ပါပြီ။")
    
    time.sleep(2)
    browser.close()

print("\nInteraction လေ့ကျင့်ခန်း အောင်မြင်စွာ ပြီးဆုံးပါပြီဗျာ!")