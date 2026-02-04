from datetime import datetime
from prob.memory.memory_engine import MemoryEngine
from prob.brain.core import ProbBrain

class ProgressSummarizer:
    def __init__(self, memory: MemoryEngine, brain: ProbBrain = None):
        self.memory = memory
        self.brain = brain

    def generate_daily_summary(self):
        notes = self.memory.get_all_notes()
        today = datetime.now().date().isoformat()

        today_notes = [n for n in notes if n['timestamp'].startswith(today)]

        if not today_notes:
            return "No activity recorded for today yet."

        summary = f"Progress Report for {today}: "
        actions = {}
        for n in today_notes:
            a = n['action']
            actions[a] = actions.get(a, 0) + 1

        items = [f"{count} {action.replace('_', ' ')}" for action, count in actions.items()]
        summary += ", ".join(items) + "."

        return summary
