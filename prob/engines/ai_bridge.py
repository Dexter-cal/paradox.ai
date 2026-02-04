import requests
import json

class AIBridgeEngine:
    def __init__(self, config_path="prob/config/consultants.json"):
        self.config_path = config_path
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                json.dump([], f)

    def add_consultant(self, name, model_type, api_url, api_key):
        with open(self.config_path, "r") as f:
            consultants = json.load(f)

        consultants.append({
            "name": name,
            "type": model_type,
            "url": api_url,
            "key": api_key
        })

        with open(self.config_path, "w") as f:
            json.dump(consultants, f, indent=2)

    def query_consultant(self, name, prompt):
        with open(self.config_path, "r") as f:
            consultants = json.load(f)

        target = next((c for c in consultants if c["name"] == name), None)
        if not target:
            return f"Error: Consultant {name} not found."

        if target["type"] == "openai-compatible":
            try:
                headers = {"Authorization": f"Bearer {target['key']}", "Content-Type": "application/json"}
                data = {
                    "model": "gpt-4", # Or specific model
                    "messages": [{"role": "user", "content": prompt}]
                }
                res = requests.post(target["url"], headers=headers, json=data, timeout=30)
                return res.json()["choices"][0]["message"]["content"]
            except Exception as e:
                return f"Consultant error: {e}"

        return "Unsupported model type."

    def list_consultants(self):
        with open(self.config_path, "r") as f:
            return json.load(f)

import os
