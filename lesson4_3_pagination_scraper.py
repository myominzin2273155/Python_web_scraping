import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# ၁။ စတင်မည့် Base URL သတ်မှတ်ခြင်း
base_url = "https://books.toscrape.com/catalogue/"
current_page_url = "https://books.toscrape.com/catalogue/page-1.html"

all_books = []
page_count = 1

print("=== စာမျက်နှာ အားလုံးမှ Data များကို အလိုအလျောက် စတင် ဆွဲယူနေပါသည် ===\n")

while current_page_url:
    print(f"စာမျက်နှာ ({page_count}) ကို ဖတ်ယူနေပါသည်: {current_page_url}")
    
    response = requests.get(current_page_url)
    response.encoding = 'utf-8'
    
    if response.status_code != 200:
        print(f"စာမျက်နှာ ဖတ်၍ မရတော့ပါ (Error: {response.status_code})")
        break
        
    soup = BeautifulSoup(response.text, "html.parser")
    product_pods = soup.find_all("article", class_="product_pod")
    
    for pod in product_pods:
        # စာအုပ် အမည်
        title_tag = pod.find("h3").find("a")
        title = title_tag["title"] if "title" in title_tag.attrs else title_tag.text.strip()
        
        # ဈေးနှုန်း
        price_tag = pod.find("p", class_="price_color")
        price = price_tag.text.strip().replace("Â", "") if price_tag else "N/A"
        
        all_books.append({
            "စာမျက်နှာ": page_count,
            "စာအုပ်အမည်": title,
            "ဈေးနှုန်း": price
        })
    
    # ၂။ 'Next' Button ရှိမရှိ စစ်ဆေးခြင်း
    next_button = soup.find("li", class_="next")
    if next_button and next_button.find("a"):
        next_page_rel_path = next_button.find("a")["href"]
        # Next link ရဲ့ Path အသစ်ကို လိပ်စာအပြည့် ပြန်ဆင်ခြင်း
        current_page_url = base_url + next_page_rel_path
        page_count += 1
        time.sleep(0.5)  # ဝဘ်ဆိုက် Server မလေးစေရန် 0.5 စက္ကန့် ခဏနားပေးခြင်း
    else:
        print("\n--> နောက်ဆုံး စာမျက်နှာသို့ ရောက်ရှိသွားပါပြီ။")
        current_page_url = None  # Loop ကို ရပ်တန့်ရန်

# ၃။ ရရှိလာသော Data အားလုံးကို Excel ဖိုင်အဖြစ် သိမ်းဆည်းခြင်း
df = pd.DataFrame(all_books)
excel_filename = "all_books_pages.xlsx"
df.to_excel(excel_filename, index=False)

print(f"\n==========================================")
print(f"စုစုပေါင်း စာမျက်နှာ: {page_count} Page")
print(f"စုစုပေါင်း ရရှိသော စာအုပ် အရေအတွက်: {len(df)} အုပ်")
print(f"Data များကို '{excel_filename}' ဖိုင်ထဲသို့ အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီဗျာ!")
print(f"==========================================")