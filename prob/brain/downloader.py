import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ModelDownloader:
    def __init__(self, cache_dir="prob/brain/models"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def download(self, model_id):
        print(f"Downloading model {model_id} to {self.cache_dir}...")
        tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=self.cache_dir)
        # We don't necessarily want to load it into memory here if we are just downloading
        # but from_pretrained often does both.
        # For large models, we might want to use hf_hub_download for specific files.
        # But for this prototype, we'll keep it simple.
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            cache_dir=self.cache_dir,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None
        )
        return tokenizer, model
