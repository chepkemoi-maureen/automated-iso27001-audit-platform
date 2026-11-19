"""
server_store.py

Replaces the hardcoded config.py VMS dict with a JSON file the user
can add/edit/delete servers in through the dashboard, instead of
editing source code. This is what makes the platform reusable by
another organization without touching Python.
"""

import json
import os

SERVERS_FILE = os.path.join("config", "servers.json")


def _ensure_file():
    os.makedirs(os.path.dirname(SERVERS_FILE), exist_ok=True)
    if not os.path.exists(SERVERS_FILE):
        with open(SERVERS_FILE, "w") as f:
            json.dump({}, f)


def load_servers():
    """Returns dict: {label: {ip, username, key_path}}"""
    _ensure_file()
    with open(SERVERS_FILE) as f:
        return json.load(f)


def save_servers(servers):
    _ensure_file()
    with open(SERVERS_FILE, "w") as f:
        json.dump(servers, f, indent=2)


def add_server(label, ip, username, key_path):
    servers = load_servers()
    servers[label] = {"ip": ip, "username": username, "key_path": key_path}
    save_servers(servers)


def delete_server(label):
    servers = load_servers()
    servers.pop(label, None)
    save_servers(servers)


def seed_from_config_if_empty():
    """One-time migration: if servers.json is empty, pull in whatever
    was hardcoded in config.py, so existing VMs aren't lost."""
    servers = load_servers()
    if servers:
        return
    try:
        from config import VMS
        save_servers(VMS)
    except ImportError:
        pass