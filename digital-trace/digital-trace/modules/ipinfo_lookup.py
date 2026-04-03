# modules/ipinfo_lookup.py
"""
IP Info Lookup — gets geolocation and ASN info for an IP address.
Free tier: 50,000 requests/month. No key required for basic use.
Get a free token at: https://ipinfo.io/signup
"""
import requests
from utils.logger import get_logger
from utils.validator import validate_ip
from config.settings import IPINFO_TOKEN, REQUEST_TIMEOUT

logger = get_logger("ipinfo_lookup")

def ip_lookup(ip: str) -> dict:
    if not validate_ip(ip):
        return {"error": f"Invalid IP address: {ip}"}

    logger.info(f"Looking up IP: {ip}")
    try:
        token_param = f"?token={IPINFO_TOKEN}" if IPINFO_TOKEN != "YOUR_IPINFO_TOKEN" else ""
        url = f"https://ipinfo.io/{ip}/json{token_param}"
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "ip":       data.get("ip"),
                "hostname": data.get("hostname"),
                "city":     data.get("city"),
                "region":   data.get("region"),
                "country":  data.get("country"),
                "org":      data.get("org"),
                "timezone": data.get("timezone"),
                "loc":      data.get("loc"),
            }
        return {"error": f"API returned {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}
