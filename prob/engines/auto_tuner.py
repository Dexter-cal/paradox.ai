import json
import os
from prob.brain.core import ProbBrain

class AutoTuner:
    def __init__(self, brain: ProbBrain):
        self.brain = brain
        self.stats_path = "prob/memory/performance_stats.json"
        self._ensure_stats()

    def _ensure_stats(self):
        if not os.path.exists(self.stats_path):
            with open(self.stats_path, "w") as f:
                json.dump({"prompts": [], "success_rate": 1.0}, f)

    def log_interaction(self, prompt, response, user_feedback=None):
        """Logs interaction to analyze success."""
        with open(self.stats_path, "r") as f:
            data = json.load(f)

        # Self-critique the response if no feedback
        if user_feedback is None:
            critique = self.brain.reason(f"Analyze your own response for clarity and accuracy (0-10):\nPrompt: {prompt}\nResponse: {response}\nScore:")
            try:
                score = int(critique.strip()[:1]) / 10.0
            except:
                score = 0.8
        else:
            score = 1.0 if user_feedback == "positive" else 0.2

        data["prompts"].append({"p": prompt, "s": score})
        # Keep last 100
        data["prompts"] = data["prompts"][-100:]
        data["success_rate"] = sum(x["s"] for x in data["prompts"]) / len(data["prompts"])

        with open(self.stats_path, "w") as f:
            json.dump(data, f)

    def optimize_system_instruction(self, current_instruction):
        """AI-driven self-optimization of its own instructions."""
        with open(self.stats_path, "r") as f:
            data = json.load(f)

        failures = [x["p"] for x in data["prompts"] if x["s"] < 0.5]
        if not failures:
            return current_instruction

        prompt = f"""Current System Instruction: {current_instruction}
Recent failures or low-quality responses occurred for these queries: {failures[:5]}

Task: Rewrite the System Instruction to be more robust, accurate, and helpful based on these failures.
Output ONLY the new instruction."""

        return self.brain.reason(prompt)
