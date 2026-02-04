from prob.brain.core import ProbBrain

class RedTeamAdversary:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def attack(self, finding):
        prompt = f"""You are the Prob AI Red Team Adversary.
Your sole mission is to DISPROVE the following discovery.
Finding: {finding}

Tasks:
1. Identify the 'Weakest Link' in the assumptions.
2. Propose a scenario where this logic fails completely.
3. Search for counter-evidence (simulated).
4. Assign a 'Fragility Score' (0-10).

ADVERSARIAL ATTACK:"""
        return self.brain.reason(prompt)
