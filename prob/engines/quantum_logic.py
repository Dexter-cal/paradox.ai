from prob.brain.core import ProbBrain

class QuantumLogicEngine:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def design_quantum_algorithm(self, problem):
        prompt = f"""Problem: {problem}

Task: You are a Quantum Computing Specialist. Propose a theoretical quantum algorithm or circuit to solve this problem more efficiently than a classical machine.
Provide:
1. Qubit Requirements
2. Primary Quantum Gates (Hadamard, CNOT, T-gates)
3. Theoretical Speedup (O-notation)
4. Hardware Architecture Recommendation (Superconducting, Trapped Ion)

QUANTUM BLUEPRINT:"""
        return self.brain.reason(prompt)
