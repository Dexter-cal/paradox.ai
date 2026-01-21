from prob.brain.core import ProbBrain

class EpistemicIgnoranceMap:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory
        self.unknowns = []

    def identify_boundary(self, topic):
        """Attempts to map what is NOT known about a topic."""
        prompt = f"""Topic: {topic}

Based on current scientific consensus, identify the 'Event Horizon' of knowledge for this topic.
What are the 3 most critical questions that are currently impossible to answer with existing data?
List them as 'THE UNKNOWN'."""

        res = self.brain.reason(prompt)
        entry = {"topic": topic, "boundaries": res}
        self.unknowns.append(entry)
        self.memory.log_action("epistemic_mapping", entry)
        return res

    def get_map(self):
        return self.unknowns
