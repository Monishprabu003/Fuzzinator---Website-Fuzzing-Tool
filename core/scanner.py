import os
import json
import time
from datetime import datetime

from core.payloads import (
    SQLI_PAYLOADS,
    XSS_PAYLOADS,
    LFI_PAYLOADS,
    RFI_PAYLOADS,
    CMDI_PAYLOADS,
    HEADER_PAYLOADS,
    NOISE_PAYLOADS,
    COMMON_PAYLOADS
)
from core.utils import is_valid_url, safe_request_get

# ----------------------------------------
# Path Setup
# ----------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANS_DIR = os.path.join(BASE_DIR, "scans")
RAW_LOGS = os.path.join(SCANS_DIR, "raw_logs")
HISTORY_FILE = os.path.join(SCANS_DIR, "history.json")

# Ensure folders exist
os.makedirs(RAW_LOGS, exist_ok=True)

# Ensure history file exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f, indent=2)


# ----------------------------------------
# Helper: Append to history.json
# ----------------------------------------
def _append_history(record: dict):
    with open(HISTORY_FILE, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.insert(0, record)  # newest first
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()


# ----------------------------------------
# Helper: Write raw log file
# ----------------------------------------
def _write_raw_log(job_id: str, url: str, logs: list):
    path = os.path.join(RAW_LOGS, f"scan_{job_id}.txt")
    with open(path, "w", encoding="utf-8") as f:
        text = json.dumps({"job_id": job_id, "url": url, "logs": logs}, indent=2)
        f.write(text)
    return path


# ----------------------------------------
# Main Fuzzing Engine
# ----------------------------------------
def start_fuzz_scan(job_id: str, target_url: str, mode: str = "Basic Scan"):
    """
    The WebFuzz scanning engine

    Workflow:
    1. Validate URL
    2. Select payload set based on scan mode
    3. Inject payloads via GET query param (?test=payload)
    4. Basic vulnerability signature detection
    5. Save logs + history record
    """

    print(f"\n[{job_id}] Starting scan → {target_url} (mode={mode})")

    started_at = datetime.utcnow().isoformat() + "Z"

    # URL validation
    if not is_valid_url(target_url):
        error_record = {
            "job_id": job_id,
            "url": target_url,
            "mode": mode,
            "status": "failed",
            "reason": "Invalid URL",
            "vulns_found": 0,
            "started_at": started_at,
            "finished_at": datetime.utcnow().isoformat() + "Z",
        }
        _append_history(error_record)
        return

    # Choose payload set
    if mode == "Basic Scan":
        payload_list = COMMON_PAYLOADS
    elif mode == "SQL Injection":
        payload_list = SQLI_PAYLOADS
    elif mode == "XSS":
        payload_list = XSS_PAYLOADS
    elif mode == "Header Fuzzing":
        payload_list = HEADER_PAYLOADS
    elif mode == "Deep Scan":
        payload_list = COMMON_PAYLOADS + XSS_PAYLOADS + SQLI_PAYLOADS + LFI_PAYLOADS + CMDI_PAYLOADS
    else:
        payload_list = COMMON_PAYLOADS

    logs = []
    vulns = []

    # ----------------------------------------
    # Payload Injection Loop
    # ----------------------------------------
    for payload in payload_list:
        test_url = f"{target_url.rstrip('/')}/?test={payload}"

        status_code, response_snippet = safe_request_get(test_url)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "payload": payload,
            "test_url": test_url,
            "status_code": status_code,
            "response_snippet": response_snippet[:500] if response_snippet else None,
        }

        logs.append(log_entry)

        # Very basic detection (you will improve this later)
        if response_snippet and payload in response_snippet:
            vulns.append({
                "payload": payload,
                "type": "reflected",
                "test_url": test_url
            })

        time.sleep(0.1)  # prevent hitting target too fast

    # ----------------------------------------
    # Save Raw Logs
    # ----------------------------------------
    raw_log_path = _write_raw_log(job_id, target_url, logs)

    finished_at = datetime.utcnow().isoformat() + "Z"

    # ----------------------------------------
    # Build Scan Record (History)
    # ----------------------------------------
    scan_record = {
        "job_id": job_id,
        "url": target_url,
        "mode": mode,
        "status": "vulnerable" if len(vulns) > 0 else "finished",
        "vulns_found": len(vulns),
        "started_at": started_at,
        "finished_at": finished_at,
        "raw_log": raw_log_path.replace(BASE_DIR + "/", ""),
        "vulnerabilities": vulns,
    }

    _append_history(scan_record)

    print(f"[{job_id}] Scan complete | Vulns found: {len(vulns)}")


# ----------------------------------------
# Fetch Scan Status (Used by frontend polling)
# ----------------------------------------
def get_scan_status(job_id: str):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return None

    for entry in data:
        if entry["job_id"] == job_id:
            return entry

    return None


# ----------------------------------------
# Get Recent Scans (For Scan History Page)
# ----------------------------------------
def get_recent_scans(limit: int = 20):
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            all_scans = json.load(f)
    except:
        return []
    return all_scans[:limit]
