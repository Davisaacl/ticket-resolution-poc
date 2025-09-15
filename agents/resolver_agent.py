"""
Resolver Agent - Executes technical tasks and system interactions
"""
from connectors.postgres import PostgresAdapter  # NEW

class ResolverAgent:
    def __init__(self):
        # Initialize adapters (simulated for PoC)
        self.pg = PostgresAdapter()

    def attempt_resolution(self, ticket_data, knowledge):
        """Attempt to resolve the ticket based on knowledge and available actions"""
        print(f"🔧 Resolver Agent: Attempting resolution for '{ticket_data['title']}'")

        actions_taken = []

        # If ticket looks like a DB issue → use Postgres adapter
        title = ticket_data.get("title", "").lower()
        desc = ticket_data.get("description", "").lower()
        if "database" in title or "db" in desc:
            diag = self.pg.diagnose({"ticket": ticket_data, "knowledge": knowledge})
            rem = self.pg.remediate({"ticket": ticket_data, "knowledge": knowledge})
            for action in diag + rem:
                print(f"  → {action}")
                actions_taken.append(action)

            return {
                "success": True,
                "resolution": "Database connection pool restarted successfully. Connection timeouts resolved.",
                "actions_taken": actions_taken,
            }

        # Default path: execute suggested actions (if any) and fail → escalate
        for action in knowledge.get("suggested_actions", []):
            print(f"  → Executing: {action}")
            actions_taken.append(action)

        return {
            "success": False,
            "reason": "Unable to identify root cause automatically",
            "actions_taken": actions_taken,
        }
