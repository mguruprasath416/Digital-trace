# core/dork_generator.py
"""
Google Dork Generator — generates search query strings for OSINT research.
This module ONLY generates text queries. It does NOT automate any searches.
Paste the output into a search engine manually.
"""
from utils.logger import get_logger

logger = get_logger("dork_generator")

DORK_TEMPLATES = {
    "exposed_files": [
        'site:{target} filetype:pdf',
        'site:{target} filetype:xls OR filetype:xlsx',
        'site:{target} filetype:doc OR filetype:docx',
        'site:{target} filetype:env OR filetype:log',
    ],
    "login_pages": [
        'site:{target} inurl:login',
        'site:{target} inurl:admin',
        'site:{target} inurl:dashboard',
    ],
    "sensitive_directories": [
        'site:{target} intitle:"index of"',
        'site:{target} inurl:/backup',
        'site:{target} inurl:/config',
    ],
    "error_messages": [
        'site:{target} "SQL syntax" OR "mysql_fetch"',
        'site:{target} "Warning: include()" OR "Fatal error"',
    ],
    "social_footprint": [
        '"{target}" site:linkedin.com',
        '"{target}" site:twitter.com OR site:x.com',
        '"{target}" site:github.com',
        '"{target}" email OR contact',
    ],
    "email_exposure": [
        '"{target}" "@gmail.com" OR "@yahoo.com"',
        'site:{target} "email" filetype:pdf',
    ]
}

def generate_dorks(target: str, categories: list = None) -> dict:
    """
    Generate Google dork queries for a given target (domain or name).
    Returns a dict of category -> list of query strings.
    """
    selected = categories if categories else list(DORK_TEMPLATES.keys())
    results = {}

    for cat in selected:
        if cat not in DORK_TEMPLATES:
            logger.warning(f"Unknown dork category: {cat}")
            continue
        results[cat] = [q.replace("{target}", target) for q in DORK_TEMPLATES[cat]]

    logger.info(f"Generated {sum(len(v) for v in results.values())} dork queries for: {target}")
    return results

def print_dorks(target: str):
    """Pretty print all dorks for a target."""
    dorks = generate_dorks(target)
    print(f"\n{'='*60}")
    print(f"  Google Dorks for: {target}")
    print(f"{'='*60}")
    for category, queries in dorks.items():
        print(f"\n[{category.upper().replace('_',' ')}]")
        for q in queries:
            print(f"  {q}")
    print(f"\n{'='*60}")
    print("  Paste these queries manually into Google/Bing/DuckDuckGo")
    print(f"{'='*60}\n")
