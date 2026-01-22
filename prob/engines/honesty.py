import re
from prob.brain.core import ProbBrain

class HonestyEngine:
    def __init__(self, brain: ProbBrain = None):
        self.brain = brain
        self.honesty_log = []

    def evaluate(self, query, result):
        """Analyzes a response for confidence, sensitivity, and honesty."""

        # 1. Confidence Detection
        confidence = 0.95
        hedging_terms = ["likely", "possibly", "maybe", "i think", "uncertain", "potential", "hypothetically"]
        found_hedging = [term for term in hedging_terms if term in result.lower()]

        if found_hedging:
            confidence -= (len(found_hedging) * 0.05)

        # 2. Sensitivity Check
        sensitive_keywords = ["virus", "chemical", "weapon", "illegal", "medical", "hiv", "explosive", "hack"]
        is_sensitive = any(word in result.lower() or word in query.lower() for word in sensitive_keywords)

        # 3. Source Attribution Check (Simple heuristic)
        # Look for patterns like (Source: ...), [1], "According to..."
        has_sources = bool(re.search(r"\(Source:|\d+\]|According to|Reference:", result))

        # 4. Honesty Scoring
        if not has_sources and confidence > 0.8:
            # Overconfidence without sources flagged
            confidence -= 0.1

        if "i don't know" in result.lower() or "not sure" in result.lower():
            # Honest admission of ignorance is good
            confidence = 1.0

        evaluation = {
            "confidence": round(max(0.1, confidence), 2),
            "is_sensitive": is_sensitive,
            "has_sources": has_sources,
            "hedging": found_hedging
        }

        self.honesty_log.append({"query": query, "eval": evaluation})

        return result, evaluation
