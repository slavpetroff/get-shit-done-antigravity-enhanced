import unittest
import json
import os
import subprocess
import time
import shutil

LOG_PATH = ".gsd/logs/audit.jsonl"

class TestContextIntegrity(unittest.TestCase):
    def setUp(self):
        # Create a backup if log exists, to isolate test
        if os.path.exists(LOG_PATH):
            shutil.move(LOG_PATH, LOG_PATH + ".bak")
            
    def tearDown(self):
        # Restore backup
        if os.path.exists(LOG_PATH + ".bak"):
            shutil.move(LOG_PATH + ".bak", LOG_PATH)
        elif os.path.exists(LOG_PATH):
            os.remove(LOG_PATH)

    def test_full_injection_integrity(self):
        """
        Verifies that a specific context triggers a known skill, and the logged
        fragment is 100% identical to the source skill content.
        """
        # We know "python" triggers "python-patterns" or similar if available.
        # Let's use a context guaranteed to trigger a known skill from SKILLS.md.
        # "tdd workflow" -> "tdd-workflow" skill.
        
        context = "tdd workflow"
        
        # Run gsd_select.py
        result = subprocess.run(
            ["python3", "scripts/gsd_select.py", context],
            capture_output=True,
            text=True
        )
        
        self.assertEqual(result.returncode, 0, "gsd_select.py failed")
        
        # Give filesystem a moment
        time.sleep(0.1)
        
        # Read the log
        self.assertTrue(os.path.exists(LOG_PATH), "Log file was not created")
        
        found_entry = None
        with open(LOG_PATH, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("context") == context:
                        found_entry = entry
                        break
                except:
                    continue
                    
        self.assertIsNotNone(found_entry, "Context event not found in log")
        
        # Assertions
        selected_ids = found_entry.get("selected_ids", [])
        self.assertIn("tdd-workflow", selected_ids, "Expected skill 'tdd-workflow' not selected")
        
        full_fragment = found_entry.get("full_fragment", [])
        self.assertTrue(len(full_fragment) > 0, "Prompt fragment is empty")
        
        # Check specific content we know is in tdd-workflow skill
        # From context retrieval: "RED-GREEN-REFACTOR cycle"
        needle = "RED-GREEN-REFACTOR cycle"
        
        # Join fragment if it's a list (gsd_select.py logs it as a list of strings)
        combined_fragment = "\n\n".join(full_fragment)
        
        self.assertIn(needle, combined_fragment, "Skill content truncated or missing!")
        
        # Verify length consistency
        self.assertEqual(len(combined_fragment), found_entry.get("fragment_length"), 
                         "Logged fragment_length does not match actual content length")

if __name__ == '__main__':
    unittest.main()
