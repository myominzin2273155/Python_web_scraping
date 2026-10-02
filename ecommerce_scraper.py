import requests
from bs4 import BeautifulSoup
import openpyxl
from deep_translator import GoogleTranslator

print("=== E-Commerce Book Scraping & Translation Started ===")

rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

raw_books_data = []
titles_to_translate = [] # Batch ဘာသာပြန်ရန် ခေါင်းစဉ်များ စုဆောင်းမည့် List

# ၁။ Web Scraping အရင်လုပ်၍ Data များ သိမ်းဆည်းမည်
for page in range(1, 2):
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    print(f"[+] Scraping Page {page}: {url}")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"[-] Page {page} ကို တောင်းဆို၍ မရပါ!")
        continue
        
    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.find_all('article', class_='product_pod')
    
    for book in books:
        title_en = book.h3.a['title']
        
        price_raw = book.find('p', class_='price_color').text
        price = float(price_raw.replace('£', '').replace('Â', '').strip())
        
        stock_raw = book.find('p', class_='instock availability').text.strip()
        stock_en = "In Stock" if "In stock" in stock_raw else "Out of Stock"
        
        rating_class = book.find('p', class_='star-rating')['class'][1]
        rating_num = rating_map.get(rating_class, 0)
        
        raw_books_data.append({
            "title_en": title_en,
            "price_gbp": price,
            "rating": rating_num,
            "stock_en": stock_en,
            "stock_my": "ပစ္စည်းရှိသည်" if stock_en == "In Stock" else "ပစ္စည်းကုန်နေသည်"
        })
        
        titles_to_translate.append(title_en)

# ၂။ စာအုပ် ခေါင်းစဉ် အားလုံးကို တစ်ပြိုင်နက်တည်း (Batch) မြန်မာလို ဘာသာပြန်မည်
print(f"\n[+] စာအုပ်ခေါင်းစဉ် ({len(titles_to_translate)}) ခုကို Batch Translation စတင်နေပါသည်...")
translated_titles = []

try:
    translator = GoogleTranslator(source='auto', target='my')
    # translate_batch ဖြင့် ၁ ခေါက်တည်း Google ဆီ ပို့ခြင်း
    translated_titles = translator.translate_batch(titles_to_translate)
    print("[✓] Batch Translation အောင်မြင်စွာ ပြီးဆုံးပါပြီ!")
except Exception as e:
    print(f"[-] Batch Translation Error: {e}")
    # Error တက်ပါက အင်္ဂလိပ် ခေါင်းစဉ်အတိုင်း အစားထိုးမည်
    translated_titles = titles_to_translate

# ၃။ Excel ဖိုင်ထဲသို့ ထည့်သွင်း သိမ်းဆည်းမည်
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "E-Commerce Scraping"

headers = [
    "No.", 
    "Book Title (English)", 
    "Book Title (Myanmar)", 
    "Price (£)", 
    "Rating (1-5)", 
    "Status (English)", 
    "Status (Myanmar)"
]
ws.append(headers)

for idx, (book, my_title) in enumerate(zip(raw_books_data, translated_titles), start=1):
    ws.append([
        idx,
        book["title_en"],
        my_title,
        book["price_gbp"],
        book["rating"],
        book["stock_en"],
        book["stock_my"]
    ])
    print(f"-> {book['title_en']} | မြန်မာဘာသာပြန်: {my_title}")

excel_filename = "ecommerce_books_translated.xlsx"
wb.save(excel_filename)
print(f"\n[✓] Data အားလုံးကို '{excel_filename}' အဖြစ် အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")