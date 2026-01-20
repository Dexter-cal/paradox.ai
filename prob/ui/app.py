from flask import Flask, render_template, request, jsonify
from prob.brain.core import ProbBrain
from prob.memory.engine import MemoryEngine
from prob.engines.whatif import WhatIfEngine
from prob.engines.guardrail import GuardrailEngine
from prob.engines.documentation import DocumentationEngine
from prob.engines.honesty import HonestyEngine
from prob.engines.human_review import HumanReviewEngine
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
