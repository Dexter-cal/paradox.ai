import unittest
import os
import shutil
from prob.brain.model_selector import ModelSelector
from prob.memory.engine import MemoryEngine
from prob.engines.whatif import WhatIfEngine
from prob.engines.guardrail import GuardrailEngine
from prob.output.engine import OutputEngine

class TestImports(unittest.TestCase):
    def test_selector(self):
        selector = ModelSelector()
        hardware = selector.detect_hardware()
        self.assertIn("vram", hardware)

    def test_memory(self):
        test_path = "tests/memory_test_unique"
        if os.path.exists(test_path):
            shutil.rmtree(test_path)
        memory = MemoryEngine(storage_path=test_path)
        memory.log_action("test", {"foo": "bar"})
        notes = memory.get_all_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["action"], "test")
        shutil.rmtree(test_path)

    def test_guardrail(self):
        config_path = "tests/guardrails_test_unique.json"
        if os.path.exists(config_path):
            os.remove(config_path)
        guardrail = GuardrailEngine(config_path=config_path)
        guardrail.add_rule("Test Rule")
        self.assertIn("Test Rule", guardrail.rules["rules"])
        os.remove(config_path)

if __name__ == "__main__":
    unittest.main()
