from prob.brain.core import ProbBrain
try:
    import sympy
except ImportError:
    sympy = None

class SymEngine:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def formalize_discovery(self, discovery):
        prompt = f"""Discovery: {discovery}

Task: Attempt to formalize this discovery into a mathematical equation or logical proof.
Use LaTeX format for equations.
If a formal proof is impossible, provide a symbolic representation of the variables involved.

FORMALIZATION:"""
        return self.brain.reason(prompt)

    def balance_chemistry(self, equation):
        # Simplified: uses LLM but directs it to be precise
        prompt = f"Balance this chemical equation precisely: {equation}. Provide the step-by-step stoichiometric coefficients."
        return self.brain.reason(prompt)
