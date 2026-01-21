import json
import os
from prob.brain.core import ProbBrain

class KnowledgeGraphPro:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory

    def find_missing_links(self):
        """Analyzes the graph to find high-value potential connections."""
        graph = self.memory.get_knowledge_graph()
        nodes = graph.get("nodes", [])
        if len(nodes) < 3:
            return "Insufficient knowledge density for link analysis."

        # Pick random pairs to test for hidden bridges
        # In a real system, we'd use adjacency matrix analysis
        node_names = [n['id'] for n in nodes]

        prompt = f"""Knowledge Nodes: {node_names[:10]}

Task: Identify the most 'Distant' pair of concepts that could have a non-obvious, revolutionary connection.
Propose a research mission to bridge them.
Output format:
MISSION: [Name]
PAIR: [Node A] + [Node B]
HYPOTHESIS: [Reasoning]"""

        return self.brain.reason(prompt)

    def evolve_graph(self, text):
        """Advanced extraction including relationship types."""
        # This enhances the simple extractor
        prompt = f"Text: {text}\n\nTask: Extract Entities and their Relationships. Output as JSON: {{\"nodes\": [\"id\", \"type\"], \"links\": [\"source\", \"target\", \"type\"]}}"
        res = self.brain.reason(prompt)
        try:
            # Basic JSON extraction from string
            if "{" in res:
                data = json.loads(res[res.find("{"):res.rfind("}")+1])
                # Merge with existing
                # (Simplified for now)
                return data
        except:
            pass
        return None
