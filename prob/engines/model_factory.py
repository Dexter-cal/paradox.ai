from prob.engines.coder import CoderEngine
from prob.engines.data_library import DataLibraryEngine

class ModelFactoryEngine:
    def __init__(self, coder: CoderEngine, data_lib: DataLibraryEngine):
        self.coder = coder
        self.data_lib = data_lib

    def design_and_build_model(self, model_name, dataset_name):
        """Creates a training script for a new model based on a dataset."""
        registry = self.data_lib.list_local_datasets()
        if dataset_name not in registry:
            return f"Error: Dataset {dataset_name} not found in library. Please download it first."

        code = self.coder.generate_ai_model_code("microsoft/Phi-3-mini-4k-instruct", dataset_name)

        filename = f"train_{dataset_name.replace('/', '_')}.py"
        path = self.coder.write_code(filename, code)

        return f"Model training script for {dataset_name} created at {path}."
