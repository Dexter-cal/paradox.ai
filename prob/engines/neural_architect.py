from prob.brain.core import ProbBrain
import json

class NeuralArchitect:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory

    def propose_correction_plan(self):
        failures = self.memory.get_recent_failures()
        if not failures:
            return "No failures detected. Neural architecture is stable."

        failure_context = "\n".join([f"{f['task']}: {f['reason']}" for f in failures])
        prompt = f"""Failure History:
{failure_context}

Task: You are the Prob AI Neural Architect.
Analyze these failures and propose a 'Neural Correction Plan'.
Identify:
1. Target Fine-tuning Dataset (What new data do you need?)
2. Hyperparameter adjustments (LoRA rank, Alpha, Learning Rate)
3. Prompt Engineering tweaks.

CORRECTION PLAN:"""
        return self.brain.reason(prompt)
