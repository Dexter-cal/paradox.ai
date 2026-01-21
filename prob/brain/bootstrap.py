import threading
import time
import os
import subprocess
from prob.brain.downloader import ModelDownloader
from prob.brain.model_selector import ModelSelector

class BootstrapManager:
    def __init__(self, brain_core, autonomous_loop_func):
        self.brain_core = brain_core
        self.autonomous_loop_func = autonomous_loop_func
        self.downloader = ModelDownloader()
        self.selector = ModelSelector()
        self.status = "idle"
        self.progress = 0
        self.error = None

    def start_bootstrap(self):
        if self.status == "in_progress":
            return

        thread = threading.Thread(target=self._run_sequence)
        thread.daemon = True
        thread.start()

    def _run_sequence(self):
        try:
            self.status = "in_progress"
            self.progress = 10

            # 1. Select Model
            model_name, _, _ = self.selector.recommend_model()
            model_id = self.selector.get_model_details(model_name)["id"]

            # 2. Download Transformers & Model
            self.progress = 20
            print(f"[BOOTSTRAP] Initiating background download for {model_id}...")
            # This will continue even if user session ends
            self.downloader.download(model_id)

            self.progress = 80
            print("[BOOTSTRAP] Download complete. Initializing brain...")

            # 3. Load Brain
            self.brain_core.load()

            self.progress = 90
            self.status = "ready"
            print("[BOOTSTRAP] Brain ready. Launching autonomous discovery loop...")

            # 4. Immediate Start
            self.autonomous_loop_func()

            self.progress = 100
            self.status = "mission_active"

        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            print(f"[BOOTSTRAP] CRITICAL_FAILURE: {e}")

    def get_status(self):
        return {
            "status": self.status,
            "progress": self.progress,
            "error": self.error
        }
