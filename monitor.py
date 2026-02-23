import requests
import sys

# Configuration
# "check" is text that MUST be on the page. 
# Using broader terms to ensure we catch the page content accurately.
HEALTH_MATRIX = [
    {"name": "New Web (Drive)", "url": "https://drive.tempcover.com/", "check": "Tempcover"},
    {"name": "Legacy Web (Motor)", "url": "https://motor.tempcover.com/", "check": "Tempcover"},
]

def monitor():
    failures = []
    
    # Convincing headers to bypass 403 Forbidden (Bot Protection)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    for page in HEALTH_MATRIX:
        print(f"Checking {page['name']}...")
        try:
            # Added a timeout and explicit headers
            r = requests.get(page["url"], timeout=30, headers=headers)
            
            # If we get a 403, it means we are still being blocked
            if r.status_code == 403:
                failures.append(f"🛡️ {page['name']}: Blocked by Firewall (403 Forbidden).")
                continue
                
            r.raise_for_status()
            
            if page["check"] not in r.text:
                failures.append(f"❌ {page['name']}: Content '{page['check']}' missing on page.")
        except Exception as e:
            failures.append(f"🔥 {page['name']}: Request failed! Error: {e}")

    if failures:
        print("\n".join(failures))
        # This exit code triggers the GitHub Action failure notification
        sys.exit(1)
    else:
        print("✅ All pages healthy!")

if __name__ == "__main__":
    monitor()
