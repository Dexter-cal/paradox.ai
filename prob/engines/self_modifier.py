import os
import shutil
from datetime import datetime
from prob.brain.core import ProbBrain

class SelfModifierEngine:
    def __init__(self, brain: ProbBrain):
        self.brain = brain
        self.backup_dir = "prob/memory/backups"
        os.makedirs(self.backup_dir, exist_ok=True)

    def rewrite_logic(self, filepath, instruction):
        """AI-driven code modification."""
        if not os.path.exists(filepath):
            return f"Error: File {filepath} not found."

        try:
            with open(filepath, "r") as f:
                original_code = f.read()

            # Backup
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(self.backup_dir, f"{os.path.basename(filepath)}.{timestamp}.bak")
            shutil.copy2(filepath, backup_path)

            prompt = f"""System: You are Prob AI, an autonomous system capable of self-modification.
The user wants to rewrite a part of your own code.

File: {filepath}
Original Code:
```python
{original_code}
```

Instruction: {instruction}

Task: Output the complete REWRITTEN code for this file. ONLY output the code, no explanations or markdown blocks.
REWRITTEN CODE:"""

            new_code = self.brain.reason(prompt, max_new_tokens=2000)

            # Basic cleanup (remove markdown markers if LLM included them despite instructions)
            if "```python" in new_code:
                new_code = new_code.split("```python")[1].split("```")[0].strip()
            elif "```" in new_code:
                new_code = new_code.split("```")[1].strip()

            with open(filepath, "w") as f:
                f.write(new_code)

            return f"Successfully modified {filepath}. Original backed up at {backup_path}."

        except Exception as e:
            return f"Modification failed: {e}"
