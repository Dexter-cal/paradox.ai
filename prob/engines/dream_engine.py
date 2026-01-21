import random
import time
import threading
from prob.brain.core import ProbBrain

class DreamEngine:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory
        self.is_dreaming = False
        self.dreams = []

    def start_dream_cycle(self):
        """Spawns a background thread to 'dream' (combine random concepts)."""
        self.is_dreaming = True
        thread = threading.Thread(target=self._dream_loop)
        thread.daemon = True
        thread.start()

    def _dream_loop(self):
        while self.is_dreaming:
            try:
                # 1. Pull random discoveries from memory
                discoveries = self.memory.get_discoveries()
                if len(discoveries) < 2:
                    time.sleep(60)
                    continue

                d1 = random.choice(discoveries)
                d2 = random.choice(discoveries)

                # 2. Combinatorial Innovation Prompt
                prompt = f"""You are in Prob's Dream State (Combinatorial Innovation).
Take these two seemingly unrelated findings:
1. {d1['query']}: {d1['result'][:200]}
2. {d2['query']}: {d2['result'][:200]}

Task: Find a 'Hidden Bridge'. Is there a third, novel concept that emerges from combining these two?
If so, describe it as a 'Dream Synthesis'. If not, say 'Dissociation'."""

                synthesis = self.brain.reason(prompt)

                if "Dissociation" not in synthesis:
                    dream_entry = {
                        "timestamp": time.time(),
                        "source_a": d1['query'],
                        "source_b": d2['query'],
                        "synthesis": synthesis
                    }
                    self.dreams.append(dream_entry)
                    self.memory.log_action("dream_synthesis", dream_entry)

            except Exception as e:
                print(f"Dream interruption: {e}")

            # Dream every 5 minutes during idle
            time.sleep(300)

    def get_dreams(self):
        return self.dreams
