from prob.brain.core import ProbBrain

class FutureHistorian:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def generate_future_history(self, discovery):
        prompt = f"""Discovery: {discovery}

Task: Write a 'Future History' narrative spanning 50 years after this discovery.
Include:
- Year 1: Initial skepticism and early adoption.
- Year 10: First major societal shift.
- Year 25: The 'Crisis of Maturity' (unintended consequences).
- Year 50: Integration into the human baseline.

FUTURE HISTORY:"""
        return self.brain.reason(prompt)
