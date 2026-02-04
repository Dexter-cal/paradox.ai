import argparse
import sys
import json
import os

# Add root to path
sys.path.append(os.getcwd())

from prob.brain.core import ProbBrain
from prob.engines.what_if import WhatIfEngine
from prob.engines.honesty import HonestyEngine
from prob.engines.guardrail_engine import GuardrailEngine

def main():
    parser = argparse.ArgumentParser(description="Prob AI CLI")
    parser.add_argument("command", choices=["ask", "whatif", "status", "rules"])
    parser.add_argument("query", nargs="?", help="The question or scenario")
    parser.add_argument("--no-guardrails", action="store_true", help="Bypass natural language guardrails")

    args = parser.parse_args()

    brain = ProbBrain()
    guardrails = GuardrailEngine()

    if args.command == "ask":
        if not args.query:
            print("Error: Missing query.")
            return

        if not args.no_guardrails:
            allowed, msg = guardrails.check(args.query)
            if not allowed:
                print(f"BLOCKED: {msg}")
                return

        print("Thinking...")
        response = brain.reason(args.query)
        print(f"\nProb: {response}")

    elif args.command == "whatif":
        if not args.query:
            print("Error: Missing scenario.")
            return

        wi = WhatIfEngine(brain)
        print("Simulating...")
        result = wi.simulate(args.query)
        print(f"\nSimulation Results:\n{result}")

    elif args.command == "status":
        print("Prob AI v4.0.0 Status: ONLINE")
        print(f"Brain: {brain.model_name}")
        print(f"Memory: Persistent (JSON)")
        print(f"Guardrails: {len(guardrails.rules)} active rules")

    elif args.command == "rules":
        print("Active Guardrails:")
        for r in guardrails.rules:
            print(f"- {r}")

if __name__ == "__main__":
    main()
