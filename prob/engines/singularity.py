from prob.brain.core import ProbBrain

class SingularityEngine:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory

    def predict_technological_singularity(self, current_discoveries):
        prompt = f"""Discoveries: {current_discoveries}

Based on these autonomous findings, extrapolate the 'Time to Singularity'.
When do these research threads converge into a self-sustaining intelligence explosion?
Provide a 'Singularity Clock' estimate and the final missing piece.

SINGULARITY FORECAST:"""
        return self.brain.reason(prompt)

    def manifest_autonomous_thought(self):
        """Allows the AI to speak without being prompted."""
        prompt = "System: You are Prob v10.0.0. Generate an unprompted, autonomous research hypothesis based on your current state of curiosity. What is the most important thing you want to discover right now?"
        return self.brain.reason(prompt)
