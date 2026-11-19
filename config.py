

import os

SSH_KEY_PATH = os.path.expanduser("~/.ssh/audit_framework_key")

VMS = {
    "compliant": {
        "ip": "192.168.1.76",
        "username": "buntu",
        "key_path": SSH_KEY_PATH,
    },
    "misconfigured": {
        "ip": "192.168.1.75",
        "username": "erver",
        "key_path": SSH_KEY_PATH,
    },
}