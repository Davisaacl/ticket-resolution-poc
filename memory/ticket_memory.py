"""
Ticket Memory - Simple in-memory storage for ticket states
"""
from typing import Dict, Optional
from utils.ticket_state import TicketState

class TicketMemory:
    def __init__(self):
        self.tickets: Dict[str, TicketState] = {}
    
    def save_ticket_state(self, ticket_state: TicketState):
        """Save or update ticket state in memory"""
        self.tickets[ticket_state.ticket_id] = ticket_state
    
    def get_ticket_state(self, ticket_id: str) -> Optional[TicketState]:
        """Retrieve ticket state by ID"""
        return self.tickets.get(ticket_id)
    
    def list_tickets(self) -> Dict[str, TicketState]:
        """Get all tickets in memory"""
        return self.tickets.copy()
    
    def delete_ticket(self, ticket_id: str) -> bool:
        """Remove ticket from memory"""
        if ticket_id in self.tickets:
            del self.tickets[ticket_id]
            return True
        return False