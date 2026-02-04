import json
import os
import shutil
from prob.brain.core import ProbBrain

class SelfRepairEngine:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory
        self.repair_log_path = "prob/memory/repair_log.json"
        self._ensure_log()

    def _ensure_log(self):
        if not os.path.exists(self.repair_log_path):
            with open(self.repair_log_path, "w") as f:
                json.dump([], f)

    def scan_and_fix(self):
        """Analyzes failures and attempts autonomous fixes."""
        failures = self.memory.get_recent_failures(limit=10)
        if not failures:
            return "No critical system errors detected."

        repairs_attempted = []
        for f in failures:
            prompt = f"""System Error Detected:
Task: {f['task']}
Reason: {f['reason']}

As Prob AI, propose a one-line bash command or Python instruction to fix this.
Output ONLY the fix instruction, starting with 'FIX: '."""

            fix_suggestion = self.brain.reason(prompt)
            if fix_suggestion.startswith("FIX: "):
                fix = fix_suggestion.replace("FIX: ", "").strip()
                # Here we could theoretically execute it if safe, but we will log it for now
                repairs_attempted.append({"error": f['reason'], "fix": fix})
                self._log_repair(f['reason'], fix)

        return repairs_attempted

    def _log_repair(self, error, fix):
        with open(self.repair_log_path, "r") as f:
            log = json.load(f)
        log.append({"timestamp": str(os.times()), "error": error, "fix": fix})
        with open(self.repair_log_path, "w") as f:
            json.dump(log, f, indent=2)
