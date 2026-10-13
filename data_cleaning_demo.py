import pandas as pd

def clean_scraped_data_pro():
    print("၁။ မသပ်ရပ်သေးသော စာရင်းအချက်အလက်များကို ဖန်တီးနေပါပြီ...")
    
    raw_data = {
        'Book Name': ['  Python Programming  \n', 'Data Science 101', 'Python Programming', '  Machine Learning ', None],
        'Price': ['$45.00', ' $30.50 ', ' $45.00 ', 'Free', '$20.00'],
        'Stock Status': ['In Stock', 'Out of Stock', 'In Stock', 'In Stock', '  ']
    }
    
    df = pd.DataFrame(raw_data)
    
    print("\n--- မသပ်ရပ်သေးသော ပုံစံ (Before Cleaning) ---")
    print(df)
    
    print("\n၂။ ဒေတာများကို ပိုမိုစနစ်တကျ သန့်စင်နေပါပြီ...")
    
    # အဆင့် (က) - ပထမဦးဆုံး NaN (Missing values) များကို ဖယ်ရှားခြင်း
    df = df.dropna(subset=['Book Name'])
    
    # အဆင့် (ခ) - Book Name ထဲမှ မလိုအပ်သော Space များနှင့် Newline များကို ဖယ်ရှားခြင်း
    df['Book Name'] = df['Book Name'].str.strip()
    
    # အဆင့် (ဂ) - Price ထဲမှ ဒေါ်လာသင်္ကေတ ($) နှင့် Space များကို ဦးစွာ ရှင်းလင်းခြင်း
    df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False).str.strip()
    
    # အဆင့် (ဃ) - အချက်အလက် အားလုံး သန့်စင်ပြီးမှ ထပ်နေသော Data များကို ဖယ်ရှားခြင်း
    df = df.drop_duplicates(subset=['Book Name', 'Price'])
    
    print("\n--- အလွန်သပ်ရပ်သွားသော ပုံစံ (After Pro Cleaning) ---")
    print(df.reset_index(drop=True))
    
    # Excel သို့ သိမ်းဆည်းခြင်း
    output_filename = 'cleaned_books_output.xlsx'
    df.to_excel(output_filename, index=False)
    print(f"\n[အောင်မြင်မှု] သန့်စင်ပြီးသား ဒေတာများကို '{output_filename}' သို့ အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")

if __name__ == "__main__":
    clean_scraped_data_pro()