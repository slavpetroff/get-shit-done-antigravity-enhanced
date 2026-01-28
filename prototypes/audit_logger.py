import fcntl
import json
import os
import contextlib

class SafeAuditLogger:
    def __init__(self, log_path):
        self.log_path = log_path

    def log_event(self, event_data):
        """
        Safely append a JSON event to the log file using fcntl locking.
        """
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

        with open(self.log_path, 'a') as f:
            try:
                # Acquire an exclusive lock (blocking)
                fcntl.flock(f, fcntl.LOCK_EX)
                
                # Write the JSON line
                json_line = json.dumps(event_data) + "\n"
                f.write(json_line)
                
                # Flush buffers to ensure data hits OS buffers
                f.flush()
                os.fsync(f.fileno())
                
            finally:
                # Release the lock
                fcntl.flock(f, fcntl.LOCK_UN)

if __name__ == "__main__":
    # verification
    logger = SafeAuditLogger(".gsd/logs/prototype_audit.jsonl")
    logger.log_event({"event": "test_init", "status": "ok"})
    print("Log entry written safely.")
