import secrets
import json
import os
from datetime import datetime

class APIKeyManager:
    def __init__(self, storage_path="prob/config/api_keys.json"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump({}, f)

    def generate_key(self, label):
        key = f"prob_{secrets.token_hex(24)}"
        with open(self.storage_path, "r") as f:
            keys = json.load(f)

        keys[key] = {
            "label": label,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }

        with open(self.storage_path, "w") as f:
            json.dump(keys, f, indent=2)
        return key

    def validate_key(self, key):
        if not key:
            return False
        with open(self.storage_path, "r") as f:
            keys = json.load(f)
        return key in keys and keys[key]["status"] == "active"

    def list_keys(self):
        with open(self.storage_path, "r") as f:
            return json.load(f)

    def revoke_key(self, key):
        with open(self.storage_path, "r") as f:
            keys = json.load(f)
        if key in keys:
            keys[key]["status"] = "revoked"
            with open(self.storage_path, "w") as f:
                json.dump(keys, f, indent=2)
            return True
        return False
