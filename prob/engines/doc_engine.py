import os
import json
from datetime import datetime
from prob.memory.memory_engine import MemoryEngine
from prob.brain.core import ProbBrain

class DocumentationEngine:
    def __init__(self, memory: MemoryEngine, brain: ProbBrain = None, output_dir="prob/output/docs"):
        self.memory = memory
        self.brain = brain
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def generate_research_paper(self, scenario):
        notes = self.memory.get_all_notes()
        relevant_notes = [n for n in notes if n.get("details", {}).get("scenario") == scenario]

        if not relevant_notes:
            # Fallback: if no notes, try to generate one from brain if scenario is provided
            if self.brain:
                result = self.brain.reason(f"Write a short scientific analysis on: {scenario}")
            else:
                return None
        else:
            result = next((n["details"]["result"] for n in relevant_notes if n["action"] == "exploration_result"), "No result found")

        paper = f"""# SCIENTIFIC PAPER: {scenario.upper()}
Date: {datetime.now().strftime('%Y-%m-%d')}
Author: Prob AI Discovery Engine (v14.0.0)

## Abstract
This paper presents an autonomous reasoning analysis of the following scenario: "{scenario}".
Using probabilistic what-if engines, we explore the causal chains and potential outcomes.

## Introduction
The exploration of "{scenario}" is critical for understanding second-order effects in complex systems.
Prob AI was tasked with simulating the perturbations and recording results.

## Methods
Our methodology involves generating causal branches through a Large Language Model optimized with 4-bit quantization.
Each branch is assigned a confidence score and checked for internal contradictions.

## Results
{result}

## Discussion
The findings suggest a complex interplay of variables. Further human-led experimentation is recommended.
Prob's Honesty Engine indicates a confidence interval based on existing datasets.

## Recommended Validation Experiments
The following protocols have been generated autonomously by the Prob Experimentalist Engine:
{self._get_experiment_protocol(result)}

## References
- Prob AI Internal Memory Log (Session: {datetime.now().isoformat()})
- Global Knowledge Graph (Entity Mapped)
"""
        filename = f"paper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(paper)
        return path

    def _get_experiment_protocol(self, discovery):
        if not self.brain:
            return "Protocol generation requires an active brain link."
        prompt = f"Design a short validation experiment for: {discovery}. Output only the steps."
        return self.brain.reason(prompt)

    def generate_book(self, topic):
        """Compiles multiple research entries into a structured 'book'."""
        notes = self.memory.get_all_notes()
        book_content = f"# THE BOOK OF PROB: {topic.upper()}\n"
        book_content += f"Sub-title: An Autonomous Exploration into {topic}\n"
        book_content += f"Compiled on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        book_content += "## Preface\nThis book was written autonomously by Prob AI, documenting the failures and successes of its reasoning process.\n\n"

        found_chapters = 0
        for note in notes:
            if note["action"] == "exploration_result":
                scenario = note["details"]["scenario"]
                if topic.lower() in scenario.lower() or topic.lower() in note["details"]["result"].lower():
                    result = note["details"]["result"]
                    book_content += f"## Chapter {found_chapters + 1}: {scenario}\n\n{result}\n\n---\n\n"
                    found_chapters += 1

        if found_chapters == 0:
            book_content += "\n*No chapters found in memory for this topic. Running autonomous research...*\n"
            if self.brain:
                book_content += "\n## Summary Analysis\n"
                book_content += self.brain.reason(f"Write a comprehensive overview about {topic} for an AI-authored book.")

        filename = f"book_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(book_content)
        return path

    def generate_dataset(self, scenario):
        notes = self.memory.get_all_notes()
        relevant_notes = [n for n in notes if n.get("details", {}).get("scenario") == scenario]

        if not relevant_notes:
            return None

        filename = f"dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        path = os.path.join(self.output_dir, filename)

        with open(path, "w") as f:
            f.write("timestamp,action,details\n")
            for note in relevant_notes:
                details_str = json.dumps(note["details"]).replace('"', '""')
                f.write(f"{note['timestamp']},{note['action']},\"{details_str}\"\n")

        return path
