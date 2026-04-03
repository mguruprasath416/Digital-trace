# utils/validator.py
import re

def validate_username(username: str) -> bool:
    """Allow only safe alphanumeric usernames."""
    return bool(re.match(r'^[a-zA-Z0-9_.\-]{1,50}$', username))

def validate_email(email: str) -> bool:
    return bool(re.match(r'^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$', email, re.IGNORECASE))

def validate_domain(domain: str) -> bool:
    return bool(re.match(r'^(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}$', domain))

def validate_ip(ip: str) -> bool:
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    return all(p.isdigit() and 0 <= int(p) <= 255 for p in parts)

def sanitize_input(text: str) -> str:
    """Strip dangerous characters."""
    return re.sub(r'[^\w\s@.\-_]', '', text).strip()
