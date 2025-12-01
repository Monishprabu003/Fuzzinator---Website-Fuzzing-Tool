"""
Core module for WebFuzz

This package contains:
- scanner.py          → Main fuzzing engine / scan orchestration
- payloads.py         → Payload libraries (XSS, SQLi, LFI, etc.)
- utils.py            → Utility functions (request wrappers, validators)
- report_generator.py → Export scan results into CSV/JSON/PDF formats
"""

from .scanner import start_fuzz_scan, get_scan_status, get_recent_scans
from .payloads import COMMON_PAYLOADS
from .utils import is_valid_url, safe_request_get
