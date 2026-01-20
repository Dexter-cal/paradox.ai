import unittest
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
        memory = MemoryEngine(storage_path="tests/memory_test")
        memory.log_action("test", {"foo": "bar"})
        notes = memory.get_all_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]["action"], "test")

    def test_guardrail(self):
        guardrail = GuardrailEngine(config_path="tests/guardrails_test.json")
        guardrail.add_rule("Test Rule")
        self.assertIn("Test Rule", guardrail.rules["rules"])

if __name__ == "__main__":
    unittest.main()
