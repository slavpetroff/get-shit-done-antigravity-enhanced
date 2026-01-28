import unittest
import json
import os
import subprocess
import time

LOG_PATH = ".gsd/logs/audit.jsonl"

class TestRankingSimulation(unittest.TestCase):
    def run_selection(self, context):
        subprocess.run(
            ["python3", "scripts/gsd_select.py", context],
            capture_output=True,
            text=True
        )
        time.sleep(0.05) # fast wait for file write

    def get_last_selection(self):
        last_entry = None
        if not os.path.exists(LOG_PATH):
            return None
            
        with open(LOG_PATH, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    last_entry = entry
                except:
                    continue
        return last_entry

    def test_python_context(self):
        self.run_selection("python coding patterns")
        entry = self.get_last_selection()
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry['context'], "python coding patterns")
        
        # Check if Python skills are selected
        # "python-patterns" or "python-expert" should be present if they exist
        # We know "python-patterns" exists from previous context
        ids = entry.get('selected_ids', [])
        
        # Check for ANY relevant python skill
        python_skills = [s for s in ids if "python" in s]
        self.assertTrue(len(python_skills) > 0, f"No python skills selected for python context. Got: {ids}")

    def test_debugging_context(self):
        self.run_selection("fix bug in production")
        entry = self.get_last_selection()
        
        ids = entry.get('selected_ids', [])
        # Check for debugger or systematic-debugging
        self.assertTrue(
            "debugger" in ids or "systematic-debugging" in ids or "test-fixing" in ids,
            f"No debugging skills selected. Got: {ids}"
        )

    def test_react_context(self):
        self.run_selection("react frontend component")
        entry = self.get_last_selection()
        
        ids = entry.get('selected_ids', [])
        # Check for react patterns or similar
        react_skills = [s for s in ids if "react" in s or "frontend" in s]
        self.assertTrue(len(react_skills) > 0, f"No react/frontend skills selected. Got: {ids}")

if __name__ == '__main__':
    unittest.main()
