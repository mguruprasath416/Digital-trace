# config/settings.py
# DigitalTrace Configuration
# Replace placeholder values with your actual API keys

# --- Optional API Keys (free tier available) ---
HIBP_API_KEY    = "YOUR_HIBP_API_KEY"      # https://haveibeenpwned.com/API/Key
IPINFO_TOKEN    = "YOUR_IPINFO_TOKEN"      # https://ipinfo.io/signup  (free: 50k/month)
SHODAN_API_KEY  = "YOUR_SHODAN_API_KEY"    # https://account.shodan.io (free tier)

# --- Request Settings ---
REQUEST_TIMEOUT = 8          # seconds per HTTP request
RATE_LIMIT_DELAY = 1.5       # seconds between requests (be polite)
MAX_RETRIES = 2

# --- Report Settings ---
REPORT_OUTPUT_DIR = "reports/output"
REPORT_FORMAT = "html"       # "html" or "txt"

# --- Flask Dashboard ---
FLASK_HOST = "127.0.0.1"
FLASK_PORT = 5000
FLASK_DEBUG = False
