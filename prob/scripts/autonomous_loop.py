import time
import random
import sys
import os

# Add root to path
sys.path.append(os.getcwd())

from prob.brain.core import ProbBrain
from prob.engines.search_engine import SearchEngine
from prob.engines.data_library import DataLibraryEngine
from prob.engines.self_trainer import SelfTrainerEngine
from prob.memory.memory_engine import MemoryEngine

def main():
    print("PROB AI: INDEPENDENT DISCOVERY MODE ACTIVE")
    print("------------------------------------------")

    brain = ProbBrain()
    search = SearchEngine()
    data_lib = DataLibraryEngine()
    trainer = SelfTrainerEngine(brain, search, data_lib)
    memory = MemoryEngine()

    # Curiosity Seeds
    seeds = [
        "Unsolved patterns in prime number distribution",
        "Novel carbon sequestration methods",
        "Economic impact of post-scarcity energy",
        "Bypassing biological barriers for targeted drug delivery",
        "Emergent behavior in multi-agent reinforcement learning",
        "Historical contradictions in ancient maritime civilizations",
        "Alternative chemical pathways for synthetic photosynthesis"
    ]

    while True:
        # 1. Self-scan for ignorance or pick a seed
        discovery_log = memory.get_discoveries()
        if not discovery_log:
            target = random.choice(seeds)
        else:
            # Analyze past discoveries to find a "gap" (Simplified)
            target = random.choice(seeds) # For now, rotation

        print(f"\n[AUTONOMOUS_CYCLE] Mission Target: {target}")

        try:
            result = trainer.run_autonomous_cycle(target)
            print(f"[AUTONOMOUS_CYCLE] Result Logged: {result[:100]}...")
        except Exception as e:
            print(f"[AUTONOMOUS_CYCLE] MISSION_FAILURE: {str(e)}")

        # 2. Wait between cycles to simulate thinking/cooling
        print("[AUTONOMOUS_CYCLE] Cooling down for next jump...")
        time.sleep(60)

if __name__ == "__main__":
    main()
