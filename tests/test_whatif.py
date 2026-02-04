import unittest
from unittest.mock import MagicMock
from prob.engines.what_if import WhatIfEngine
from prob.memory.memory_engine import MemoryEngine
import json
import os

class TestWhatIf(unittest.TestCase):
    def test_exploration(self):
        brain = MagicMock()
        brain.what_if.return_value = "This is a discovery about HIV."
        storage_path = "tests/memory_whatif"
        memory = MemoryEngine(storage_path=storage_path)

        engine = WhatIfEngine(brain, memory)
        result = engine.explore("What if HIV had a synthetic inhibitor?")

        self.assertEqual(result, "This is a discovery about HIV.")

        # Verify discovery was logged
        discovery_file = os.path.join(storage_path, "discoveries.json")
        with open(discovery_file, "r") as f:
            data = json.load(f)
        self.assertTrue(any("Discovery" in d["discovery"] for d in data))

if __name__ == "__main__":
    unittest.main()
