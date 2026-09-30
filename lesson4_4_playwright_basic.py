from playwright.sync_api import sync_playwright
import pandas as pd

print("Playwright ဖြင့် ဘရောက်ဆာကို အလိုအလျောက် စတင်ဖွင့်လှစ်နေပါသည်...\n")

with sync_playwright() as p:
    # Chromium ဘရောက်ဆာကို မျက်မြင်ပွင့်လာအောင် ဖွင့်ခြင်း (headless=False ထားပါက ဘရောက်ဆာပွင့်လာသည်ကို မြင်ရမည်)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # ဝဘ်ဆိုက်သို့ သွားရောက်ခြင်း
    url = "https://books.toscrape.com/"
    page.goto(url)
    
    # စာမျက်နှာ ခေါင်းစဉ်ကို ဆွဲယူခြင်း
    page_title = page.title()
    print(f"ဝဘ်ဆိုက် ခေါင်းစဉ်: {page_title}")
    
    # စာအုပ်အကွက်များ အားလုံးကို ရှာဖွေခြင်း
    # Playwright ၏ Selector သုံး၍ <article class="product_pod"> ကို ရှာခြင်း
    product_pods = page.query_selector_all("article.product_pod")
    print(f"တွေ့ရှိသော စာအုပ် အရေအတွက်: {len(product_pods)} အုပ်\n")
    
    books_data = []
    
    for pod in product_pods:
        # စာအုပ် အမည်
        title_element = pod.query_selector("h3 a")
        title = title_element.get_attribute("title") if title_element else "N/A"
        
        # ဈေးနှုန်း
        price_element = pod.query_selector("p.price_color")
        price = price_element.inner_text().replace("Â", "") if price_element else "N/A"
        
        books_data.append({
            "စာအုပ်အမည်": title,
            "ဈေးနှုန်း": price
        })
    
    # စခရင်ရှော့ (Screenshot) တစ်ပုံ အလိုအလျောက် ရိုက်ယူသိမ်းဆည်းခြင်း
    page.screenshot(path="website_screenshot.png")
    print("--> ဝဘ်ဆိုက်၏ Screenshot ကို 'website_screenshot.png' အဖြစ် သိမ်းဆည်းလိုက်ပါပြီ။")
    
    # ဘရောက်ဆာကို ပြန်ပိတ်ခြင်း
    browser.close()

# Pandas ဖြင့် Excel သို့ သိမ်းဆည်းခြင်း
df = pd.DataFrame(books_data)
excel_filename = "playwright_books.xlsx"
df.to_excel(excel_filename, index=False)

print(f"--> Playwright ဖြင့် ဆွဲယူထားသော စာအုပ် {len(df)} အုပ်၏ Data ကို '{excel_filename}' အဖြစ် သိမ်းဆည်းပြီးပါပြီဗျာ!")