import os
import json
import time
import uuid
import threading
from flask import Flask, render_template, request, jsonify, send_from_directory
from core.scanner import start_fuzz_scan, get_scan_status, get_recent_scans

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCANS_DIR = os.path.join(BASE_DIR, "scans")
if not os.path.exists(SCANS_DIR):
    os.makedirs(SCANS_DIR)

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start-scan", methods=["POST"])
def start_scan():
    """
    Starts a fuzzing scan in background and returns a job id.
    Expected JSON body: { "url": "https://example.com", "mode": "Basic Scan" }
    """
    data = request.get_json(force=True)
    url = data.get("url")
    mode = data.get("mode", "Basic Scan")

    if not url:
        return jsonify({"error": "Missing url"}), 400

    job_id = str(uuid.uuid4())[:8]
    started_at = int(time.time())

    # kick off background scanning thread
    thread = threading.Thread(target=start_fuzz_scan, args=(job_id, url, mode), daemon=True)
    thread.start()

    return jsonify({"job_id": job_id, "status": "started", "started_at": started_at}), 202


@app.route("/scan-status/<job_id>", methods=["GET"])
def scan_status(job_id):
    status = get_scan_status(job_id)
    if status is None:
        return jsonify({"error": "Job not found"}), 404
    return jsonify(status)


@app.route("/scans", methods=["GET"])
def scans():
    """Return recent scan history"""
    scans = get_recent_scans()
    return jsonify(scans)


if __name__ == "__main__":
    # ensure history file exists
    history_file = os.path.join(SCANS_DIR, "history.json")
    if not os.path.exists(history_file):
        with open(history_file, "w") as f:
            json.dump([], f, indent=2)

    # run flask
    app.run(host="0.0.0.0", port=8000, debug=True)
