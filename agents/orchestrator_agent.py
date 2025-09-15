"""
Orchestrator Agent - Central brain and project manager for ticket resolution
"""
from utils.ticket_state import TicketState
from memory.ticket_memory import TicketMemory
from agents.knowledge_agent import KnowledgeAgent
from agents.resolver_agent import ResolverAgent
from agents.communication_agent import CommunicationAgent
from agents.escalator_agent import EscalatorAgent
from utils.llm import gen_plan
from utils.metrics import Timer, count

class OrchestratorAgent:
    def __init__(self):
        self.knowledge_agent = KnowledgeAgent()
        self.resolver_agent = ResolverAgent()
        self.communication_agent = CommunicationAgent()
        self.escalator_agent = EscalatorAgent()
        self.memory = TicketMemory()
    
    def process_ticket(self, ticket_data):
        with Timer("ticket_total_seconds"):            # NEW
            count("tickets_started", 1)                # NEW

            print(f"🧠 Orchestrator: Starting analysis of ticket {ticket_data['id']}")
            ticket_state = TicketState(ticket_data)
            self.memory.save_ticket_state(ticket_state)

            # Step 1: Plan
            with Timer("plan_seconds"):                # NEW (optional granular metric)
                strategy = self._develop_strategy(ticket_data)
            print(f"📋 Strategy: {strategy}")
            ticket_state.planning_log = strategy

            # Step 2: Knowledge
            print("🔍 Gathering knowledge...")
            with Timer("knowledge_seconds"):           # NEW (optional)
                knowledge = self.knowledge_agent.search_knowledge(ticket_data)
            ticket_state.add_knowledge(knowledge)

            # Step 3: Resolution
            print("🔧 Attempting resolution...")
            with Timer("resolution_seconds"):          # NEW (optional)
                resolution_result = self.resolver_agent.attempt_resolution(ticket_data, knowledge)

            actions = resolution_result.get("actions") or resolution_result.get("actions_taken") or []
            if actions:
                try:
                    for a in actions: ticket_state.add_action(a)  # if available
                except AttributeError:
                    ticket_state.actions_taken = actions

            if resolution_result.get('success'):
                # Step 4: Communication
                with Timer("communication_seconds"):   # NEW (optional)
                    self.communication_agent.send_resolution(ticket_data, resolution_result)
                ticket_state.set_resolved(resolution_result['resolution'])

                # Outcome counters
                count("tickets_resolved", 1)           # NEW
                # (persistence call stays as you have it)
                return {
                    'status': 'resolved',
                    'resolution': resolution_result['resolution']
                }
            else:
                print("⚠️ Resolution failed, escalating...")
                with Timer("escalation_seconds"):      # NEW (optional)
                    escalation_summary = self.escalator_agent.escalate_ticket(ticket_state)

                count("tickets_escalated", 1)          # NEW
                return {
                    'status': 'escalated',
                    'escalation_summary': escalation_summary
                }

    
    def _develop_strategy(self, ticket_data):
        """Develop high-level strategy based on ticket analysis"""
        return gen_plan(ticket_data)  # NEW (replaces the hardcoded string)
