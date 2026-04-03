# modules/whois_lookup.py
"""
WHOIS Lookup — queries public domain registration records.
Uses python-whois library; no API key required.
"""
from utils.logger import get_logger
from utils.validator import validate_domain

logger = get_logger("whois_lookup")

def whois_lookup(domain: str) -> dict:
    if not validate_domain(domain):
        return {"error": f"Invalid domain format: {domain}"}
    try:
        import whois
        logger.info(f"Running WHOIS on: {domain}")
        w = whois.whois(domain)
        return {
            "domain":       domain,
            "registrar":    w.registrar,
            "created":      str(w.creation_date),
            "expires":      str(w.expiration_date),
            "updated":      str(w.updated_date),
            "name_servers": w.name_servers,
            "status":       w.status,
            "emails":       w.emails,
            "org":          w.org,
            "country":      w.country,
        }
    except ImportError:
        return {"error": "python-whois not installed. Run: pip install python-whois"}
    except Exception as e:
        return {"error": str(e)}
