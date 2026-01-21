from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import psutil
import time
from prob.brain.core import ProbBrain
from prob.memory.memory_engine import MemoryEngine
from prob.engines.what_if import WhatIfEngine
from prob.engines.honesty import HonestyEngine
from prob.engines.doc_engine import DocumentationEngine
from prob.engines.search_engine import SearchEngine
from prob.engines.data_library import DataLibraryEngine
from prob.engines.coder import CoderEngine
from prob.engines.model_factory import ModelFactoryEngine
from prob.engines.self_trainer import SelfTrainerEngine
from prob.engines.guardrail_engine import GuardrailEngine
from prob.engines.self_modifier import SelfModifierEngine
from prob.engines.entity_extractor import EntityExtractorEngine
from prob.engines.progress_summarizer import ProgressSummarizer
from prob.engines.api_key_manager import APIKeyManager
from prob.engines.consultant_engine import ConsultantEngine
from prob.engines.swarm_engine import SwarmEngine
from prob.engines.critique_console import CritiqueConsole
from prob.engines.external_nexus import ExternalNexus
from prob.engines.curiosity_duel import CuriosityDuel
from prob.engines.adv_dev import AdvancedDevFeatures
from prob.engines.experimentalist import ExperimentalistEngine
from prob.engines.dream_engine import DreamEngine
from prob.engines.auto_tuner import AutoTuner
from prob.engines.epistemic_map import EpistemicIgnoranceMap
from prob.engines.backcaster import BackcasterEngine

app = Flask(__name__)

# Initialize Engines
brain = ProbBrain()
memory = MemoryEngine()
whatif_engine = WhatIfEngine(brain, memory)
honesty = HonestyEngine(brain)
doc_engine = DocumentationEngine(memory, brain=brain)
search = SearchEngine()
data_lib = DataLibraryEngine()
coder = CoderEngine()
factory = ModelFactoryEngine()
trainer = SelfTrainerEngine(brain, search, data_lib)
guardrails = GuardrailEngine()
modifier = SelfModifierEngine()
extractor = EntityExtractorEngine(brain, memory)
summarizer = ProgressSummarizer(memory, brain)
key_manager = APIKeyManager()
consultants = ConsultantEngine()
swarm = SwarmEngine(brain, memory)
critique = CritiqueConsole(brain)
nexus = ExternalNexus(brain)
duel = CuriosityDuel(brain, memory)
adv = AdvancedDevFeatures(brain, memory)
experimentalist = ExperimentalistEngine(brain)
dreamer = DreamEngine(brain, memory)
tuner = AutoTuner(brain)
frontier = EpistemicIgnoranceMap(brain, memory)
backcaster = BackcasterEngine(brain)

# Start Dreaming
dreamer.start_dream_cycle()

# Real-time Thought Stream
thought_buffer = []

def add_thought(agent, msg):
    thought_buffer.append({"agent": agent, "msg": msg, "time": time.time()})
    if len(thought_buffer) > 50: thought_buffer.pop(0)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/thoughts')
def get_thoughts():
    return jsonify(thought_buffer)

@app.route('/api/duel/run', methods=['POST'])
def run_duel():
    topic = request.json.get('topic')
    add_thought("system", f"Starting curiosity duel on {topic}")
    result = duel.run_duel(topic)
    for t in duel.get_stream():
        add_thought(t['agent'], t['thought'])
    return jsonify(result)

@app.route('/api/adv/paradox', methods=['POST'])
def check_paradox():
    discovery = request.json.get('discovery')
    res = adv.detect_paradox(discovery)
    return jsonify({"result": res})

@app.route('/api/adv/forecast', methods=['POST'])
def forecast():
    discovery = request.json.get('discovery')
    res = adv.forecast_impact(discovery)
    return jsonify({"result": res})

@app.route('/api/adv/experiment', methods=['POST'])
def design_experiment():
    discovery = request.json.get('discovery')
    add_thought("experimentalist", "Designing validation protocol...")
    res = experimentalist.design_experiment(discovery)
    example = experimentalist.provide_real_world_example(discovery)
    return jsonify({"protocol": res, "example": example})

@app.route('/api/meta/dreams')
def get_dreams():
    return jsonify(dreamer.get_dreams())

@app.route('/api/meta/frontier', methods=['POST'])
def get_frontier():
    topic = request.json.get('topic')
    res = frontier.identify_boundary(topic)
    return jsonify({"result": res})

@app.route('/api/meta/optimize', methods=['POST'])
def optimize_brain():
    instr = request.json.get('instruction')
    res = tuner.optimize_system_instruction(instr)
    return jsonify({"new_instruction": res})

@app.route('/api/meta/backcast', methods=['POST'])
def run_backcast():
    outcome = request.json.get('outcome')
    year = request.json.get('year', 2040)
    res = backcaster.generate_roadmap(outcome, year)
    return jsonify({"roadmap": res})

@app.route('/api/ask', methods=['POST'])
def ask():
    query = request.json.get('query')
    add_thought("brain", f"Processing query: {query[:30]}...")
    allowed, message = guardrails.check(query)
    if not allowed:
        add_thought("guardrail", "Request BLOCKED")
        return jsonify({"result": f"BLOCKED: {message}"})

    response = brain.reason(query)
    add_thought("brain", "Reasoning complete.")
    extractor.extract_and_store(response)
    result, is_sensitive = honesty.evaluate(query, response)

    if is_sensitive:
        add_thought("honesty", "Sensitive content detected. Vaulting.")
        memory.store_discovery(query, response, sensitive=True)
        return jsonify({"result": "Finding secured in sensitive vault."})

    memory.store_discovery(query, response)
    return jsonify({"result": response})

@app.route('/api/health')
def health():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "swarm_tasks": len(swarm.get_status())
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
