import asyncio
from playwright.async_api import async_playwright

async def main():
    print("=== Playwright Native Stealth Bypass Test ===")
    
    async with async_playwright() as p:
        # Chromium Browser ကို launch လုပ်ခြင်း
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ]
        )
        
        # Real Browser Fingerprint အသွင်ဖန်တီးခြင်း
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720},
            locale="en-US"
        )
        
        page = await context.new_page()
        
        # navigator.webdriver = true ဖြစ်နေတာကို ဖျောက်ဖျက်ပေးခြင်း
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        url = "https://bot.sannysoft.com/"
        print(f"[+] Navigating to: {url}")
        
        try:
            # wait_until="domcontentloaded" ထည့်ထားသဖြင့် ဝဘ်ဆိုက်အပြည့်အဝ မတက်သေးသော်လည်း တန်းဝင်ပါမည်
            # timeout=60000 (စက္ကန့် ၆၀ ထိ တိုးပေးထားပါသည်)
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.wait_for_timeout(5000)
            
            title = await page.title()
            print(f"[✓] Successfully Loaded Page Title: {title}")
            
            await page.screenshot(path="stealth_test_result.png")
            print("[✓] Screenshot ကို stealth_test_result.png အမည်ဖြင့် သိမ်းဆည်းလိုက်ပါပြီ!")
            
        except Exception as e:
            print(f"[!] Error ပေါ်ပေါက်ခဲ့ပါသည်: {e}")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(main())