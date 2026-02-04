import unittest
import os
import shutil
from unittest.mock import MagicMock
from prob.engines.self_modifier import SelfModifierEngine

class TestSelfModifier(unittest.TestCase):
    def test_rewrite_logic(self):
        brain = MagicMock()
        brain.reason.return_value = "print('modified')"

        modifier = SelfModifierEngine(brain)

        test_file = "tests/test_to_modify.py"
        with open(test_file, "w") as f:
            f.write("print('original')")

        res = modifier.rewrite_logic(test_file, "Change to modified")

        self.assertIn("Successfully modified", res)
        with open(test_file, "r") as f:
            content = f.read()
        self.assertEqual(content, "print('modified')")

        # Cleanup
        os.remove(test_file)
        if os.path.exists(modifier.backup_dir):
            shutil.rmtree(modifier.backup_dir)

if __name__ == "__main__":
    unittest.main()
