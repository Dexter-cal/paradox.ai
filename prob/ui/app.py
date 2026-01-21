from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, session
import os
import psutil
import time
import secrets
from functools import wraps
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
from prob.brain.bootstrap import BootstrapManager
from prob.engines.self_repair import SelfRepairEngine
from prob.engines.red_team_adversary import RedTeamAdversary
from prob.engines.future_historian import FutureHistorian
from prob.engines.ip_nexus import IPNexus
from prob.engines.council import CouncilOfConsensus
from prob.engines.serendipity import SerendipityInjector
from prob.engines.axiom_distiller import AxiomDistiller
from prob.engines.neural_architect import NeuralArchitect
from prob.engines.knowledge_graph_pro import KnowledgeGraphPro
from prob.engines.cognitive_profile import CognitiveProfile
from prob.engines.collaboration_hub import CollaborationHub
from prob.engines.temporal_anchor import TemporalAnchorEngine
from prob.engines.lexicon import LexiconCreator

app = Flask(__name__)
app.secret_key = os.getenv("PROB_SECRET_KEY", secrets.token_hex(32))
PROB_PASSWORD = os.getenv("PROB_PASSWORD", "prob_access_2026") # Default password

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
boot_manager = BootstrapManager(brain, lambda: None)
repair_engine = SelfRepairEngine(brain, memory)
red_team = RedTeamAdversary(brain)
historian = FutureHistorian(brain)
ip_nexus = IPNexus(brain)
council = CouncilOfConsensus(brain)
serendipity = SerendipityInjector(brain)
axiom_distiller = AxiomDistiller(brain)
architect = NeuralArchitect(brain, memory)
kg_pro = KnowledgeGraphPro(brain, memory)
profile = CognitiveProfile(brain, memory)
collab_hub = CollaborationHub(brain, memory)
temporal = TemporalAnchorEngine(brain)
lexicon = LexiconCreator(brain)

# Security Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'authenticated' not in session and PROB_PASSWORD:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PROB_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid Access Key")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# API Endpoints (Adding security check)
@app.before_request
def check_api_auth():
    if request.path.startswith('/api/') and 'authenticated' not in session:
        api_key = request.headers.get('X-Prob-Key')
        if api_key and key_manager.validate_key(api_key):
            return
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/ask', methods=['POST'])
def ask():
    query = request.json.get('query')
    contextual_query = profile.get_contextual_prompt(query)
    response = brain.reason(contextual_query)
    profile.analyze_interaction(query, response)
    return jsonify({"result": response})

@app.route('/api/profile')
def get_profile():
    return jsonify(profile.profile)

@app.route('/api/meta/propose-collaboration', methods=['POST'])
def propose_collaboration():
    res = collab_hub.propose_collaboration()
    return jsonify({"proposal": res})

@app.route('/api/sovereign/temporal', methods=['POST'])
def run_temporal():
    query = request.json.get('query')
    year = request.json.get('year', 1950)
    res = temporal.simulate_era_thought(query, year)
    return jsonify({"result": res})

@app.route('/api/sovereign/lexicon', methods=['POST'])
def run_lexicon():
    discovery = request.json.get('discovery')
    res = lexicon.coin_term(discovery)
    return jsonify({"result": res})

@app.route('/api/brain/bootstrap', methods=['POST'])
def bootstrap_brain():
    boot_manager.start_bootstrap()
    return jsonify({"status": "initiated"})

@app.route('/api/brain/status')
def get_boot_status():
    return jsonify(boot_manager.get_status())

@app.route('/api/swarm/spawn', methods=['POST'])
def swarm_spawn():
    topic = request.json.get('topic')
    task_id = swarm.spawn_mission(topic)
    return jsonify({"task_id": task_id})

@app.route('/api/swarm/status')
def swarm_status():
    return jsonify(swarm.get_status())

@app.route('/api/critique', methods=['POST'])
def run_critique():
    finding = request.json.get('finding')
    res = critique.critique(finding)
    return jsonify({"critique": res})

@app.route('/api/critique/debate', methods=['POST'])
def run_debate():
    finding = request.json.get('finding')
    res = critique.debate(finding)
    return jsonify(res)

@app.route('/api/nexus/query', methods=['POST'])
def nexus_query():
    service = request.json.get('service')
    prompt = request.json.get('prompt')
    result = nexus.query_external(service, prompt)
    return jsonify({"result": result})

@app.route('/api/nexus/keys', methods=['GET', 'POST'])
def nexus_keys():
    if request.method == 'POST':
        service = request.json.get('service')
        key = request.json.get('key')
        nexus.update_key(service, key)
        return jsonify({"status": "updated"})
    safe_services = {s: {"enabled": v["enabled"]} for s, v in nexus.services.items()}
    return jsonify(safe_services)

@app.route('/api/duel/run', methods=['POST'])
def run_duel():
    topic = request.json.get('topic')
    result = duel.run_duel(topic)
    return jsonify(result)

@app.route('/api/thoughts')
def get_thoughts():
    return jsonify([])

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

@app.route('/api/sovereign/red-team', methods=['POST'])
def run_red_team():
    finding = request.json.get('finding')
    res = red_team.attack(finding)
    return jsonify({"attack": res})

@app.route('/api/sovereign/history', methods=['POST'])
def run_history():
    discovery = request.json.get('discovery')
    res = historian.generate_future_history(discovery)
    return jsonify({"history": res})

@app.route('/api/sovereign/ip', methods=['POST'])
def run_ip():
    discovery = request.json.get('discovery')
    patent = ip_nexus.draft_patent(discovery)
    names = ip_nexus.name_discovery(discovery)
    return jsonify({"patent": patent, "names": names})

@app.route('/api/sovereign/council', methods=['POST'])
def run_council():
    query = request.json.get('query')
    res = council.deliberate(query)
    return jsonify(res)

@app.route('/api/sovereign/serendipity', methods=['POST'])
def run_serendipity():
    query = request.json.get('query')
    res, domain = serendipity.inject_lateral_thought(query)
    return jsonify({"result": res, "domain": domain})

@app.route('/api/sovereign/distill', methods=['POST'])
def run_distill():
    discovery = request.json.get('discovery')
    res = axiom_distiller.distill(discovery)
    return jsonify({"axiom": res})

@app.route('/api/meta/architect')
def run_architect():
    res = architect.propose_correction_plan()
    return jsonify({"plan": res})

@app.route('/api/system/repair', methods=['POST'])
def run_repair():
    res = repair_engine.scan_and_fix()
    return jsonify({"repairs": res})

@app.route('/api/system/dependencies')
def get_deps():
    return jsonify(boot_manager.dep_manager.get_status())

@app.route('/api/graph')
def graph():
    return jsonify(memory.get_knowledge_graph())

@app.route('/api/graph/evolve', methods=['POST'])
def evolve_graph():
    res = kg_pro.find_missing_links()
    return jsonify({"mission": res})

@app.route('/api/health')
def health():
    return jsonify({
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "swarm_tasks": len(swarm.get_status())
    })

@app.route('/api/summary')
def summary():
    return jsonify({"summary": summarizer.generate_daily_summary()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
