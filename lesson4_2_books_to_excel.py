import requests
from bs4 import BeautifulSoup
import pandas as pd

# ၁။ Scraping လုပ်မည့် Target URL
url = "https://books.toscrape.com/"

print("ဝဘ်ဆိုက်သို့ ဆက်သွယ်နေပါသည်...")
response = requests.get(url)

if response.status_code == 200:
    print("ဝဘ်ဆိုက်မှ အချက်အလက်များ ဖတ်ယူ၍ ရရှိပါပြီ။\n")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # စာအုပ်တစ်အုပ်စီ၏ အချက်အလက် သိမ်းဆည်းရန် List
    books_data = []
    
    # Books to Scrape တွင် စာအုပ်တစ်အုပ်စီကို <article class="product_pod"> ထဲတွင် ထည့်ထားပါသည်
    product_pods = soup.find_all("article", class_="product_pod")
    
    for pod in product_pods:
        # စာအုပ် အမည် (Title) ယူခြင်း
        title_tag = pod.find("h3").find("a")
        title = title_tag["title"] if "title" in title_tag.attrs else title_tag.text.strip()
        
        # ဈေးနှုန်း (Price) ယူခြင်း (p class="price_color" ထဲတွင် ရှိပါသည်)
        price_tag = pod.find("p", class_="price_color")
        price = price_tag.text.strip() if price_tag else "N/A"
        
        # Dictionary အဖြစ် သိမ်းဆည်းခြင်း
        books_data.append({
            "စာအုပ်အမည်": title,
            "ဈေးနှုန်း": price
        })
    
    # ၂။ Data Frame အဖြစ် ပြောင်းလဲခြင်း
    df = pd.DataFrame(books_data)
    
    # ၃။ Excel ဖိုင်အဖြစ် အလိုအလျောက် သိမ်းဆည်းခြင်း
    excel_filename = "books_list.xlsx"
    df.to_excel(excel_filename, index=False)
    
    print(f"--> အောင်မြင်ပါသည်! စာအုပ် {len(df)} အုပ်၏ စာရင်းနှင့် ဈေးနှုန်းများကို '{excel_filename}' ဖိုင်အဖြစ် သိမ်းဆည်းလိုက်ပါပြီဗျာ။")
    print("\n--- ထွက်ရှိလာသော Data နမူနာ ---")
    print(df.head())

else:
    print(f"ဝဘ်ဆိုက်သို့ ချိတ်ဆက်၍ မရပါ (Error Code: {response.status_code})")