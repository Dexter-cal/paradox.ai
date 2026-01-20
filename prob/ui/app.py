from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import psutil
import secrets
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
import matplotlib.pyplot as plt

app = Flask(__name__)

# Initialize Engines
brain = ProbBrain()
memory = MemoryEngine()
whatif_engine = WhatIfEngine(brain, memory)
honesty = HonestyEngine(brain)
doc_engine = DocumentationEngine(memory)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    api_key = request.headers.get('X-Prob-Key')
    if api_key and not key_manager.validate_key(api_key):
        return jsonify({"error": "Invalid API Key"}), 403

    query = request.json.get('query')
    allowed, message = guardrails.check(query)
    if not allowed:
        return jsonify({"result": f"BLOCKED: {message}"})

    response = brain.reason(query)
    extractor.extract_and_store(response)
    result, is_sensitive = honesty.evaluate(query, response)

    if is_sensitive:
        memory.store_discovery(query, response, sensitive=True)
        return jsonify({"result": "Finding secured in sensitive vault for review."})

    memory.store_discovery(query, response)

    if request.json.get('structured'):
        steps = ["Analyzing intent...", "Querying graph...", "Simulating outcomes..."]
        return jsonify({"result": {"full": response, "steps": steps}})
    return jsonify({"result": response})

@app.route('/api/swarm/spawn', methods=['POST'])
def swarm_spawn():
    topic = request.json.get('topic')
    m_type = request.json.get('type', 'discovery')
    task_id = swarm.spawn_mission(topic, m_type)
    return jsonify({"task_id": task_id, "status": "initiated"})

@app.route('/api/swarm/status')
def swarm_status():
    return jsonify(swarm.get_status())

@app.route('/api/critique', methods=['POST'])
def run_critique():
    finding = request.json.get('finding')
    perspective = request.json.get('perspective', 'Scientific Rigor')
    result = critique.critique(finding, perspective)
    return jsonify({"critique": result})

@app.route('/api/critique/debate', methods=['POST'])
def run_debate():
    finding = request.json.get('finding')
    result = critique.debate(finding)
    return jsonify(result)

@app.route('/api/nexus/query', methods=['POST'])
def nexus_query():
    service = request.json.get('service')
    prompt = request.json.get('prompt')
    result = nexus.query_external(service, prompt)
    return jsonify({"result": result})

@app.route('/api/whatif', methods=['POST'])
def whatif():
    scenario = request.json.get('scenario')
    result = whatif_engine.simulate(scenario)
    memory.store_discovery(f"WHAT-IF: {scenario}", result)
    return jsonify({"result": result})

@app.route('/api/search', methods=['POST'])
def search_web():
    query = request.json.get('query')
    results = search.search(query)
    return jsonify(results)

@app.route('/api/health')
def health():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "swarm_tasks": len(swarm.get_status())
    })

@app.route('/api/graph')
def graph():
    return jsonify(memory.get_knowledge_graph())

@app.route('/api/summary')
def summary():
    return jsonify({"summary": summarizer.generate_daily_summary()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
