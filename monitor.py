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
        # Use a more complete, modern user agent and headers to look like a real browser
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            viewport={'width': 1280, 'height': 720},
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'en-US,en;q=0.9',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Sec-Fetch-Dest': 'document',
            }
        )
        
        for page_info in HEALTH_MATRIX:
            print(f"--- RUNNING CHECK: {page_info['name']} ---")
            page = context.new_page()
            try:
                # Use 'commit' to return as soon as headers are received. 
                # This prevents timeouts if the page hangs on assets or JS.
                response = page.goto(page_info['url'], wait_until="commit", timeout=30000)
                status = response.status
                print(f"DEBUG: Status Code = {status}")
                
                # Check for blocking status codes immediately
                if status == 403:
                    failures.append(f"❌ {page_info['name']}: Access Denied (403). WAF/Cloudflare blocking active.")
                    continue
                elif status >= 400:
                    failures.append(f"❌ {page_info['name']}: Received {status} error.")
                    continue

                # Manually wait for the content to appear, with a safety timeout
                try:
                    # Give the page some time to render
                    page.wait_for_load_state("domcontentloaded", timeout=10000)
                    page.wait_for_timeout(2000) # Small buffer for dynamic content
                except Exception as e:
                    print(f"DEBUG: Load state timeout ignored, proceeding to content check: {str(e)[:50]}")

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
