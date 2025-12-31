<h1 align="center">
  <br>
  🚀 WebFuzz – Web Application Fuzzing & Vulnerability Discovery Tool  
  <br>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Flask-Backend-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Fuzzing-Engine-purple?style=for-the-badge">
</p>

---

# 🌐 **Live Demo**
### 👉 **WebFuzz is LIVE here:**  
### 🔗 **https://fuzzinator-website-fuzzing-tool.onrender.com**

> ⚠️ First load may take 10–20 seconds because Render free tier sleeps when idle.

---

     WEBFUZZ – WEB APPLICATION SECURITY FUZZING TOOL

---

# 🛡️ **Overview**

**WebFuzz** is a lightweight, modular, and extensible **web fuzzing framework** built using **Python + Flask**.

It is designed to detect common web vulnerabilities such as:

- XSS  
- SQL Injection  
- LFI & RFI  
- Header-based attacks  
- Command Injection  
- And custom fuzzing payloads  

It features a **modern cyberpunk UI**, a clean backend architecture, and cloud deployment — making it perfect for:

- Cybersecurity learners  
- Pentesting students  
- Bug bounty beginners  

---

# 🚀 Features

### 🔎 Core Fuzzing Engine
- Categorized payloads (XSS, SQLi, LFI, RFI, CMDI)
- Deep Scan Mode (combined payload categories)
- Header fuzzing support  
- Safe HTTP requests with sanitization  
- Lightweight signature-based detection  
- Background-thread scanning engine  

### 🖥️ Frontend (HTML + CSS + JS)
- Cyberpunk professional dark UI  
- Sidebar navigation  
- Live scan updates  
- Dynamic statuses (High / Medium / Safe / Pending)  
- Single-page multipanel architecture  

### 📦 Backend (Flask)
- `/start-scan` → Begin fuzzing  
- `/scan-status/<job_id>` → Poll scan status  
- `/scans` → Fetch full scan history  

### 📊 Reporting
- Export in **CSV**  
- Export in **JSON**  
- Generate lightweight text-based PDFs  

### 📁 Storage
- Persistent scan history  
- Raw logs saved for each scan  

---

# 🧩 Project Structure

WebFuzz/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│ └── index.html
│
├── core/
│ ├── init.py
│ ├── scanner.py
│ ├── payloads.py
│ ├── utils.py
│ └── report_generator.py
│
└── scans/
├── history.json
└── raw_logs/

---

# ⚙️ Tech Stack

### **Backend**
- Python 3  
- Flask  
- Gunicorn  
- Requests  

### **Frontend**
- HTML5  
- CSS3  
- Vanilla JavaScript  

### **Security Concepts Used**
- Payload fuzzing  
- Parameter injection  
- Reflective vulnerability detection  
- HTTP response analysis  

---

# 📥 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Monishprabu003/Fuzzinator---Website-Fuzzing-Tool.git

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
python app.py


Visit:

http://localhost:8000

🧪 API Endpoints
▶ Start a scan
POST /start-scan
{
  "url": "https://example.com",
  "mode": "Basic Scan"
}

▶ Check scan status
GET /scan-status/<job_id>

▶ Fetch scan history
GET /scans
🧭 Roadmap
Planned Features:

Multi-threading support

WAF detection module

Plugin-based architecture

Authentication fuzzing

Browser-based XSS simulation

Docker deployment

API key authentication

⚖️ License

MIT License © 2025 Monish Prabu B

🙌 Credits

Developed by Monish Prabu B

Inspired by industry tools like XSStrike, Wfuzz, ZAP

UI designed with a cyber-dark theme aesthetic
