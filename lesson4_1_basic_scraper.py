import requests
from bs4 import BeautifulSoup

# ၁။ စမ်းသပ်မည့် ဝဘ်ဆိုက် URL (Web Scraping လေ့ကျင့်ရန် သီးသန့်ပြုလုပ်ထားသော Free Site)
url = "https://books.toscrape.com/"

print("ဝဘ်ဆိုက်သို့ အချက်အလက်များ လှမ်းတောင်းနေပါသည်...")

# ၂။ requests ဖြင့် ဝဘ်ဆိုက်ဆီ ရောက်အောင် သွားခြင်း
response = requests.get(url)

# HTTP Status Code စစ်ဆေးခြင်း (200 ဆိုလျှင် အောင်မြင်ပါသည်)
if response.status_code == 200:
    print("ဝဘ်ဆိုက်သို့ ချိတ်ဆက်မှု အောင်မြင်ပါသည်။\n")
    
    # ၃။ HTML Code များကို BeautifulSoup ဖြင့် Parse လုပ်ခြင်း (ဖတ်ရှုရလွယ်အောင် ပြင်ခြင်း)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # ၄။ Web Page ရဲ့ ခေါင်းစဉ် (Title) ကို ဆွဲယူခြင်း
    page_title = soup.title.text.strip()
    print(f"ဝဘ်ဆိုက် ခေါင်းစဉ်: {page_title}")
    print("-" * 40)
    
    # ၅။ စာအုပ် ခေါင်းစဉ် (Book Titles) များကို လိုက်ရှာယူခြင်း
    # Books to Scrape ဝဘ်ဆိုက်မှာ စာအုပ်ခေါင်းစဉ်တွေက <h3> အကွက်ထဲက <a> tag ထဲမှာ ရှိပါတယ်
    books = soup.find_all("h3")
    
    print(f"တွေ့ရှိသော စာအုပ် အရေအတွက်: {len(books)} အုပ်\n")
    print("စာအုပ် အမည်များ -")
    
    for index, book in enumerate(books, 1):
        # <h3> ထဲက <a> tag ကို ရှာပြီး title သို့မဟုတ် စာသားကို ယူခြင်း
        title = book.find("a")["title"]
        print(f"{index}။ {title}")

else:
    print(f"ဝဘ်ဆိုက်သို့ ချိတ်ဆက်၍ မရပါ (Error Code: {response.status_code})")