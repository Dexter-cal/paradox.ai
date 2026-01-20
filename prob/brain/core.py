from prob.brain.model_selector import ModelSelector
from prob.brain.downloader import ModelDownloader
from prob.utils.network import is_online
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
try:
    from peft import PeftModel
except ImportError:
    PeftModel = None

class ProbBrain:
    def __init__(self, model_name=None):
        self.selector = ModelSelector()
        self.downloader = ModelDownloader()

        self.recommended_model, self.hardware, self.selected_optimizations = self.selector.recommend_model()

        if model_name is None:
            self.model_name = self.recommended_model
            print(f"Recommended model based on hardware: {self.model_name}")
        else:
            self.model_name = model_name

        self.model_details = self.selector.get_model_details(self.model_name)
        self.model = None
        self.tokenizer = None
        self.online = is_online()

    def load(self):
        model_id = self.model_details["id"]

        # Configure quantization if needed
        bnb_config = None
        if "quantization_4bit" in self.selected_optimizations:
            print("Enabling 4-bit quantization...")
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir=self.downloader.cache_dir)

        # Optimized loading
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            cache_dir=self.downloader.cache_dir,
            quantization_config=bnb_config,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto" if torch.cuda.is_available() else None,
            low_cpu_mem_usage=True
        )

        print(f"Model {self.model_details['name']} loaded successfully with optimizations: {self.selected_optimizations}")

    def reason(self, prompt, max_new_tokens=500, return_steps=False):
        if self.model is None:
            self.load()

        # If return_steps is true, we try to force a structured thinking process
        if return_steps:
            prompt += "\nBreak down your reasoning into Step 1, Step 2, Step 3, etc. Conclusion:"

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )

        full_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        if return_steps:
            # Simple heuristic to split steps
            parts = full_text.split("Step ")
            steps = [p.strip() for p in parts if p.strip()]
            return {"full": full_text, "steps": steps}

        return full_text

    def what_if(self, scenario, structured=True):
        prompt = f"System: You are Prob, a what-if reasoning AI. Analyze the following scenario and its consequences.\nScenario: {scenario}\nAnalysis:"
        return self.reason(prompt, return_steps=structured)
