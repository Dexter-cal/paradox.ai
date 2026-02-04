from prob.engines.coder import CoderEngine
from prob.engines.data_library import DataLibraryEngine

class ModelFactoryEngine:
    def __init__(self, coder: CoderEngine, data_lib: DataLibraryEngine):
        self.coder = coder
        self.data_lib = data_lib

    def design_and_build_model(self, model_name, dataset_name, use_lora=False):
        """Creates a training script for a new model based on a dataset."""
        registry = self.data_lib.list_local_datasets()
        if dataset_name not in registry:
            return f"Error: Dataset {dataset_name} not found in library. Please download it first."

        if use_lora:
            code = self.generate_lora_fine_tuning_code(model_name, dataset_name)
        else:
            code = self.coder.generate_ai_model_code(model_name, dataset_name)

        prefix = "lora_" if use_lora else "train_"
        filename = f"{prefix}{dataset_name.replace('/', '_')}.py"
        path = self.coder.write_code(filename, code)

        return f"Model training script for {dataset_name} created at {path}."

    def generate_lora_fine_tuning_code(self, model_name, dataset_name):
        """Generates template code for LoRA fine-tuning."""
        code = f"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, BitsAndBytesConfig
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

model_id = "{model_name}"
dataset_id = "{dataset_name}"

print(f"Loading model {{model_id}} with 4-bit quantization...")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config, device_map="auto")

model = prepare_model_for_kbit_training(model)

config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, config)

print(f"Loading dataset {{dataset_id}}...")
dataset = load_dataset(dataset_id, split='train[:100]')

def tokenize_function(examples):
    return tokenizer(examples['text'], padding='max_length', truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

training_args = TrainingArguments(
    output_dir='./results_lora',
    num_train_epochs=1,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    warmup_steps=2,
    max_steps=10,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=1,
    push_to_hub=False,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
)

print("LoRA Fine-tuning code prepared.")
"""
        return code
