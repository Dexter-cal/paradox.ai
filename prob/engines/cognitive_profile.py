import json
import os
from prob.brain.core import ProbBrain

class CognitiveProfile:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory
        self.profile_path = "prob/memory/cognitive_profile.json"
        self._load()

    def _load(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r") as f:
                self.profile = json.load(f)
        else:
            self.profile = {
                "research_style": "Scientific/Technical",
                "risk_tolerance": 0.5,
                "curiosity_focus": ["Quantum Computing", "Deep Biology"],
                "interaction_count": 0
            }
            self._save()

    def _save(self):
        with open(self.profile_path, "w") as f:
            json.dump(self.profile, f, indent=2)

    def analyze_interaction(self, query, result):
        """Learns from user interaction to update focus."""
        self.profile["interaction_count"] += 1
        prompt = f"""Interaction:
User: {query}
AI: {result[:200]}...

Task: Update the AI's Cognitive Profile. What is the user's primary interest and preferred style?
Output JSON: {{"style": "...", "focus_addition": "..."}}"""

        analysis = self.brain.reason(prompt)
        try:
            if "{" in analysis:
                data = json.loads(analysis[analysis.find("{"):analysis.rfind("}")+1])
                self.profile["research_style"] = data.get("style", self.profile["research_style"])
                if data.get("focus_addition") not in self.profile["curiosity_focus"]:
                    self.profile["curiosity_focus"].append(data.get("focus_addition"))
                self._save()
        except:
            pass

    def get_contextual_prompt(self, base_prompt):
        return f"System Context (Research Style: {self.profile['research_style']}, Focus: {self.profile['curiosity_focus']})\n\n{base_prompt}"
