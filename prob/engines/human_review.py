import os
import json
from datetime import datetime

class HumanReviewEngine:
    def __init__(self, storage_path="prob/memory/vault"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        self.vault_path = os.path.join(self.storage_path, "sensitive_findings.json")
        if not os.path.exists(self.vault_path):
            with open(self.vault_path, "w") as f:
                json.dump([], f)

    def flag_for_review(self, reasoning, result, flags):
        entry = {
            "id": datetime.now().strftime('%Y%m%d%H%M%S'),
            "timestamp": datetime.now().isoformat(),
            "reasoning": reasoning,
            "result": result,
            "flags": flags,
            "status": "pending"
        }
        with open(self.vault_path, "r") as f:
            data = json.load(f)
        data.append(entry)
        with open(self.vault_path, "w") as f:
            json.dump(data, f, indent=2)
        return entry["id"]

    def get_pending(self):
        with open(self.vault_path, "r") as f:
            data = json.load(f)
        return [e for e in data if e["status"] == "pending"]

    def approve(self, entry_id):
        with open(self.vault_path, "r") as f:
            data = json.load(f)
        for e in data:
            if e["id"] == entry_id:
                e["status"] = "approved"
                break
        with open(self.vault_path, "w") as f:
            json.dump(data, f, indent=2)
