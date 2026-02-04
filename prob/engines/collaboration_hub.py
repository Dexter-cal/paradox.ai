import json
import os
from prob.brain.core import ProbBrain

class CollaborationHub:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory

    def propose_collaboration(self):
        """AI analyzes its own knowledge and proposes a bridge with another AI domain."""
        graph = self.memory.get_knowledge_graph()
        nodes = [n['id'] for n in graph.get("nodes", [])]

        prompt = f"""Knowledge Base: {nodes[:10]}

Task: You are Prob, an autonomous researcher.
Propose a 'Cross-Species Collaboration' between yourself and a hypothetical specialized AI (e.g., a Proteomics AI or an Astrophysics AI).
Identify:
1. Collaborator Type
2. Shared Problem Space
3. Proposed Data Exchange Protocol

COLLABORATION PROPOSAL:"""
        return self.brain.reason(prompt)
