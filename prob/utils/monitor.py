import psutil
import os
try:
    import torch
except ImportError:
    torch = None

def get_system_health():
    health = {
        "cpu_percent": psutil.cpu_percent(),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_used_gb": psutil.virtual_memory().used / (1024**3),
        "ram_total_gb": psutil.virtual_memory().total / (1024**3),
        "disk_percent": psutil.disk_usage('/').percent,
        "gpu": None
    }

    if torch and torch.cuda.is_available():
        health["gpu"] = {
            "name": torch.cuda.get_device_name(0),
            "vram_used_gb": torch.cuda.memory_allocated(0) / (1024**3),
            "vram_total_gb": torch.cuda.get_device_properties(0).total_memory / (1024**3),
            "vram_percent": (torch.cuda.memory_allocated(0) / torch.cuda.get_device_properties(0).total_memory) * 100
        }

    return health
