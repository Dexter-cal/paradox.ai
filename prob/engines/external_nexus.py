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
                "gemini": {"key": "", "enabled": False, "url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"},
                "openai": {"key": "", "enabled": False, "url": "https://api.openai.com/v1/chat/completions"},
                "anthropic": {"key": "", "enabled": False, "url": "https://api.anthropic.com/v1/messages"},
                "mistral": {"key": "", "enabled": False, "url": "https://api.mistral.ai/v1/chat/completions"},
                "groq": {"key": "", "enabled": False, "url": "https://api.groq.com/openai/v1/chat/completions"}
            }
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            self._save_config()

    def _save_config(self):
        with open(self.config_path, "w") as f:
            json.dump(self.services, f, indent=2)

    def update_key(self, service, key):
        if service in self.services:
            self.services[service]["key"] = key
            self.services[service]["enabled"] = True if key else False
            self._save_config()
            return True
        return False

    def query_external(self, service, prompt):
        if service not in self.services or not self.services[service]["enabled"]:
            return f"Service {service} is disabled or key is missing."

        key = self.services[service]["key"]
        url = self.services[service]["url"]

        try:
            if service == "gemini":
                res = requests.post(f"{url}?key={key}", json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
                return res.json()['candidates'][0]['content']['parts'][0]['text']

            elif service in ["openai", "groq", "mistral"]:
                headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
                model = "gpt-3.5-turbo" if service == "openai" else ("mixtral-8x7b-32768" if service == "groq" else "mistral-tiny")
                payload = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }
                res = requests.post(url, headers=headers, json=payload, timeout=15)
                return res.json()['choices'][0]['message']['content']

            elif service == "anthropic":
                headers = {"x-api-key": key, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}
                payload = {
                    "model": "claude-3-haiku-20240307",
                    "max_tokens": 1024,
                    "messages": [{"role": "user", "content": prompt}]
                }
                res = requests.post(url, headers=headers, json=payload, timeout=15)
                return res.json()['content'][0]['text']

        except Exception as e:
            return f"Nexus Error ({service}): {str(e)}"

        return "Service architecture not yet implemented."
