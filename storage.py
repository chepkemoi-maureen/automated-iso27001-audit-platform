
import json
import os
from datetime import datetime

DB_DIR = "database"


def save_run(server_label, results, summary):
    os.makedirs(DB_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{server_label}_{timestamp}.json"
    path = os.path.join(DB_DIR, filename)

    with open(path, "w") as f:
        json.dump({
            "server_label": server_label,
            "results": results,
            "summary": summary,
        }, f, indent=2)

    return path


def load_all_runs():

    os.makedirs(DB_DIR, exist_ok=True)
    runs = []
    for fname in sorted(os.listdir(DB_DIR)):
        if fname.endswith(".json"):
            with open(os.path.join(DB_DIR, fname)) as f:
                data = json.load(f)
                data["filename"] = fname
                runs.append(data)
    return runs


def load_latest_run_per_server():

    runs = load_all_runs()
    latest = {}
    for run in runs:
        latest[run["server_label"]] = run  
    return latest