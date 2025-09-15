# utils/metrics.py
import time, json

class Timer:
    """Context manager to time a code block and print a JSON metric line."""
    def __init__(self, name: str):
        self.name = name
        self._t0 = None

    def __enter__(self):
        self._t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        dt = time.perf_counter() - self._t0
        print(json.dumps({"metric": self.name, "seconds": round(dt, 4)}))

def count(label: str, value: int = 1):
    """Emit a simple JSON counter metric."""
    print(json.dumps({"metric": label, "count": value}))
