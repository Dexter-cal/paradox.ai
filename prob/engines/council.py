from prob.brain.core import ProbBrain

class CouncilOfConsensus:
    def __init__(self, brain: ProbBrain):
        self.brain = brain
        self.personas = {
            "Skeptic": "Be highly critical, look for reasons why this is wrong or impossible.",
            "Dreamer": "Focus on the maximum positive potential and futuristic impact.",
            "Pragmatist": "Focus on implementation, cost, and immediate feasibility.",
            "Historian": "Compare this to past scientific breakthroughs and historical patterns.",
            "Ethicist": "Analyze the moral implications and potential for human harm or benefit."
        }

    def deliberate(self, query):
        deliberations = {}
        for name, prompt in self.personas.items():
            full_prompt = f"Role: {name}. Instruction: {prompt}\nTopic: {query}\nResponse:"
            deliberations[name] = self.brain.reason(full_prompt)

        synthesis_prompt = f"Synthesize the following 5 perspectives on '{query}':\n"
        for name, text in deliberations.items():
            synthesis_prompt += f"\n[{name}]: {text[:300]}..."

        synthesis_prompt += "\n\nTask: Provide a 'Consensus Verdict' and highlight the primary area of disagreement."
        verdict = self.brain.reason(synthesis_prompt)

        return {"deliberations": deliberations, "verdict": verdict}
