import pandas as pd
import matplotlib.pyplot as plt

# 1. ပေါင်းချုပ်ထားသော Data ဖိုင်ကို ပြန်လည် ဖတ်ယူခြင်း
df = pd.read_excel('combined_departments.xlsx')

# 2. ဌာနအလိုက် စုစုပေါင်း လစာကို တွက်ချက်ခြင်း
dept_salary = df.groupby('မူရင်းဌာန')['လစာ'].sum()

# 3. Chart ပုံစံ ပြင်ဆင်ရေးဆွဲခြင်း
plt.figure(figsize=(8, 5))  # Graph အရွယ်အစား (အကျယ် 8, အမြင့် 5)

# Bar Chart ဆွဲခြင်း (အရောင်ကို skyblue ဟု သတ်မှတ်ခြင်း)
bars = plt.bar(dept_salary.index, dept_salary.values, color='skyblue', edgecolor='navy')

# Chart Title နှင့် Axis Label များ ထည့်သွင်းခြင်း
plt.title('Total Salary Expense by Department', fontsize=14, fontweight='bold')
plt.xlabel('Department', fontsize=12)
plt.ylabel('Total Salary (MMK)', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)  # နောက်ခံ လိုင်းအစင်းလေးများ ထည့်ခြင်း

# 4. Graph ကို ပုံရိပ်ဖိုင် (PNG Image) အဖြစ် သိမ်းဆည်းခြင်း
chart_filename = 'department_salary_chart.png'
plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
plt.close()

print(f"အောင်မြင်စွာဖြင့် Graph ကို '{chart_filename}' အဖြစ် သိမ်းဆည်းပြီးပါပြီဗျာ!")