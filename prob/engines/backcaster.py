from prob.brain.core import ProbBrain

class BackcasterEngine:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def generate_roadmap(self, future_outcome, target_year=2040):
        prompt = f"""Target Future Outcome: {future_outcome}
Target Year: {target_year}

Task: Perform 'Backcasting' analysis. Work backwards from the success of this outcome in {target_year} to the present day.
Identify:
1. Final milestone (1 year before)
2. Mid-point breakthrough
3. Critical research required NOW (next 12 months)
4. Dependencies and risks.

ROADMAP TO {target_year}:"""
        return self.brain.reason(prompt)
