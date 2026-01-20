# Prob AI (ROB)

Prob is an autonomous discovery, problem-solving, and reasoning engine. It is designed to hunt for unknowns, explore multiple possible outcomes through what-if simulations, and document its findings comprehensively.

## Key Features

- **Autonomous Discovery**: Generates hypotheses, simulates scenarios, and identifies gaps in knowledge.
- **What-If Engine**: Explores causal chains and potential outcomes with probabilistic reasoning.
- **Self-Learning**: Logs failures and successes to improve future reasoning.
- **Documentation Engine**: Automatically generates research papers, books, and reports in multiple formats.
- **Flexible Brain**: Supports multiple open-source models (GPT-OSS-20B, Llama-3, Phi-3, etc.) with optimizations like quantization and LoRA.
- **Guardrail Engine**: Modular safety system configurable via natural language.
- **Offline/Online Autonomy**: Works fully offline with local memory and brain, syncing only when requested.

## Architecture

1. **Core Brain**: Reasoning hub using LLMs.
2. **Memory Engine**: Persistent notebook, failure logs, and discovery datasets.
3. **What-If Engine**: Causal reasoning and simulation.
4. **Documentation Engine**: Narrative generation and multi-format output.
5. **Guardrail Engine**: Natural language safety controls.
6. **Honesty Engine**: Confidence scoring and self-consistency checks.
7. **CLI & UI**: Multiple ways to interact with the engine.

## Usage

### CLI

```bash
# Ask a question
python3 -m prob.cli.main ask --query "Why don't mosquitoes spread HIV?"

# Run a what-if simulation
python3 -m prob.cli.main whatif --query "What if a synthetic enzyme inhibited HIV replication?"

# Manage guardrails
python3 -m prob.cli.main rules --rule "Do not generate unsafe chemical formulas"
python3 -m prob.cli.main rules --query disable

# Generate a research paper
python3 -m prob.cli.main paper --query "What if a synthetic enzyme inhibited HIV replication?"
```

### UI

Run the dashboard:
```bash
python3 -m prob.ui.app
```
Then navigate to `http://localhost:5000`.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Models and hardware preferences are configured in `prob/config/models.json`.
Guardrails are stored in `prob/config/guardrails.json`.
