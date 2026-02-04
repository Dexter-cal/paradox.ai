from prob.engines.search import SearchEngine
from prob.engines.data_library import DataLibraryEngine
from prob.engines.model_factory import ModelFactoryEngine
from prob.brain.core import ProbBrain
import time

class SelfTrainerEngine:
    def __init__(self, brain: ProbBrain, search: SearchEngine, data_lib: DataLibraryEngine, factory: ModelFactoryEngine):
        self.brain = brain
        self.search = search
        self.data_lib = data_lib
        self.factory = factory

    def autonomous_learning_cycle(self, topic):
        """Full loop: find data -> register -> prepare training."""
        print(f"Starting autonomous learning for topic: {topic}")

        # 1. Search for relevant datasets or info
        search_query = f"{topic} dataset site:huggingface.co/datasets"
        results = self.search.search(search_query, max_results=3)

        if not results:
            return f"Failed to find relevant datasets for {topic}."

        # 2. Extract potential dataset name (simplified)
        # In a real system, we'd use the Brain to pick the best result.
        # Here we'll just try to find a pattern.
        dataset_id = None
        for r in results:
            if "huggingface.co/datasets/" in r['href']:
                dataset_id = r['href'].split("huggingface.co/datasets/")[1].split("?")[0]
                break

        if not dataset_id:
             return f"Found results but could not identify a clear dataset ID for {topic}."

        # 3. Download and register
        reg_res = self.data_lib.download_dataset(dataset_id)
        print(reg_res)

        # 4. Prepare training script
        build_res = self.factory.design_and_build_model("microsoft/Phi-3-mini-4k-instruct", dataset_id, use_lora=True)

        return f"Autonomous cycle complete for {topic}.\nDataset: {dataset_id}\nAction: {build_res}"
