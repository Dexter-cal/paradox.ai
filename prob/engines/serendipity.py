import random
from prob.brain.core import ProbBrain

class SerendipityInjector:
    def __init__(self, brain: ProbBrain):
        self.brain = brain
        self.domains = ["Mycology", "Astronomy", "Quantum Mechanics", "Ancient History", "Linguistics", "Architecture", "Oceanography", "Poetry", "Game Theory", "Thermodynamics"]

    def inject_lateral_thought(self, query):
        domain = random.choice(self.domains)
        prompt = f"""Topic: {query}
Lateral Domain: {domain}

Task: Force a 'Lateral Leap'. How would a specialist in {domain} approach or solve the problem presented in '{query}'?
Find a non-obvious connection.
LATERAL INSIGHT:"""
        return self.brain.reason(prompt), domain
