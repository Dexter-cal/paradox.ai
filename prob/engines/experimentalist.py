from prob.brain.core import ProbBrain

class ExperimentalistEngine:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def design_experiment(self, discovery):
        prompt = f"""Discovery: {discovery}

Task: Design a rigorous scientific experiment to validate this discovery.
Provide:
1. Hypothesis to be tested
2. Controlled variables
3. Experimental procedure (Step-by-step)
4. Success metrics
5. Potential edge cases or failure modes

EXPERIMENTAL PROTOCOL:"""
        return self.brain.reason(prompt)

    def provide_real_world_example(self, concept):
        prompt = f"""Concept/Discovery: {concept}

Task: Provide a concrete, real-world example or analogy that explains how this discovery would manifest in reality.
EXAMPLE:"""
        return self.brain.reason(prompt)
