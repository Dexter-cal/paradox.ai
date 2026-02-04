import json
import os
import threading
import time
from prob.brain.core import ProbBrain
from prob.engines.search_engine import SearchEngine
from prob.engines.data_library import DataLibraryEngine

class SwarmEngine:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory
        self.search = SearchEngine()
        self.data_lib = DataLibraryEngine()
        self.active_tasks = {}
        self.lock = threading.Lock()

    def spawn_mission(self, topic, mission_type="discovery"):
        """Spawns a background thread for a specific mission."""
        task_id = f"task_{int(time.time())}_{topic[:10].replace(' ', '_')}"
        thread = threading.Thread(target=self._run_mission, args=(task_id, topic, mission_type))
        thread.daemon = True

        with self.lock:
            self.active_tasks[task_id] = {
                "topic": topic,
                "type": mission_type,
                "status": "active",
                "start_time": time.time(),
                "progress": 0
            }

        thread.start()
        return task_id

    def _run_mission(self, task_id, topic, mission_type):
        try:
            # 1. Intelligence Gathering
            self._update_task(task_id, progress=20)
            context = self.search.search(topic)

            # 2. Reasoning Loop
            self._update_task(task_id, progress=50)
            result = self.brain.reason(f"Mission: {mission_type} on {topic}. Context: {context}")

            # 3. Validation / Critique
            self._update_task(task_id, progress=80)
            critique = self.brain.reason(f"Critique the following research finding: {result}")

            # 4. Finalization
            self.memory.store_discovery(topic, f"RESULT: {result}\n\nCRITIQUE: {critique}")
            self._update_task(task_id, status="completed", progress=100)

        except Exception as e:
            self._update_task(task_id, status=f"failed: {str(e)}")

    def _update_task(self, task_id, **kwargs):
        with self.lock:
            if task_id in self.active_tasks:
                self.active_tasks[task_id].update(kwargs)

    def get_status(self):
        with self.lock:
            return self.active_tasks
