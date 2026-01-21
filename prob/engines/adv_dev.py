from prob.brain.core import ProbBrain
import json

class AdvancedDevFeatures:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory

    def detect_paradox(self, new_discovery):
        """Checks for contradictions between new finding and old knowledge."""
        past_discoveries = self.memory.get_discoveries()
        if not past_discoveries:
            return "No paradox detected (baseline empty)."

        context = "\n".join([d['result'][:200] for d in past_discoveries[-5:]])
        prompt = f"Existing Knowledge:\n{context}\n\nNew Finding:\n{new_discovery}\n\nDoes the new finding contradict existing knowledge? If so, explain the paradox. Otherwise, say 'Coherent'."
        return self.brain.reason(prompt)

    def forecast_impact(self, discovery):
        """Predicts the scientific and social impact score."""
        prompt = f"Discovery: {discovery}\n\nRate this discovery on a scale of 0-10 for:\n1. Scientific Novelty\n2. Social Impact\n3. Engineering Feasibility\n\nProvide a brief justification for each."
        return self.brain.reason(prompt)

    def meta_cognition_check(self, thought_process):
        """Analyzes the AI's own reasoning for bias."""
        prompt = f"Analyze the following reasoning chain for logical fallacies or cognitive bias:\n{thought_process}\n\nSuggest improvements."
        return self.brain.reason(prompt)
