import time
import random
from prob.brain.core import ProbBrain
from prob.engines.search_engine import SearchEngine

class CuriosityDuel:
    def __init__(self, brain: ProbBrain, memory):
        self.brain = brain
        self.memory = memory
        self.search = SearchEngine()
        self.scores = {"inquisitor": 0, "solver": 0}
        self.thought_stream = []

    def log_thought(self, agent, thought):
        entry = {"agent": agent, "thought": thought, "timestamp": time.time()}
        self.thought_stream.append(entry)
        print(f"[{agent.upper()}] {thought}")

    def run_duel(self, topic):
        self.log_thought("system", f"Initiating Duel on: {topic}")

        # 1. Inquisitor: Scan and Question
        self.log_thought("inquisitor", "Scanning web for knowledge gaps...")
        context = self.search.search(topic)
        formatted_context = self.search.format_results(context)

        inquiry_prompt = f"Given this context:\n{formatted_context}\n\nGenerate 3 deep, challenging research questions that remain unanswered or controversial regarding {topic}."
        questions_raw = self.brain.reason(inquiry_prompt)
        self.log_thought("inquisitor", f"Formulated Questions:\n{questions_raw}")
        self.scores["inquisitor"] += 10 # Reward for inquiry

        # 2. Solver: Take one question and solve
        question = questions_raw.split("\n")[0] # Just take the first for the duel loop
        self.log_thought("solver", f"Attempting to solve: {question}")

        solve_prompt = f"Research and provide a reasoned hypothesis for this question: {question}. Use probabilistic logic."
        answer = self.brain.reason(solve_prompt)
        self.log_thought("solver", f"Proposed Solution:\n{answer}")

        # 3. Validation & Reward
        validation = self.brain.reason(f"Evaluate the logic of this answer: {answer}. Is it coherent?")
        if "yes" in validation.lower() or "coherent" in validation.lower():
            self.log_thought("system", "Solution validated. Solver awarded credits.")
            self.scores["solver"] += 15
        else:
            self.log_thought("system", "Solution rejected. Inquisitor wins this round.")
            self.scores["inquisitor"] += 5

        self.memory.store_discovery(f"Duel: {topic}", f"Q: {question}\nA: {answer}\nScores: {self.scores}")
        return {"questions": questions_raw, "answer": answer, "scores": self.scores}

    def get_stream(self):
        return self.thought_stream
