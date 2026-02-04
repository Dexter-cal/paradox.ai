import secrets
import json
import os
from datetime import datetime

class APIKeyManager:
    def __init__(self, db_path="prob/memory/api_keys.json"):
        self.db_path = db_path
        self.keys = {}
        self._load()

    def _load(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                self.keys = json.load(f)
        else:
            self._save()

    def _save(self):
        with open(self.db_path, "w") as f:
            json.dump(self.keys, f)

    def generate_key(self, label: str):
        key = f"prob_{secrets.token_urlsafe(32)}"
        self.keys[key] = {
            "label": label,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        self._save()
        return key

    def validate_key(self, key: str):
        return key in self.keys and self.keys[key]["status"] == "active"

    def revoke_key(self, key: str):
        if key in self.keys:
            self.keys[key]["status"] = "revoked"
            self._save()
