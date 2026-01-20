# Prob AI (ROB)

Prob is an autonomous discovery, problem-solving, and reasoning engine. It is designed to hunt for unknowns, explore multiple possible outcomes through what-if simulations, and document its findings comprehensively.

## Key Features

- **Autonomous Discovery**: Generates hypotheses, simulates scenarios, and identifies gaps in knowledge.
- **Web Search**: Integrated DuckDuckGo search for real-time information retrieval.
- **Data Library & Drag-and-Drop**: Autonomous dataset management from Hugging Face and local file uploads via drag-and-drop.
- **Self-Training**: Automatically acquires knowledge, processes data, and prepares fine-tuning scripts.
- **Self-Modification**: AI can propose and apply changes to its own source code when prompted.
- **Autonomous Dependencies**: Automatically installs required Python packages via natural language prompts.
- **What-If Engine**: Explores causal chains and potential outcomes with probabilistic reasoning.
- **Self-Learning**: Logs failures and successes to improve future reasoning.
- **Documentation Engine**: Automatically generates research papers, books, and reports in multiple formats.
- **Visualization Engine**: Generates charts and analytics from research data.
- **Flexible Brain**: Supports multiple open-source models (GPT-OSS-20B, Llama-3, Phi-3, etc.) with optimizations like quantization and LoRA.
- **Guardrail Engine**: Modular safety system configurable via natural language.
- **Offline/Online Autonomy**: Works fully offline with local memory and brain, syncing only when requested.

## Architecture

1. **Core Brain**: Reasoning hub using LLMs with 4-bit quantization.
2. **Memory Engine**: Persistent notebook, failure logs, and discovery datasets organized by projects.
3. **What-If Engine**: Causal reasoning and simulation.
4. **Search Engine**: Web retrieval and information formatting.
5. **Data Library**: Dataset ingestion, registry, and local file uploads.
6. **Coder & Dependency Engine**: Code generation, sandboxed execution, and autonomous package management.
7. **Model Factory**: Design and build fine-tuning loops (LoRA) for new AI models.
8. **Documentation Engine**: Narrative generation and multi-format output (.md, .csv).
9. **Visualization Engine**: Research analytics and chart generation.
10. **Guardrail Engine**: Natural language safety controls.
11. **Honesty Engine**: Confidence scoring and sensitivity checks.
12. **Human Review**: Vault for sensitive findings requiring approval.

## Usage

### CLI

```bash
# Ask a question
python3 -m prob.cli.main ask --query "Why don't mosquitoes spread HIV?"

# Run a what-if simulation
python3 -m prob.cli.main whatif --query "What if a synthetic enzyme inhibited HIV replication?"

# Search the web
python3 -m prob.cli.main search --query "latest HIV research"

# Autonomous Learning
python3 -m prob.cli.main learn --topic "Quantum Biology"

# Self-Modification
python3 -m prob.cli.main rewrite --filename "prob/engines/honesty.py" --instruction "Add a check for X"

# Manage dependencies
python3 -m prob.cli.main ask --query "install numpy"
```

### UI

Prob features a modern, professional dark-themed dashboard with multiple tabs:
- **Research**: Perform What-If simulations, Deep Dives, and Visualization.
- **Chat**: Interactive agent interface with command support (learn about, rewrite, install).
- **Data Library**: Manage datasets and search the web.
- **Coder**: Sandboxed code execution.
- **Models**: Build and fine-tune models.
- **Learning**: Upload local datasets and trigger autonomous learning cycles.

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
