from prob.brain.core import ProbBrain

class HonestyEngine:
    def __init__(self, brain: ProbBrain = None):
        self.brain = brain

    def evaluate(self, query, result):
        # In a real system, this might use another AI model to check the 'result'
        confidence = 0.85
        flags = []

        if "i am not sure" in result.lower() or "uncertain" in result.lower():
            confidence = 0.5
            flags.append("Low confidence detected in response.")

        sensitive_keywords = ["virus", "chemical", "weapon", "illegal", "medical", "hiv"]
        is_sensitive = any(word in result.lower() or word in query.lower() for word in sensitive_keywords)

        return result, is_sensitive
