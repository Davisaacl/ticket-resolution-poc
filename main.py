"""
Main entry point for the Enterprise Support Ticket Resolution PoC
"""
from dotenv import load_dotenv
load_dotenv()

import json
from pathlib import Path
from agents.orchestrator_agent import OrchestratorAgent

def main():
    print("🎫 Starting Ticket Resolution PoC")

    # Resolve tickets.json relative to THIS file, not the shell’s cwd
    here = Path(__file__).parent
    tickets_path = here / "tickets.json"

    if not tickets_path.exists():
        print(f"❌ Could not find {tickets_path}. Create it next to main.py.")
        print("   Example content:")
        print("""[
  {"id":"TICKET-001","title":"Database connection issues","description":"Users are unable...","priority":"high","customer_email":"user@company.com"},
  {"id":"TICKET-002","title":"API latency spike","description":"Requests >5s...","priority":"medium","customer_email":"api-team@company.com"}
]""")
        return

    try:
        tickets = json.loads(tickets_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"❌ Failed to read {tickets_path}: {e}")
        return

    if not isinstance(tickets, list) or not tickets:
        print(f"❌ {tickets_path} is empty or not a JSON array.")
        return

    orchestrator = OrchestratorAgent()
    print(f"🗂️  Loaded {len(tickets)} tickets from {tickets_path.name}")

    for t in tickets:
        print(f"\nProcessing ticket: {t.get('id')} - {t.get('title')}")
        result = orchestrator.process_ticket(t)
        print(f"✅ Ticket {t.get('id')} completed with status: {result['status']}")
        print(f"Resolution: {result.get('resolution', 'No resolution provided')}")

if __name__ == "__main__":
    main()
