"""
app.py

Module 7: Dashboard, now extended with:
  - Server management (add / delete servers via the UI, no code edits)
  - Audit history (list past runs per server)
  - Run Audit button (triggers run_audit.py's logic from the browser)

Usage (from project root, venv active):
    python app.py
Then open http://127.0.0.1:5000 in a browser.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "audit_engine"))

from flask import Flask, render_template, request, redirect, url_for

from storage import load_latest_run_per_server, load_all_runs
from server_store import load_servers, add_server, delete_server, seed_from_config_if_empty
from compliance_engine import run_compliance_check
from risk_engine import score_results
from report_engine import generate_report
from storage import save_run

app = Flask(__name__)

# One-time: if servers.json is empty, pull in whatever was in config.py
seed_from_config_if_empty()


@app.route("/")
def index():
    latest_runs = load_latest_run_per_server()
    servers = load_servers()
    return render_template("index.html", runs=latest_runs, servers=servers)


@app.route("/report/<server_label>")
def report(server_label):
    latest_runs = load_latest_run_per_server()
    run = latest_runs.get(server_label)
    if run is None:
        return f"No audit run found for '{server_label}'. Run an audit first.", 404
    return render_template("report.html", run=run)


@app.route("/report/<server_label>/<rule_id>")
def finding_detail(server_label, rule_id):
    latest_runs = load_latest_run_per_server()
    run = latest_runs.get(server_label)
    if run is None:
        return f"No audit run found for '{server_label}'.", 404

    finding = next((r for r in run["results"] if r["rule_id"] == rule_id), None)
    if finding is None:
        return f"No finding '{rule_id}' found for '{server_label}'.", 404

    return render_template("finding_detail.html", run=run, finding=finding)


@app.route("/history/<server_label>")
def history(server_label):
    all_runs = load_all_runs()
    server_runs = [r for r in all_runs if r["server_label"] == server_label]
    server_runs.sort(key=lambda r: r["filename"], reverse=True)  # most recent first
    return render_template("history.html", server_label=server_label, runs=server_runs)


@app.route("/servers")
def servers_page():
    servers = load_servers()
    return render_template("servers.html", servers=servers)


@app.route("/servers/add", methods=["POST"])
def servers_add():
    label = request.form["label"].strip()
    ip = request.form["ip"].strip()
    username = request.form["username"].strip()
    key_path = request.form["key_path"].strip()
    add_server(label, ip, username, key_path)
    return redirect(url_for("servers_page"))


@app.route("/servers/delete/<label>", methods=["POST"])
def servers_delete(label):
    delete_server(label)
    return redirect(url_for("servers_page"))


@app.route("/run_audit/<server_label>", methods=["POST"])
def run_audit_single(server_label):
    """Runs the full pipeline for ONE server, triggered from the browser."""
    servers = load_servers()
    vm = servers.get(server_label)
    if vm is None:
        return f"No server '{server_label}' found.", 404

    try:
        results = run_compliance_check(vm["ip"], vm["username"], vm["key_path"])
    except Exception as e:
        return f"Audit failed for '{server_label}': {e}", 500

    summary = score_results(results)
    save_run(server_label, results, summary)

    os.makedirs("reports", exist_ok=True)
    generate_report(results, summary, output_path=os.path.join("reports", f"{server_label}_audit_report.pdf"))

    return redirect(url_for("report", server_label=server_label))

@app.route("/benchmark")
def benchmark_page():
    import json
    with open(os.path.join("rules", "knowledge_base.json")) as f:
        kb = json.load(f)
    return render_template("benchmark.html", source=kb["source"], rules=kb["rules"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
