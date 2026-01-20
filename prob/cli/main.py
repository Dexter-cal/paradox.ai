import argparse
import sys
import json
from prob.brain.core import ProbBrain
from prob.memory.engine import MemoryEngine
from prob.engines.whatif import WhatIfEngine
from prob.engines.guardrail import GuardrailEngine
from prob.engines.documentation import DocumentationEngine
from prob.engines.honesty import HonestyEngine
from prob.engines.search import SearchEngine
from prob.engines.data_library import DataLibraryEngine
from prob.engines.coder import CoderEngine
from prob.engines.model_factory import ModelFactoryEngine
from prob.engines.self_trainer import SelfTrainerEngine
from prob.engines.self_modifier import SelfModifierEngine
from prob.output.engine import OutputEngine

def main():
    parser = argparse.ArgumentParser(description="Prob AI - Autonomous Discovery Engine")
    parser.add_argument("command", choices=["ask", "whatif", "rules", "notes", "report", "paper", "book", "search", "dataset", "code", "build_model", "learn", "rewrite"], help="Command to run")
    parser.add_argument("--query", help="The question or scenario")
    parser.add_argument("--rule", help="Rule to add/remove")
    parser.add_argument("--index", type=int, help="Index of rule to remove")
    parser.add_argument("--topic", help="Topic for the book or learning")
    parser.add_argument("--dataset", help="Dataset name on HF")
    parser.add_argument("--filename", help="Filename for code or rewrite")
    parser.add_argument("--code", help="Code to write")
    parser.add_argument("--instruction", help="Instruction for self-modification")

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

    elif args.command == "search":
        if not args.query:
            print("Error: --query is required for search.")
            sys.exit(1)
        search_engine = SearchEngine()
        results = search_engine.search(args.query)
        print(search_engine.format_results(results))

    elif args.command == "dataset":
        data_lib = DataLibraryEngine()
        if args.dataset:
            res = data_lib.download_dataset(args.dataset)
            print(res)
        else:
            print("Local Dataset Library:")
            print(json.dumps(data_lib.list_local_datasets(), indent=2))

    elif args.command == "code":
        coder = CoderEngine()
        if args.code and args.filename:
            path = coder.write_code(args.filename, args.code)
            print(f"Code written to {path}")
        elif args.filename:
            print(f"Executing {args.filename}...")
            res = coder.execute_code(args.filename)
            print(json.dumps(res, indent=2))

    elif args.command == "build_model":
        if not args.dataset:
            print("Error: --dataset is required for build_model.")
            sys.exit(1)
        coder = CoderEngine()
        data_lib = DataLibraryEngine()
        factory = ModelFactoryEngine(coder, data_lib)
        res = factory.design_and_build_model("microsoft/Phi-3-mini-4k-instruct", args.dataset, use_lora=True)
        print(res)

    elif args.command == "learn":
        if not args.topic:
            print("Error: --topic is required for learn.")
            sys.exit(1)
        brain = ProbBrain()
        search = SearchEngine()
        data_lib = DataLibraryEngine()
        coder = CoderEngine()
        factory = ModelFactoryEngine(coder, data_lib)
        trainer = SelfTrainerEngine(brain, search, data_lib, factory)
        print(f"Starting autonomous learning for {args.topic}...")
        res = trainer.autonomous_learning_cycle(args.topic)
        print(res)

    elif args.command == "rewrite":
        if not args.filename or not args.instruction:
            print("Error: --filename and --instruction are required for rewrite.")
            sys.exit(1)
        brain = ProbBrain()
        modifier = SelfModifierEngine(brain)
        print(f"Modifying {args.filename}...")
        res = modifier.rewrite_logic(args.filename, args.instruction)
        print(res)

if __name__ == "__main__":
    main()
