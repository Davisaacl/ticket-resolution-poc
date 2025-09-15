from .base import ActionAdapter
from typing import Dict, Any, List

class PostgresAdapter(ActionAdapter):
    def diagnose(self, context: Dict[str, Any]) -> List[str]:
        return [
            "Pinged Postgres (simulated)",
            "Checked connection pool metrics (simulated)"
        ]

    def remediate(self, context: Dict[str, Any]) -> List[str]:
        return ["Restarted connection pool (simulated)"]
