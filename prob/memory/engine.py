import json
import os
from datetime import datetime

class MemoryEngine:
    def __init__(self, storage_path="prob/memory/data"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        self.notebook_path = os.path.join(self.storage_path, "notebook.json")
        self.failures_path = os.path.join(self.storage_path, "failures.json")
        self.discoveries_path = os.path.join(self.storage_path, "discoveries.json")

        self._initialize_files()

    def _initialize_files(self):
        for path in [self.notebook_path, self.failures_path, self.discoveries_path]:
            if not os.path.exists(path):
                with open(path, "w") as f:
                    json.dump([], f)

    def log_action(self, action, details, project="default"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "project": project,
            "action": action,
            "details": details
        }
        self._append_to_json(self.notebook_path, entry)

    def log_failure(self, task, reason, context, project="default"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "project": project,
            "task": task,
            "reason": reason,
            "context": context
        }
        self._append_to_json(self.failures_path, entry)

    def log_discovery(self, discovery, evidence, project="default"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "project": project,
            "discovery": discovery,
            "evidence": evidence
        }
        self._append_to_json(self.discoveries_path, entry)

    def _append_to_json(self, path, entry):
        with open(path, "r") as f:
            data = json.load(f)
        data.append(entry)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def get_all_notes(self):
        with open(self.notebook_path, "r") as f:
            return json.load(f)

    def get_recent_failures(self, limit=5):
        with open(self.failures_path, "r") as f:
            data = json.load(f)
        return data[-limit:]
