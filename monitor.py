import sys
import os
from playwright.sync_api import sync_playwright

# FINAL VERIFIED MONITOR VERSION
HEALTH_MATRIX = [
    {"name": "Main Site (Home)", "url": "https://www.tempcover.com/", "check": "Temporary Vehicle Insurance"},
    {"name": "Invalid Reg Page", "url": "https://drive.tempcover.com/invalid-reg", "check": "To get started"},
    {"name": "Private Car Flow", "url": "https://drive.tempcover.com/privatecar", "check": "Enter your details"},
]

def monitor():
    failures = []
    
    with sync_playwright() as p:
        print("🚀 LAUNCHING BROWSER ENGINE...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        )
        
        for page_info in HEALTH_MATRIX:
            print(f"--- RUNNING CHECK: {page_info['name']} ---")
            page = context.new_page()
            try:
                # Use 'networkidle' to ensure Builder.io/Next.js content has fully loaded
                response = page.goto(page_info['url'], wait_until="networkidle", timeout=60000)
                status = response.status
                print(f"DEBUG: Status Code = {status}")
                
                if status >= 400:
                    failures.append(f"❌ {page_info['name']}: Received {status} error.")
                else:
                    # Give it a tiny bit of extra time for any late-loading JS
                    page.wait_for_timeout(2000)
                    
                    content = page.content()
                    if page_info['check'].lower() not in content.lower():
                        # If it fails, print a larger chunk of the content to see what's there
                        print(f"DEBUG: Content check failed. Full Page Snippet (first 2000 chars):\n{content[:2000]}")
                        failures.append(f"❌ {page_info['name']}: Content '{page_info['check']}' not found.")
                    else:
                        print(f"✅ {page_info['name']} is healthy.")
                    
            except Exception as e:
                failures.append(f"🔥 {page_info['name']}: Request failed! Error: {str(e)[:100]}")
            finally:
                page.close()
        
        browser.close()

    if failures:
        print("\nCRITICAL FAILURES:")
        print("\n".join(failures))
        sys.exit(1)
    else:
        print("\nSUCCESS: All systems operational.")

if __name__ == "__main__":
    monitor()
