# 🔥 WebFuzz – Web Application Fuzzing & Vulnerability Discovery Tool

A professional, lightweight, and extensible **web fuzzing framework** built with **Python + Flask**, designed to detect common vulnerabilities such as **XSS**, **SQL Injection**, **LFI**, **Command Injection**, and more.

WebFuzz provides a **clean cyber-professional UI**, easy backend integration, and a modular architecture that makes it perfect for:

- Pentesting students  
- Bug bounty beginners  
- Security researchers  
- Interview/portfolio projects  

---

## 🚀 Features

### 🔎 Core Fuzzing Engine
- Payload-based fuzzing (XSS, SQLi, LFI, RFI, CMDI)
- Deep Scan Mode (combined payload categories)
- Header fuzzing support  
- Safe HTTP request handling  
- Lightweight signature-based detection  

### 🖥️ Frontend (HTML + CSS + JS)
- Cyberpunk + professional dark theme  
- Start scan UI  
- Live scan status updates  
- Dynamic results table  
- Pending / High / Medium / Safe indicator tags  

### 📦 Backend (Flask)
- `/start-scan` → starts fuzzing job  
- `/scan-status/<job_id>` → returns scan results  
- `/scans` → recent scan history  

### 📊 Reporting
- Export to **CSV**  
- Export to **JSON**  
- Lightweight text-based PDF generator  

### 📁 File Storage
- Raw logs saved for every scan  
- Scan history stored in `scans/history.json`

---

## 🧩 Project Structure

