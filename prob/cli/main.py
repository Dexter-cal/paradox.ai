import argparse
import sys
from prob.brain.core import ProbBrain
from prob.memory.engine import MemoryEngine
from prob.engines.whatif import WhatIfEngine
from prob.engines.guardrail import GuardrailEngine
from prob.engines.documentation import DocumentationEngine
from prob.engines.honesty import HonestyEngine
from prob.output.engine import OutputEngine

def main():
    parser = argparse.ArgumentParser(description="Prob AI - Autonomous Discovery Engine")
    parser.add_argument("command", choices=["ask", "whatif", "rules", "notes", "report", "paper", "book"], help="Command to run")
    parser.add_argument("--query", help="The question or scenario")
    parser.add_argument("--rule", help="Rule to add/remove")
    parser.add_argument("--index", type=int, help="Index of rule to remove")
    parser.add_argument("--topic", help="Topic for the book")

    args = parser.parse_args()

    # Initialize components lazily
    memory = MemoryEngine()
    guardrail = GuardrailEngine()
    honesty = HonestyEngine()
    output = OutputEngine()
    doc_engine = DocumentationEngine(memory)

    if args.command in ["ask", "whatif"]:
        if not args.query:
            print("Error: --query is required for this command.")
            sys.exit(1)

        brain = ProbBrain()

        # Add guardrails to brain prompt if enabled
        system_rules = guardrail.get_system_prompt_addition()
        prompt = args.query + system_rules

        if args.command == "whatif":
            engine = WhatIfEngine(brain, memory)
            print(f"Prob is exploring scenario: {args.query}...")
            result = engine.explore(args.query)
        else:
            print(f"Prob is reasoning about: {args.query}...")
            result = brain.reason(prompt)

        # Honesty Check
        h_eval = honesty.evaluate(result)

        print("\n--- RESULT ---")
        print(result)
        print("\n--- HONESTY EVALUATION ---")
        print(f"Confidence: {h_eval['confidence']}")
        for flag in h_eval['flags']:
            print(f"FLAG: {flag}")

    elif args.command == "rules":
        if args.rule:
            guardrail.add_rule(args.rule)
            print(f"Added rule: {args.rule}")
        elif args.index is not None:
            guardrail.remove_rule(args.index)
            print(f"Removed rule at index {args.index}")
        elif args.query == "disable":
            guardrail.toggle(False)
            print("Guardrails DISABLED.")
        elif args.query == "enable":
            guardrail.toggle(True)
            print("Guardrails ENABLED.")
        else:
            print("Current Rules:")
            for i, rule in enumerate(guardrail.rules["rules"]):
                print(f"{i}: {rule}")
            print(f"Status: {'Enabled' if guardrail.rules['enabled'] else 'Disabled'}")

    elif args.command == "notes":
        notes = memory.get_all_notes()
        print("Recent Activity Log:")
        for note in notes[-10:]:
            print(f"[{note['timestamp']}] {note['action']}: {str(note['details'])[:100]}...")

    elif args.command == "paper":
        if not args.query:
             print("Error: --query is required for paper generation.")
             sys.exit(1)
        path = doc_engine.generate_research_paper(args.query)
        if path:
            print(f"Scientific Paper generated at: {path}")
        else:
            print("No matching research found in memory for that query.")

    elif args.command == "book":
        topic = args.topic or "General Discovery"
        path = doc_engine.generate_book(topic)
        print(f"The Book of Prob generated at: {path}")

if __name__ == "__main__":
    main()
