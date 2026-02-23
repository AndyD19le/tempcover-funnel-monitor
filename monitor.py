import requests
import sys

# Configuration
# Add as many URLs as you need. "check" is text that MUST be on the page.
HEALTH_MATRIX = [
    {"name": "New Web (Drive)", "url": "https://drive.tempcover.com/", "check": "Get a Quote"},
    {"name": "Legacy Web (Motor)", "url": "https://motor.tempcover.com/", "check": "Short Term Insurance"},
]

def monitor():
    failures = []
    
    for page in HEALTH_MATRIX:
        print(f"Checking {page['name']}...")
        try:
            # Added a user-agent to avoid being blocked by simple bot protection
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            r = requests.get(page["url"], timeout=15, headers=headers)
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
