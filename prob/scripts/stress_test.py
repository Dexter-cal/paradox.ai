import sys
import os
import json

# Add root to path
sys.path.append(os.getcwd())

from prob.brain.core import ProbBrain
from prob.engines.what_if import WhatIfEngine
from prob.engines.search_engine import SearchEngine
from prob.memory.memory_engine import MemoryEngine
from prob.engines.doc_engine import DocumentationEngine

def stress_test():
    print("PROB AI: CREATIVE STRESS TEST - MISSION INITIATED")
    print("-----------------------------------------------")

    brain = ProbBrain()
    memory = MemoryEngine()
    wi = WhatIfEngine(brain, memory)
    search = SearchEngine()
    doc = DocumentationEngine(memory)

    scenario = "What if human civilization discovered a way to transmit high-voltage electricity wirelessly using the nitrogen in Earth's atmosphere as a semi-conductive medium?"

    print(f"\n[STEP 1] Running What-If Simulation for: {scenario[:50]}...")
    simulation_result = wi.simulate(scenario)
    print("Simulation complete.")

    print("\n[STEP 2] Searching for related scientific concepts (Nitrogen ionization, wireless power)...")
    search_results = search.search("Nitrogen ionization wireless power transmission Tesla")
    print(f"Found {len(search_results)} related sources.")

    print("\n[STEP 3] Logging discovery to memory...")
    memory.store_discovery(scenario, simulation_result)

    print("\n[STEP 4] Generating Research Paper via Documentation Engine...")
    paper_path = doc.generate_research_paper(scenario)
    print(f"Research Paper generated at: {paper_path}")

    print("\n[STEP 5] Generating Summary...")
    from prob.engines.progress_summarizer import ProgressSummarizer
    sum_eng = ProgressSummarizer(memory, brain)
    print(sum_eng.generate_daily_summary())

    print("\nSTRESS TEST COMPLETE. PROB AI IS FULLY OPERATIONAL.")

if __name__ == "__main__":
    stress_test()
