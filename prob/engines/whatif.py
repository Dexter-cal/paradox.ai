from prob.brain.core import ProbBrain
from prob.memory.engine import MemoryEngine

class WhatIfEngine:
    def __init__(self, brain: ProbBrain, memory: MemoryEngine):
        self.brain = brain
        self.memory = memory

    def explore(self, scenario):
        self.memory.log_action("exploration_start", {"scenario": scenario})

        try:
            # Check if we've explored this before
            past_notes = self.memory.get_all_notes()
            for note in past_notes:
                if note["action"] == "exploration_result" and note["details"]["scenario"] == scenario:
                    self.memory.log_action("cached_retrieval", {"scenario": scenario})
                    return note["details"]["result"]

            # Perform the reasoning
            result = self.brain.what_if(scenario)

            self.memory.log_action("exploration_result", {
                "scenario": scenario,
                "result": result
            })

            # Check for discoveries (simplified logic for prototype)
            if "discovery" in result.lower() or "novel" in result.lower():
                self.memory.log_discovery(f"Discovery related to: {scenario}", result)

            return result
        except Exception as e:
            self.memory.log_failure("exploration", str(e), {"scenario": scenario})
            raise e
