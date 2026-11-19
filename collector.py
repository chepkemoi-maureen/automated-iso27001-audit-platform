

from datetime import datetime, timezone
from ssh_manager import SSHManager


def collect_evidence(ip, username, key_path, commands):
    """
    commands: list of dicts, each like:
        {"id": "LOG-01", "command": "systemctl is-active auditd"}

    Returns a list of evidence dicts — one per command — with the raw
    output, no evaluation applied.
    """
    evidence = []

    with SSHManager(ip, username, key_path) as ssh:
        for item in commands:
            output, error = ssh.run_command(item["command"])
            evidence.append({
                "id": item["id"],
                "command": item["command"],
                "output": output,
                "error": error,
                "host": ip,
                "collected_at": datetime.now(timezone.utc).isoformat(),
            })

    return evidence


if __name__ == "__main__":

    import argparse
    import json

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--key", required=True)
    args = parser.parse_args()

    sample_commands = [
        {"id": "TEST-01", "command": "systemctl is-active auditd"},
        {"id": "TEST-02", "command": "systemctl is-active ufw"},
        {"id": "TEST-03", "command": "whoami"},
    ]

    results = collect_evidence(args.ip, args.user, args.key, sample_commands)
    print(json.dumps(results, indent=2))