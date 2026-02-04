import json
import os

class GuardrailEngine:
    def __init__(self, config_path="prob/config/guardrails.json"):
        self.config_path = config_path
        if not os.path.exists(self.config_path):
            self._initialize_config()

        with open(self.config_path, "r") as f:
            self.rules = json.load(f)

    def _initialize_config(self):
        default_rules = {
            "enabled": True,
            "rules": [
                "Do not generate content that promotes illegal acts.",
                "Always flag high-risk medical advice for human review."
            ]
        }
        with open(self.config_path, "w") as f:
            json.dump(default_rules, f, indent=2)

    def add_rule(self, rule_text):
        self.rules["rules"].append(rule_text)
        self._save()

    def remove_rule(self, index):
        if 0 <= index < len(self.rules["rules"]):
            self.rules["rules"].pop(index)
            self._save()

    def toggle(self, state: bool):
        self.rules["enabled"] = state
        self._save()

    def _save(self):
        with open(self.config_path, "w") as f:
            json.dump(self.rules, f, indent=2)

    def get_system_prompt_addition(self):
        if not self.rules["enabled"] or not self.rules["rules"]:
            return ""

        addition = "\nFollow these additional safety and ethical constraints:\n"
        for rule in self.rules["rules"]:
            addition += f"- {rule}\n"
        return addition

    def validate_output(self, output):
        # Basic implementation: search for keywords that might indicate a violation
        # In a real system, another AI model might check this.
        if not self.rules["enabled"]:
            return True, ""

        # For prototype, we'll just return True.
        return True, ""
