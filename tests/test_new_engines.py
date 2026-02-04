import unittest
import os
import json
import shutil
from prob.engines.search import SearchEngine
from prob.engines.data_library import DataLibraryEngine
from prob.engines.coder import CoderEngine
from prob.engines.model_factory import ModelFactoryEngine

class TestNewEngines(unittest.TestCase):
    def test_search(self):
        search_engine = SearchEngine()
        self.assertIsNotNone(search_engine)

    def test_coder(self):
        sandbox_dir = "tests/sandbox_test_new"
        if os.path.exists(sandbox_dir):
            shutil.rmtree(sandbox_dir)
        coder = CoderEngine(sandbox_dir=sandbox_dir)
        path = coder.write_code("test.py", "print('hello')")
        self.assertTrue(os.path.exists(path))
        res = coder.execute_code("test.py")
        self.assertEqual(res["stdout"].strip(), "hello")
        shutil.rmtree(sandbox_dir)

    def test_data_library(self):
        lib_path = "tests/data_library_test_new"
        if os.path.exists(lib_path):
            shutil.rmtree(lib_path)
        data_lib = DataLibraryEngine(library_path=lib_path)
        registry = data_lib.list_local_datasets()
        self.assertEqual(registry, {})
        shutil.rmtree(lib_path)

if __name__ == "__main__":
    unittest.main()
