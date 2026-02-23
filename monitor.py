import sys
from playwright.sync_api import sync_playwright

# Configuration
HEALTH_MATRIX = [
    {"name": "New Web (Drive)", "url": "https://drive.tempcover.com/", "check": "Tempcover"},
    {"name": "Legacy Web (Motor)", "url": "https://motor.tempcover.com/", "check": "Tempcover"},
]

def monitor():
    failures = []
    
    with sync_playwright() as p:
        # Launch a real browser (Chromium)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        for page_info in HEALTH_MATRIX:
            print(f"Checking {page_info['name']} via Playwright...")
            page = context.new_page()
            try:
                # Go to the URL and wait for the page to load
                response = page.goto(page_info['url'], wait_until="networkidle", timeout=60000)
                
                if response.status == 403:
                    failures.append(f"🛡️ {page_info['name']}: Still blocked by 403 (Firewall).")
                elif page_info['check'] not in page.content():
                    failures.append(f"❌ {page_info['name']}: Content '{page_info['check']}' missing.")
                else:
                    print(f"✅ {page_info['name']} is healthy.")
                    
            except Exception as e:
                failures.append(f"🔥 {page_info['name']}: Request failed! Error: {e}")
            finally:
                page.close()
        
        browser.close()

    if failures:
        print("\n".join(failures))
        sys.exit(1)
    else:
        print("🎉 All pages healthy and accessible!")

if __name__ == "__main__":
    monitor()
