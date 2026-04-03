# core/username_checker.py
"""
Username Checker — checks if a username exists on public platforms
by making HTTP requests to public profile URLs.
No scraping of private/login-walled content.
"""
import json
import requests
from utils.logger import get_logger
from utils.rate_limiter import polite_delay
from utils.validator import validate_username
from config.settings import REQUEST_TIMEOUT

logger = get_logger("username_checker")

def load_platforms() -> list:
    with open("config/platforms.json") as f:
        return json.load(f)["platforms"]

def check_username(username: str) -> list:
    """
    Check a username across all configured platforms.
    Returns a list of dicts with platform, url, and status.
    """
    if not validate_username(username):
        logger.error(f"Invalid username format: {username}")
        return []

    platforms = load_platforms()
    results = []
    headers = {"User-Agent": "DigitalTrace-OSINT-Research/1.0 (educational)"}

    logger.info(f"Checking username: {username} across {len(platforms)} platforms...")

    for platform in platforms:
        url = platform["url"].format(username)
        try:
            resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            found = resp.status_code == 200
            status = "FOUND" if found else f"NOT FOUND ({resp.status_code})"
            logger.info(f"  [{platform['name']:15}] {status}")
            results.append({
                "platform": platform["name"],
                "url": url,
                "status_code": resp.status_code,
                "found": found
            })
        except requests.exceptions.Timeout:
            logger.warning(f"  [{platform['name']:15}] TIMEOUT")
            results.append({"platform": platform["name"], "url": url, "status_code": None, "found": False, "error": "timeout"})
        except requests.exceptions.RequestException as e:
            logger.warning(f"  [{platform['name']:15}] ERROR: {e}")
            results.append({"platform": platform["name"], "url": url, "status_code": None, "found": False, "error": str(e)})

        polite_delay()

    found_count = sum(1 for r in results if r["found"])
    logger.info(f"Done. Found on {found_count}/{len(platforms)} platforms.")
    return results
