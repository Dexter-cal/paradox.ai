from prob.brain.core import ProbBrain

class CritiqueConsole:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def critique(self, finding, perspective="Scientific Rigor"):
        prompt = f"""You are the Prob AI Critique Console.
Analyze the following finding from the perspective of {perspective}.
Identify:
1. Logical fallacies
2. Hidden assumptions
3. Potential risks
4. Areas of uncertainty

Finding: {finding}

CRITIQUE:"""
        return self.brain.reason(prompt)

    def debate(self, finding):
        """Simulates two internal personas debating a finding."""
        pro = self.brain.reason(f"Argue IN FAVOR of this finding: {finding}")
        con = self.brain.reason(f"Argue AGAINST this finding: {finding}")
        synthesis = self.brain.reason(f"Synthesize the following debate:\nPRO: {pro}\nCON: {con}")
        return {"pro": pro, "con": con, "synthesis": synthesis}
