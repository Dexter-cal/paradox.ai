import os
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    AutoModelForCausalLM = None
    AutoTokenizer = None
try:
    import torch
except ImportError:
    torch = None

class ModelDownloader:
    def __init__(self, cache_dir="prob/brain/models"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)

    def download(self, model_id):
        if not AutoModelForCausalLM:
            print("Error: transformers library not installed. Cannot download.")
            return None, None

        print(f"Downloading model {model_id} to {self.cache_dir}...")
        tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=self.cache_dir)

        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            cache_dir=self.cache_dir,
            torch_dtype=torch.float16 if torch and torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch and torch.cuda.is_available() else None
        )
        return tokenizer, model
