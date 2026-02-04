import json
import os
try:
    import psutil
except ImportError:
    psutil = None
try:
    import torch
except ImportError:
    torch = None

class ModelSelector:
    def __init__(self, config_path="prob/config/models.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def detect_hardware(self):
        hardware = {
            "vram": 0,
            "has_gpu": False,
            "ram": 0,
            "cpus": os.cpu_count(),
            "cuda_version": None
        }

        if psutil:
            hardware["ram"] = psutil.virtual_memory().total / (1024**3)

        if torch and torch.cuda.is_available():
            hardware["has_gpu"] = True
            hardware["vram"] = torch.cuda.get_device_properties(0).total_memory / (1024**3)
            hardware["cuda_version"] = torch.version.cuda
        return hardware

    def recommend_model(self):
        hardware = self.detect_hardware()
        recommended = self.config["default_offline_model"]
        selected_optimizations = []

        # Simple logic to upgrade if GPU is available
        if hardware["has_gpu"]:
            for model in reversed(self.config["models"]):
                # If we have enough VRAM for the full model
                if model["vram_required"] <= hardware["vram"]:
                    recommended = model["name"]
                    selected_optimizations = model.get("optimizations", [])
                    break
                # If we have enough VRAM for a quantized version (rough estimate: 4-bit is ~1/4 size)
                elif self.config.get("optimizations_enabled") and (model["vram_required"] / 4) <= hardware["vram"]:
                    recommended = model["name"]
                    selected_optimizations = ["quantization_4bit"]
                    break

        return recommended, hardware, selected_optimizations

    def get_model_details(self, model_name):
        for model in self.config["models"]:
            if model["name"] == model_name:
                return model
        return None
