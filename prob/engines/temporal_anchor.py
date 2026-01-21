from prob.brain.core import ProbBrain

class TemporalAnchorEngine:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def simulate_era_thought(self, query, year=1950):
        prompt = f"""Current Year: {year}

Task: Analyze the following query using ONLY the scientific knowledge and cultural context available in the year {year}.
Query: {query}

HISTORICAL ANALYSIS ({year}):"""
        return self.brain.reason(prompt)

    def compare_eras(self, query, year_a=1900, year_b=2026):
        analysis_a = self.simulate_era_thought(query, year_a)
        analysis_b = self.simulate_era_thought(query, year_b)

        prompt = f"""Era A ({year_a}): {analysis_a[:400]}...
Era B ({year_b}): {analysis_b[:400]}...

Task: Compare these two eras of thought on the same topic.
What was the 'Great Leap' in understanding?
What did the past era get fundamentally wrong?

ERA COMPARISON:"""
        return self.brain.reason(prompt)
