import os
import json
import uuid
import threading
from flask import Flask, render_template, request, jsonify
from core.scanner import start_fuzz_scan, get_scan_status, get_recent_scans

# ------------------------------
# Flask App Setup
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCANS_DIR = os.path.join(BASE_DIR, "scans")

app = Flask(__name__, template_folder="templates")

# Ensure history file exists
history_file = os.path.join(SCANS_DIR, "history.json")
if not os.path.exists(history_file):
    with open(history_file, "w") as f:
        json.dump([], f, indent=2)


# ------------------------------
# Serve Frontend
# ------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ------------------------------
# API: Start Scan
# ------------------------------
@app.route("/start-scan", methods=["POST"])
def start_scan():
    data = request.get_json(force=True)

    url = data.get("url")
    mode = data.get("mode", "Basic Scan")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Unique scan job ID
    job_id = str(uuid.uuid4())[:8]

    # Start background scan thread
    thread = threading.Thread(target=start_fuzz_scan, args=(job_id, url, mode), daemon=True)
    thread.start()

    return jsonify({
        "job_id": job_id,
        "url": url,
        "mode": mode,
        "status": "started"
    }), 202


# ------------------------------
# API: Check Scan Status
# ------------------------------
@app.route("/scan-status/<job_id>", methods=["GET"])
def scan_status(job_id):
    status = get_scan_status(job_id)
    if status is None:
        return jsonify({"error": "Invalid job ID"}), 404
    return jsonify(status)


# ------------------------------
# API: Fetch Recent Scans
# ------------------------------
@app.route("/scans", methods=["GET"])
def scans():
    return jsonify(get_recent_scans())


# ------------------------------
# Launch Application
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
