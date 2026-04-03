# utils/rate_limiter.py
import time
from config.settings import RATE_LIMIT_DELAY

def polite_delay(custom_delay: float = None):
    """Sleep between requests to avoid hammering servers."""
    time.sleep(custom_delay if custom_delay else RATE_LIMIT_DELAY)
