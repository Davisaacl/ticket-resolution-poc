"""
Ticket State - Manages the state and lifecycle of a support ticket
"""
from datetime import datetime
from enum import Enum

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    ESCALATED = "escalated"

class TicketState:
    def __init__(self, ticket_data):
        self.ticket_id = ticket_data["id"]
        self.data = ticket_data
        self.status = TicketStatus.OPEN
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.knowledge = {}
        self.actions_taken = []
        self.resolution = None
    
    def add_knowledge(self, knowledge):
        """Add knowledge gathered about the ticket"""
        self.knowledge.update(knowledge)
        self.updated_at = datetime.now()
    
    def add_action(self, action):
        """Record an action taken on the ticket"""
        self.actions_taken.append({
            "action": action,
            "timestamp": datetime.now()
        })
        self.updated_at = datetime.now()
    
    def set_status(self, status):
        """Update ticket status"""
        self.status = status
        self.updated_at = datetime.now()
    
    def set_resolved(self, resolution):
        """Mark ticket as resolved with solution"""
        self.resolution = resolution
        self.status = TicketStatus.RESOLVED
        self.updated_at = datetime.now()
    
    def set_escalated(self):
        """Mark ticket as escalated"""
        self.status = TicketStatus.ESCALATED
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert ticket state to dictionary for serialization"""
        return {
            "ticket_id": self.ticket_id,
            "data": self.data,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "knowledge": self.knowledge,
            "actions_taken": self.actions_taken,
            "resolution": self.resolution
        }