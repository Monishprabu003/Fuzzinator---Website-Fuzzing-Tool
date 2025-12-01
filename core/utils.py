"""
Utility helpers for WebFuzz

Contains:
- URL validation
- Safe HTTP request wrappers
- Sanitizing responses
- Header builders
"""

import re
import requests
from urllib.parse import urlparse


# ------------------------------------------------
# URL VALIDATION
# ------------------------------------------------
def is_valid_url(url: str) -> bool:
    """
    Basic URL validator ensuring:
    - Begins with http/https
    - Has a valid domain or IP
    """
    if not url:
        return False

    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


# ------------------------------------------------
# SAFE REQUEST HANDLING
# ------------------------------------------------
def safe_request_get(url: str, timeout: int = 8, headers: dict = None):
    """
    A safe GET request wrapper.
    
    Returns:
        (status_code, response_snippet)
    """

    try:
        r = requests.get(url, timeout=timeout, headers=headers or {}, verify=False)
        snippet = sanitize_response(r.text)
        return r.status_code, snippet

    except requests.exceptions.Timeout:
        return None, "Timeout Error"
    except requests.exceptions.ConnectionError:
        return None, "Connection Error"
    except requests.exceptions.RequestException as e:
        return None, str(e)


def safe_request_post(url: str, data=None, timeout: int = 8, headers: dict = None):
    """
    POST wrapper for future fuzzing modes
    """
    try:
        r = requests.post(url, data=data, timeout=timeout, headers=headers or {}, verify=False)
        snippet = sanitize_response(r.text)
        return r.status_code, snippet

    except requests.exceptions.Timeout:
        return None, "Timeout Error"
    except requests.exceptions.ConnectionError:
        return None, "Connection Error"
    except requests.exceptions.RequestException as e:
        return None, str(e)


# ------------------------------------------------
# RESPONSE CLEANING
# ------------------------------------------------
def sanitize_response(text: str, max_length: int = 1000):
    """
    Clean text before saving into logs:
    - Remove excessive whitespace
    - Prevent log bloat by trimming
    """
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    return text[:max_length]


# ------------------------------------------------
# HEADER GENERATOR
# ------------------------------------------------
def build_fuzz_headers(payload: str) -> dict:
    """
    Generates headers for header fuzzing.
    Only used when scanner selects header payload mode.
    """
    return {
        "User-Agent": f"WebFuzzScanner/{payload}",
        "X-Fuzz": payload,
        "X-Testing": "WebFuzz",
    }


# ------------------------------------------------
# GENERAL HELPERS
# ------------------------------------------------
def normalize_url(url: str) -> str:
    """
    Cleans & standardizes input URL
    """
    if not url:
        return url
    return url.strip().rstrip()
