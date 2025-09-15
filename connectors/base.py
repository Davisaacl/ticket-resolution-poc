from typing import Dict, Any, List

class ActionAdapter:
    """Abstract base adapter. Implement safe no-op defaults for the PoC."""
    def diagnose(self, context: Dict[str, Any]) -> List[str]:
        return ["Diagnose: no-op (demo)"]

    def remediate(self, context: Dict[str, Any]) -> List[str]:
        return ["Remediate: no-op (demo)"]
