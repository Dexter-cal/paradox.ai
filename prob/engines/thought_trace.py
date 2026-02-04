import json
import os
from datetime import datetime

class ThoughtTraceEngine:
    def __init__(self, storage_path="prob/memory/traces"):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def save_trace(self, scenario, steps, full_result):
        trace = {
            "id": datetime.now().strftime('%Y%m%d%H%M%S'),
            "timestamp": datetime.now().isoformat(),
            "scenario": scenario,
            "steps": steps,
            "full": full_result
        }
        path = os.path.join(self.storage_path, f"trace_{trace['id']}.json")
        with open(path, "w") as f:
            json.dump(trace, f, indent=2)
        return trace

    def list_traces(self):
        traces = []
        for filename in os.listdir(self.storage_path):
            if filename.endswith(".json"):
                with open(os.path.join(self.storage_path, filename), "r") as f:
                    traces.append(json.load(f))
        return sorted(traces, key=lambda x: x['timestamp'], reverse=True)
