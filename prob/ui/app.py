from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
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
from prob.engines.visualization import VisualizationEngine
from prob.engines.self_trainer import SelfTrainerEngine
from prob.engines.self_modifier import SelfModifierEngine
from prob.engines.dependency import DependencyEngine
from prob.output.engine import OutputEngine
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'prob/memory/data_library/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
viz_engine = VisualizationEngine()
dep_engine = DependencyEngine()

def get_brain():
    global brain
    if brain is None:
        brain = ProbBrain()
    return brain

# Initialize engines that need brain
trainer_engine = SelfTrainerEngine(get_brain(), search_engine, data_lib, factory)
modifier_engine = SelfModifierEngine(get_brain())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/output/<path:filename>')
def serve_output(filename):
    return send_from_directory('../output', filename)

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

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        return jsonify({"message": f"File {filename} uploaded successfully to {path}", "filename": filename})

@app.route('/api/code/execute', methods=['POST'])
def execute_code():
    data = request.json
    filename = data.get('filename')
    code = data.get('code')
    if code:
        coder.write_code(filename, code)
    res = coder.execute_code(filename)
    return jsonify(res)

@app.route('/api/viz/bar', methods=['POST'])
def viz_bar():
    data = request.json
    path = viz_engine.generate_bar_chart(
        data.get('data'),
        data.get('x_label'),
        data.get('y_label'),
        data.get('title')
    )
    return jsonify({"path": path})

@app.route('/api/models/build', methods=['POST'])
def build_model():
    data = request.json
    res = factory.design_and_build_model(
        "microsoft/Phi-3-mini-4k-instruct",
        data.get('dataset'),
        use_lora=data.get('useLora', False)
    )
    return jsonify({"result": res})

@app.route('/api/learn', methods=['POST'])
def learn():
    data = request.json
    topic = data.get('topic')
    res = trainer_engine.autonomous_learning_cycle(topic)
    return jsonify({"result": res})

@app.route('/api/self-modify', methods=['POST'])
def self_modify():
    data = request.json
    filepath = data.get('filepath')
    instruction = data.get('instruction')
    res = modifier_engine.rewrite_logic(filepath, instruction)
    return jsonify({"result": res})

@app.route('/api/install', methods=['POST'])
def install():
    data = request.json
    package = data.get('package')
    res = dep_engine.install_package(package)
    return jsonify({"result": res})

@app.route('/api/deep-dive', methods=['POST'])
def deep_dive():
    data = request.json
    topic = data.get('topic')
    search_res = search_engine.search(topic)
    context = search_engine.format_results(search_res)
    prompt = f"Topic: {topic}\nContext from Web: {context}\nTask: Perform a deep dive analysis on this topic. Identify gaps in current knowledge and suggest novel hypotheses."
    analysis = get_brain().reason(prompt)
    memory.log_action("deep_dive", {"topic": topic, "result": analysis})
    return jsonify({"result": analysis})

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
