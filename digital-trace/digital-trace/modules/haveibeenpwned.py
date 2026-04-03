# modules/haveibeenpwned.py
"""
HaveIBeenPwned — checks if an email appears in known public data breaches.
Requires a HIBP API key (~$3.50/month or free for personal use).
API docs: https://haveibeenpwned.com/API/v3
"""
import requests
from utils.logger import get_logger
from utils.validator import validate_email
from config.settings import HIBP_API_KEY, REQUEST_TIMEOUT

logger = get_logger("hibp")

def check_email_breach(email: str) -> dict:
    if not validate_email(email):
        return {"error": f"Invalid email format: {email}"}

    if HIBP_API_KEY == "YOUR_HIBP_API_KEY":
        return {"error": "HIBP API key not configured. Add it to config/settings.py"}

    logger.info(f"Checking breach exposure for: {email}")
    headers = {
        "hibp-api-key": HIBP_API_KEY,
        "user-agent":   "DigitalTrace-OSINT/1.0"
    }
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    try:
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            breaches = resp.json()
            return {
                "email":         email,
                "breached":      True,
                "breach_count":  len(breaches),
                "breaches":      [
                    {
                        "name":        b.get("Name"),
                        "domain":      b.get("Domain"),
                        "breach_date": b.get("BreachDate"),
                        "data_types":  b.get("DataClasses", []),
                    }
                    for b in breaches
                ]
            }
        elif resp.status_code == 404:
            return {"email": email, "breached": False, "breach_count": 0, "breaches": []}
        elif resp.status_code == 401:
            return {"error": "Invalid HIBP API key."}
        else:
            return {"error": f"HIBP API returned {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}
