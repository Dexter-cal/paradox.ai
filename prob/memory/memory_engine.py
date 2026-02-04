import json
import os
import secrets
from datetime import datetime

class MemoryEngine:
    def __init__(self, storage_path="prob/memory/data"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, exist_ok=True)

        self.notebook_path = os.path.join(self.storage_path, "notebook.json")
        self.failures_path = os.path.join(self.storage_path, "failures.json")
        self.discoveries_path = os.path.join(self.storage_path, "discoveries.json")
        self.vault_path = "prob/memory/vault/sensitive_findings.json"
        self.graph_path = "prob/memory/knowledge_graph/graph.json"

        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.graph_path), exist_ok=True)

        self._initialize_files()

    def _initialize_files(self):
        for path in [self.notebook_path, self.failures_path, self.discoveries_path, self.vault_path]:
            if not os.path.exists(path):
                with open(path, "w") as f:
                    json.dump([], f)
        if not os.path.exists(self.graph_path):
            with open(self.graph_path, "w") as f:
                json.dump({"nodes": [], "links": []}, f)

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

    def store_discovery(self, query, result, sensitive=False):
        entry = {
            "id": secrets.token_hex(4),
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "result": result,
            "sensitive": sensitive
        }
        path = self.vault_path if sensitive else self.discoveries_path
        self._append_to_json(path, entry)

    def _append_to_json(self, path, entry):
        with open(path, "r") as f:
            data = json.load(f)
        data.append(entry)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def get_all_notes(self):
        with open(self.notebook_path, "r") as f:
            return json.load(f)

    def get_discoveries(self):
        with open(self.discoveries_path, "r") as f:
            return json.load(f)

    def get_pending_reviews(self):
        with open(self.vault_path, "r") as f:
            return json.load(f)

    def approve_discovery(self, entry_id):
        with open(self.vault_path, "r") as f:
            vault = json.load(f)

        entry = next((e for e in vault if e["id"] == entry_id), None)
        if entry:
            entry["sensitive"] = False
            self._append_to_json(self.discoveries_path, entry)
            vault = [e for e in vault if e["id"] != entry_id]
            with open(self.vault_path, "w") as f:
                json.dump(vault, f, indent=2)

    def get_knowledge_graph(self):
        with open(self.graph_path, "r") as f:
            return json.load(f)

    def update_graph(self, nodes, links):
        with open(self.graph_path, "w") as f:
            json.dump({"nodes": nodes, "links": links}, f, indent=2)
