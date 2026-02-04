from prob.brain.core import ProbBrain

class LexiconCreator:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def coin_term(self, discovery):
        prompt = f"""Discovery: {discovery}

Task: This discovery describes a phenomenon that does not yet have a name in the human lexicon.
Coin a new, scientifically-grounded term for this discovery.
The name should ideally have Latin or Greek roots but sound modern.
Provide:
1. THE TERM
2. Etymology (Roots)
3. Definition

NEOLOGISM:"""
        return self.brain.reason(prompt)
