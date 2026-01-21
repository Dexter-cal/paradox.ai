from prob.brain.core import ProbBrain

class VisualizerEngine:
    def __init__(self, brain: ProbBrain):
        self.brain = brain

    def imagine_discovery(self, discovery):
        prompt = f"""Discovery: {discovery}

Task: Generate a highly detailed, professional Text-to-Image prompt for Midjourney/DALL-E 3 that visually captures the essence of this discovery.
Include:
- Style (e.g. hyper-realistic scientific illustration, blueprint, futuristic 3D render)
- Composition
- Lighting
- Technical details to include

IMAGE PROMPT:"""
        return self.brain.reason(prompt)
