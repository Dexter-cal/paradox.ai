from prob.brain.core import ProbBrain
from prob.memory.memory_engine import MemoryEngine

class RedTeamEngine:
    def __init__(self, brain: ProbBrain, memory: MemoryEngine):
        self.brain = brain
        self.memory = memory

    def challenge_discovery(self, discovery_id):
        # 1. Fetch discovery
        discoveries = self.memory.get_all_notes()
        discovery = next((d for d in discoveries if d.get("id") == discovery_id or d.get("action") == "discovery"), None)

        if not discovery:
            return "No discovery found to challenge."

        text = discovery.get("discovery") or discovery.get("details", {}).get("result")

        # 2. Generate counter-arguments
        prompt = f"""System: You are Prob AI acting as a Red Teamer.
Your goal is to find weaknesses in the following discovery.
Discovery: {text}

Task: Propose 3 scenarios that would DISPROVE this discovery.
Scenarios:"""

        challenges = self.brain.reason(prompt)

        # 3. Log challenges
        self.memory.log_action("red_team_challenge", {
            "target": discovery_id,
            "challenges": challenges
        })

        return challenges
