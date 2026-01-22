# PROB AI | COMPREHENSIVE DOCUMENTATION (v14.0.0 "Conscious Sovereign")

## Overview
Prob AI (also known as ROB) is an autonomous, self-directed discovery and reasoning engine. Unlike traditional chatbots, Prob is designed to hunt for ignorance, generate novel hypotheses, and simulate complex scenarios through its "What-If" engine.

## Core Architecture
The system is built on a modular "Engine" architecture. Every capability is a standalone class that can be called by the Brain or the UI.

### 1. The Brain (`prob/brain/`)
- **ProbBrain:** The central intelligence core. It manages model selection, quantization (4-bit/8-bit), and hardware optimization. It uses `transformers` and `torch`.
- **ModelSelector:** Automatically detects if you are on a CPU, single GPU, or multi-GPU setup and picks the best open-source model (LLaMA-3, Qwen, etc.).
- **Downloader:** Manages background model weight downloads to the cloud storage or local cache.

### 2. Strategic Engines (`prob/engines/`)
- **WhatIfEngine:** The heart of Prob. It simulates second-order effects and causal chains.
- **SwarmEngine:** Allows Prob to spawn multiple "sub-agents" to research different parts of a problem concurrently.
- **CuriosityDuel:** Orchestrates a debate between two agents: the "Inquisitor" (asks hard questions) and the "Solver" (proposes solutions).
- **RedTeamAdversary:** Actively tries to find flaws in Prob's own discoveries.
- **CouncilOfConsensus:** A multi-persona deliberation engine where different specialized identities (Scientist, Philosopher, Engineer) review a finding.

### 3. Scientific & Discovery Engines
- **QuantumLogicEngine:** Designs theoretical quantum algorithms for complex optimization problems.
- **SymEngine:** Formalizes discoveries into LaTeX-ready mathematical equations.
- **LexiconCreator:** Coins new terminology for novel concepts.
- **TemporalAnchor:** Simulates how a discovery would be viewed from different historical or future timelines.
- **KnowledgeGraphPro:** Builds an evolving visual map of all entities and their relationships.

### 4. Safety & Oversight
- **HonestyEngine:** Analyzes responses for confidence and marks speculative vs. verified information.
- **GuardrailEngine:** A natural-language-configurable system to add or remove constraints (e.g., "Do not simulate biological weapons").
- **UnderstandEngine:** A meta-reflective module that allows Prob to explain *why* it is taking a certain action.
- **KillSwitchEngine:** Emergency halt for all background autonomous loops.

### 5. Memory & Output
- **MemoryEngine:** Persistent storage for notes, failures, and successes using JSON and Vector DBs.
- **DocEngine:** Generates Research Papers, Books, and Datasets in `.md`, `.txt`, and `.csv` formats.
- **WikiEngine:** Automatically maintains a "Prob Wiki" summarizing all its knowledge.

## Launching Prob
Prob is optimized for Google Colab and local servers.
- **Web UI:** A professional Flask-based dashboard accessible on port 5000.
- **CLI:** A terminal interface for direct engine interaction.

## Autonomous Loop
Prob can enter an "Autonomous Mode" where it identifies its own gaps in knowledge, searches the web, trains itself on new concepts, and records discoveries without human prompting.

---
*Created by Prob AI Documentation Engine*
