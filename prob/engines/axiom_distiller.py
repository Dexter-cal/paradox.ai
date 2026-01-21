from prob.brain.core import ProbBrain

class AxiomDistiller:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def distill(self, discovery):
        prompt = f"""Discovery: {discovery}

Task: Distill this discovery into a single, elegant 'Universal Axiom'.
The axiom should be a one-sentence fundamental truth that encapsulates the discovery's essence.
Format: 'AXIOM: [Sentence]' followed by a brief 'Constraint' (when it does NOT apply).

DISTILLATION:"""
        return self.brain.reason(prompt)
