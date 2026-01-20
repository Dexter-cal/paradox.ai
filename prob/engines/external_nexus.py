import json
import os
import requests
from prob.brain.core import ProbBrain

class ExternalNexus:
    def __init__(self, brain: ProbBrain):
        self.brain = brain
        self.config_path = "prob/config/nexus.json"
        self._load_config()

    def _load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                self.services = json.load(f)
        else:
            self.services = {
                "gemini": {"key": "", "enabled": False},
                "openai": {"key": "", "enabled": False},
                "anthropic": {"key": "", "enabled": False}
            }
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self.services, f)

    def query_external(self, service, prompt):
        if service not in self.services or not self.services[service]["enabled"]:
            return f"Service {service} is disabled or not configured."

        key = self.services[service]["key"]
        if service == "gemini":
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"
            try:
                res = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=10)
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                return f"Gemini Error: {e}"
        return "Unsupported service."
