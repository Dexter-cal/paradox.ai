from prob.brain.core import ProbBrain

class IPNexus:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def draft_patent(self, discovery):
        prompt = f"""Discovery: {discovery}

Task: Draft a theoretical patent application for this discovery.
Include:
1. Theoretical Title (Creative & Technical)
2. Field of the Invention
3. Summary of 'Claims' (What makes it unique)
4. Preferred Embodiment (How it is built)

THEORETICAL PATENT:"""
        return self.brain.reason(prompt)

    def name_discovery(self, discovery):
        prompt = f"Based on this discovery: {discovery}\n\nSuggest 5 unique, scientific, and memorable names for this technology/concept."
        return self.brain.reason(prompt)
