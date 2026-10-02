import requests
from bs4 import BeautifulSoup
import pandas as pd

# ၁။ Scraping လုပ်မည့် Target URL
url = "https://books.toscrape.com/"

print("ဝဘ်ဆိုက်သို့ ဆက်သွယ်နေပါသည်...")
response = requests.get(url)

# Unicode Character (Â£ ပြဿနာ) ရှင်းရန် Encoding သတ်မှတ်ခြင်း
response.encoding = 'utf-8'

if response.status_code == 200:
    print("ဝဘ်ဆိုက်မှ အချက်အလက်များ ဖတ်ယူ၍ ရရှိပါပြီ။\n")
    soup = BeautifulSoup(response.text, "html.parser")
    
    books_data = []
    product_pods = soup.find_all("article", class_="product_pod")
    
    for pod in product_pods:
        # စာအုပ် အမည် (Title) ယူခြင်း
        title_tag = pod.find("h3").find("a")
        title = title_tag["title"] if "title" in title_tag.attrs else title_tag.text.strip()
        
        # ဈေးနှုန်း (Price) ယူခြင်း
        price_tag = pod.find("p", class_="price_color")
        price = price_tag.text.strip() if price_tag else "N/A"
        
        # Â စာလုံးအပို ပါလာပါက ရှင်းထုတ်ခြင်း (Double Clean)
        price = price.replace("Â", "")
        
        books_data.append({
            "စာအုပ်အမည်": title,
            "ဈေးနှုန်း": price
        })
    
    # Data Frame အဖြစ် ပြောင်းလဲပြီး Excel သို့ သိမ်းဆည်းခြင်း
    df = pd.DataFrame(books_data)
    excel_filename = "books_list.xlsx"
    df.to_excel(excel_filename, index=False)
    
    print(f"--> အောင်မြင်ပါသည်! စာအုပ် {len(df)} အုပ်၏ စာရင်းနှင့် ဈေးနှုန်းများကို '{excel_filename}' ဖိုင်အဖြစ် သိမ်းဆည်းလိုက်ပါပြီဗျာ။")
    print("\n--- ထွက်ရှိလာသော Data နမူနာ ---")
    print(df.head())

else:
    print(f"ဝဘ်ဆိုက်သို့ ချိတ်ဆက်၍ မရပါ (Error Code: {response.status_code})")