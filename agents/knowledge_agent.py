"""
Knowledge Agent - Manages information retrieval tasks (semantic search)
"""
from typing import List
from knowledge.vector_store import VectorStore  # make sure knowledge/vector_store.py exists
from config import settings


class KnowledgeAgent:
    def __init__(self):
        self.vs = VectorStore(                           # CHANGED
            path=settings.KB_INDEX_PATH,
            meta_path=settings.KB_META_PATH
        )
        if not getattr(self.vs, "meta", None):
            seed_docs = [
                "Runbook: Database timeouts — restart connection pool, check network, verify max_connections.",
                "Checklist: API 504 triage — DB latency, connection pooling, slow queries, timeouts.",
                "Guide: Escalate DB incidents to SRE with logs, metrics, and query plans.",
                "Playbook: Connection pool saturation — identify leak, tune pool size, recycle idle connections.",
                "How-To: Collect DB logs and slow query log for incident analysis.",
            ]
            self.vs.build(seed_docs)

    def search_knowledge(self, ticket_data):
        title = ticket_data.get("title", "")
        desc = ticket_data.get("description", "")
        print(f"📚 Knowledge Agent: Searching for information about '{title}'")
        query = f"{title} {desc}".strip()
        hits = self.vs.search(query, k=5)
        relevant_docs = [doc for doc, _ in hits]
        print(f"✅ Found {len(relevant_docs)} relevant documents")
        return {
            "relevant_docs": relevant_docs,
            "similar_tickets": [
                "TICKET-998: Database timeout resolved by restarting connection pool"
            ],
            "suggested_actions": [
                "Check database server status",
                "Verify network connectivity",
                "Review connection pool settings",
            ],
        }