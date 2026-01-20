import json
import os
from datetime import datetime

class EntityExtractorEngine:
    def __init__(self, storage_path="prob/memory/knowledge_graph"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        self.graph_path = os.path.join(self.storage_path, "graph.json")
        if not os.path.exists(self.graph_path):
            with open(self.graph_path, "w") as f:
                json.dump({"nodes": [], "edges": []}, f)

    def extract_entities(self, text):
        """Simple keyword-based extraction for prototype."""
        # In a real system, use an NER model (SpaCy, etc.)
        potential_entities = ["HIV", "enzyme", "inhibitor", "mosquito", "saliva", "quantum", "biology", "molecule", "synthetic", "cure"]
        found = [e for e in potential_entities if e.lower() in text.lower()]
        return found

    def update_graph(self, entities, context_id):
        with open(self.graph_path, "r") as f:
            graph = json.load(f)

        for entity in entities:
            # Add node if not exists
            if not any(n["id"] == entity for n in graph["nodes"]):
                graph["nodes"].append({"id": entity, "type": "concept"})

            # Add edge to context (simplified)
            graph["edges"].append({
                "source": context_id,
                "target": entity,
                "type": "related_to"
            })

        with open(self.graph_path, "w") as f:
            json.dump(graph, f, indent=2)
        return graph

    def get_graph(self):
        with open(self.graph_path, "r") as f:
            return json.load(f)
