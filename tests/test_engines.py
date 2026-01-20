import unittest
from prob.memory.engine import MemoryEngine
from prob.engines.documentation import DocumentationEngine
from prob.engines.honesty import HonestyEngine
import os

class TestEngines(unittest.TestCase):
    def test_documentation_and_honesty(self):
        memory = MemoryEngine(storage_path="tests/memory_engine_test")
        doc_engine = DocumentationEngine(memory, output_dir="tests/output_test")
        honesty = HonestyEngine()

        # Log a result
        scenario = "What if we have a test?"
        result = "This is a test discovery."
        memory.log_action("exploration_result", {"scenario": scenario, "result": result})

        # Generate paper
        path = doc_engine.generate_research_paper(scenario)
        self.assertTrue(os.path.exists(path))

        # Generate book
        book_path = doc_engine.generate_book("Test Topic")
        self.assertTrue(os.path.exists(book_path))

        # Honesty eval
        eval_res = honesty.evaluate(result)
        self.assertIn("confidence", eval_res)

        # Cleanup
        os.remove(path)
        os.remove(book_path)

if __name__ == "__main__":
    unittest.main()
