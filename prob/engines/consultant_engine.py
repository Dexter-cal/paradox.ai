import json
import os
import requests
from typing import List, Dict

class ConsultantEngine:
    def __init__(self, db_path="prob/memory/consultants.json"):
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump([], f)

    def add_consultant(self, name: str, c_type: str, url: str, key: str):
        with open(self.db_path, "r") as f:
            data = json.load(f)
        data.append({"name": name, "type": c_type, "url": url, "key": key})
        with open(self.db_path, "w") as f:
            json.dump(data, f)

    def get_consultants(self) -> List[Dict]:
        with open(self.db_path, "r") as f:
            return json.load(f)

    def query(self, consultant_name: str, prompt: str):
        consultants = self.get_consultants()
        target = next((c for c in consultants if c["name"] == consultant_name), None)
        if not target:
            return "Consultant not found."

        if target["type"] == "openai-compatible":
            try:
                headers = {"Authorization": f"Bearer {target['key']}", "Content-Type": "application/json"}
                payload = {
                    "model": "gpt-3.5-turbo", # Default fallback
                    "messages": [{"role": "user", "content": prompt}]
                }
                response = requests.post(target["url"], headers=headers, json=payload, timeout=10)
                return response.json()["choices"][0]["message"]["content"]
            except Exception as e:
                return f"Bridge failure: {str(e)}"
        return "Unsupported bridge type."
