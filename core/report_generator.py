"""
Report generator for WebFuzz

Provides:
- Export scan history to CSV
- Export scan history to JSON
- Generate simple text-based PDF reports (lightweight)
"""

import os
import json
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCANS_DIR = os.path.join(BASE_DIR, "scans")
HISTORY_FILE = os.path.join(SCANS_DIR, "history.json")


# ------------------------------------------------
# Load History File
# ------------------------------------------------
def _load_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


# ------------------------------------------------
# Export to JSON
# ------------------------------------------------
def export_history_json(out_path=None):
    """
    Exports full scan history to JSON.
    """
    scans = _load_history()
    if not out_path:
        out_path = os.path.join(SCANS_DIR, f"WebFuzz_Report_{timestamp()}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(scans, f, indent=2)

    return out_path


# ------------------------------------------------
# Export to CSV
# ------------------------------------------------
def export_history_csv(out_path=None):
    """
    Exports scan history to CSV.
    """
    scans = _load_history()
    if not out_path:
        out_path = os.path.join(SCANS_DIR, f"WebFuzz_Report_{timestamp()}.csv")

    with open(out_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "Job ID",
            "Target URL",
            "Mode",
            "Status",
            "Vulns Found",
            "Started",
            "Finished",
        ])

        for scan in scans:
            writer.writerow([
                scan.get("job_id"),
                scan.get("url"),
                scan.get("mode"),
                scan.get("status"),
                scan.get("vulns_found"),
                scan.get("started_at"),
                scan.get("finished_at")
            ])

    return out_path


# ------------------------------------------------
# Export a Minimal PDF (Plain Text PDF)
# ------------------------------------------------
def export_scan_pdf(job_id: str, out_path=None):
    """
    Generates a lightweight text-based PDF without dependencies.
    (Formatted using raw PDF structure — safe & simple.)
    """
    scans = _load_history()
    scan = next((s for s in scans if s["job_id"] == job_id), None)

    if not scan:
        return None

    if not out_path:
        out_path = os.path.join(SCANS_DIR, f"WebFuzz_Scan_{job_id}.pdf")

    text = _build_pdf_text(scan)

    # Basic PDF structure (no external libs)
    pdf_content = f"""%PDF-1.4
1 0 obj << /Type /Catalog /Pages 2 0 R >> endobj
2 0 obj << /Type /Pages /Count 1 /Kids [3 0 R] >> endobj
3 0 obj << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
    /Contents 4 0 R /Resources << >> >> endobj
4 0 obj << /Length {len(text) + 20} >>
stream
{text}
endstream
endobj
xref
0 5
0000000000 65535 f 
0000000010 00000 n 
0000000079 00000 n 
0000000174 00000 n 
0000000371 00000 n 
trailer << /Size 5 /Root 1 0 R >>
startxref
500
%%EOF
"""

    with open(out_path, "wb") as f:
        f.write(pdf_content.encode())

    return out_path


# ------------------------------------------------
# Helper to build text for PDF
# ------------------------------------------------
def _build_pdf_text(scan: dict):
    text = f"""
WebFuzz Scan Report
-----------------------------

Job ID: {scan.get("job_id")}
Target URL: {scan.get("url")}
Scan Mode: {scan.get("mode")}
Status: {scan.get("status")}
Vulnerabilities Found: {scan.get("vulns_found")}
Started: {scan.get("started_at")}
Finished: {scan.get("finished_at")}

Vulnerabilities:
-----------------------------
"""

    vulns = scan.get("vulnerabilities", [])
    if not vulns:
        text += "No vulnerabilities detected.\n"
    else:
        for v in vulns:
            text += f"- Payload: {v['payload']}\n  URL: {v['test_url']}\n"

    text = text.replace("\n", "\r")  # PDF text formatting
    return text


# ------------------------------------------------
# Timestamp
# ------------------------------------------------
def timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
