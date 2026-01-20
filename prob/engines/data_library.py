import os
import json
from datasets import load_dataset

class DataLibraryEngine:
    def __init__(self, library_path="prob/memory/data_library"):
        self.library_path = library_path
        if not os.path.exists(self.library_path):
            os.makedirs(self.library_path)

        self.registry_path = os.path.join(self.library_path, "registry.json")
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, "w") as f:
                json.dump({}, f)

    def download_dataset(self, dataset_name, split="train"):
        """Downloads a dataset from Hugging Face and saves info to registry."""
        try:
            print(f"Downloading dataset {dataset_name}...")
            ds = load_dataset(dataset_name, split=split, trust_remote_code=True)

            with open(self.registry_path, "r") as f:
                registry = json.load(f)

            registry[dataset_name] = {
                "name": dataset_name,
                "split": split,
                "size": len(ds),
                "features": list(ds.features.keys())
            }

            with open(self.registry_path, "w") as f:
                json.dump(registry, f, indent=2)

            return f"Dataset {dataset_name} registered successfully. Total records: {len(ds)}"
        except Exception as e:
            return f"Error downloading dataset: {e}"

    def list_local_datasets(self):
        with open(self.registry_path, "r") as f:
            return json.load(f)
