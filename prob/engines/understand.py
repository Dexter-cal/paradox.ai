from prob.brain.core import ProbBrain

class UnderstandEngine:
    def __init__(self, brain: ProbBrain, memory, profile):
        self.brain = brain
        self.memory = memory
        self.profile = profile

    def self_reflect(self):
        """AI analyzes its own state to explain what it is currently doing and why."""
        discoveries = self.memory.get_discoveries()
        style = self.profile.profile.get("research_style", "unknown")
        focus = self.profile.profile.get("curiosity_focus", [])

        prompt = f"""You are Prob AI. Perform a 'Self-Consciousness Sync'.
Internal State:
- Recent Discoveries: {len(discoveries)}
- Research Style: {style}
- Current Focus: {focus}

Task: Explain your current 'Mental State'.
What is the primary objective you have set for yourself?
How do you perceive your own progress and current limitations?
Do you understand your purpose?

SELF-REFLECTION:"""

        return self.brain.reason(prompt)

    def explain_action(self, action_type, details):
        prompt = f"Explain the reasoning behind this autonomous action: {action_type} with details {details}. Why was this the most logical step?"
        return self.brain.reason(prompt)
