# config/settings.py
import os

# --- Optional API Keys ---
HIBP_API_KEY   = os.environ.get("HIBP_API_KEY", "YOUR_HIBP_API_KEY")
IPINFO_TOKEN   = os.environ.get("IPINFO_TOKEN", "YOUR_IPINFO_TOKEN")
SHODAN_API_KEY = os.environ.get("SHODAN_API_KEY", "YOUR_SHODAN_API_KEY")

# --- Request Settings ---
REQUEST_TIMEOUT  = 8
RATE_LIMIT_DELAY = 1.5
MAX_RETRIES      = 2

# --- Report Settings ---
REPORT_OUTPUT_DIR = "reports/output"
REPORT_FORMAT     = "html"

# --- Flask Dashboard ---
FLASK_HOST  = os.environ.get("FLASK_HOST", "127.0.0.1")
FLASK_PORT  = int(os.environ.get("PORT", 5000))
FLASK_DEBUG = False

# --- Dashboard Login ---
DASHBOARD_USERNAME = os.environ.get("DASHBOARD_USERNAME", "admin")
DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "admin")
