from prob.brain.core import ProbBrain
from prob.memory.memory_engine import MemoryEngine

class WhatIfEngine:
    def __init__(self, brain: ProbBrain, memory: MemoryEngine):
        self.brain = brain
        self.memory = memory

    def simulate(self, scenario, structured=True):
        self.memory.log_action("simulation_start", {"scenario": scenario})

        try:
            # Check if we've explored this before
            past_notes = self.memory.get_all_notes()
            for note in past_notes:
                if note.get("action") == "simulation_result" and note.get("details", {}).get("scenario") == scenario:
                    self.memory.log_action("cached_retrieval", {"scenario": scenario})
                    return note["details"]["result"]

            # Perform the reasoning
            result_data = self.brain.what_if(scenario, structured=structured)

            if structured and isinstance(result_data, dict):
                result = result_data["full"]
                steps = result_data["steps"]
            else:
                result = result_data
                steps = []

            self.memory.log_action("simulation_result", {
                "scenario": scenario,
                "result": result,
                "steps": steps
            })

            # Check for discoveries (simplified logic for prototype)
            if "discovery" in result.lower() or "novel" in result.lower():
                self.memory.store_discovery(f"Discovery related to: {scenario}", result)

            return result
        except Exception as e:
            self.memory.log_failure("simulation", str(e), {"scenario": scenario})
            return f"Simulation failed: {str(e)}"
