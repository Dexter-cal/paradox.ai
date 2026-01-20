from flask import Flask, render_template, request, jsonify
from prob.brain.core import ProbBrain
from prob.memory.engine import MemoryEngine
from prob.engines.whatif import WhatIfEngine
from prob.engines.guardrail import GuardrailEngine
from prob.engines.documentation import DocumentationEngine
from prob.engines.honesty import HonestyEngine
from prob.engines.human_review import HumanReviewEngine
from prob.engines.search import SearchEngine
from prob.engines.data_library import DataLibraryEngine
from prob.engines.coder import CoderEngine
from prob.engines.model_factory import ModelFactoryEngine
from prob.output.engine import OutputEngine
import os

app = Flask(__name__)

# Lazy initialization
brain = None
memory = MemoryEngine()
guardrail = GuardrailEngine()
output = OutputEngine()
doc_engine = DocumentationEngine(memory)
honesty = HonestyEngine()
review_engine = HumanReviewEngine()
search_engine = SearchEngine()
data_lib = DataLibraryEngine()
coder = CoderEngine()
factory = ModelFactoryEngine(coder, data_lib)

def get_brain():
    global brain
    if brain is None:
        brain = ProbBrain()
    return brain

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query')
    b = get_brain()
    res = b.reason(query + guardrail.get_system_prompt_addition())
    h_eval = honesty.evaluate(res)
    if h_eval["sensitive"]:
        review_engine.flag_for_review(query, res, h_eval["flags"])
    return jsonify({"result": res, "honesty": h_eval})

@app.route('/api/whatif', methods=['POST'])
def whatif():
    data = request.json
    scenario = data.get('scenario')
    b = get_brain()
    engine = WhatIfEngine(b, memory)
    res = engine.explore(scenario)
    h_eval = honesty.evaluate(res)
    return jsonify({"result": res, "honesty": h_eval})

@app.route('/api/docs/paper', methods=['POST'])
def generate_paper():
    data = request.json
    scenario = data.get('scenario')
    path = doc_engine.generate_research_paper(scenario)
    return jsonify({"path": path})

@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify(memory.get_all_notes())

@app.route('/api/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    results = search_engine.search(query)
    return jsonify(results)

@app.route('/api/datasets', methods=['GET', 'POST'])
def datasets():
    if request.method == 'POST':
        data = request.json
        res = data_lib.download_dataset(data.get('dataset'))
        return jsonify({"result": res})
    return jsonify(data_lib.list_local_datasets())

@app.route('/api/code/execute', methods=['POST'])
def execute_code():
    data = request.json
    filename = data.get('filename')
    res = coder.execute_code(filename)
    return jsonify(res)

@app.route('/api/models/build', methods=['POST'])
def build_model():
    data = request.json
    res = factory.design_and_build_model("Phi-3-mini", data.get('dataset'))
    return jsonify({"result": res})

@app.route('/api/review', methods=['GET', 'POST'])
def handle_review():
    if request.method == 'POST':
        data = request.json
        review_engine.approve(data['id'])
    return jsonify(review_engine.get_pending())

@app.route('/api/rules', methods=['GET', 'POST'])
def handle_rules():
    if request.method == 'POST':
        data = request.json
        if 'rule' in data:
            guardrail.add_rule(data['rule'])
        elif 'remove_index' in data:
            guardrail.remove_rule(data['remove_index'])
        elif 'toggle' in data:
            guardrail.toggle(data['toggle'])
    return jsonify(guardrail.rules)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
