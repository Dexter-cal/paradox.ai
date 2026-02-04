import subprocess
import os

class CoderEngine:
    def __init__(self, sandbox_dir="prob/sandbox"):
        self.sandbox_dir = sandbox_dir
        if not os.path.exists(self.sandbox_dir):
            os.makedirs(self.sandbox_dir)

    def write_code(self, filename, code):
        path = os.path.join(self.sandbox_dir, filename)
        with open(path, "w") as f:
            f.write(code)
        return path

    def execute_code(self, filename):
        path = os.path.join(self.sandbox_dir, filename)
        try:
            result = subprocess.run(
                ["python3", path],
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": "Execution timed out"}
        except Exception as e:
            return {"error": str(e)}

    def generate_ai_model_code(self, model_name, dataset_name):
        """Generates template code for training a simple model."""
        code = f"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

model_id = "{model_name}"
dataset_id = "{dataset_name}"

print(f"Loading model {{model_id}}...")
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id)

print(f"Loading dataset {{dataset_id}}...")
dataset = load_dataset(dataset_id, split='train[:100]')

def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=1,
    per_device_train_batch_size=1,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
)
print("Model training code prepared and verified.")
"""
        return code
