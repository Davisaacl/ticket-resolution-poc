# Enterprise Support Ticket Resolution PoC

Authors: David López & Juan Cocco

A minimal proof-of-concept for an autonomous enterprise support ticket resolution system using multi-agent architecture with LangChain and Gemini API.

## Overview

This system uses a team of specialized AI agents to automatically resolve enterprise support tickets with human escalation as a fallback. The system is designed to handle the complete ticket lifecycle from initial analysis to resolution or escalation.

## Architecture

### Agent Roles

- **Orchestrator Agent**: Central coordinator that manages the ticket lifecycle and delegates tasks to specialist agents
- **Knowledge Agent**: Retrieves relevant information from documentation, past tickets, and knowledge bases  
- **Resolver Agent**: Executes technical tasks and system interactions to resolve issues
- **Communication Agent**: Manages all customer communications and status updates
- **Escalator Agent**: Handles formal escalation to human agents with comprehensive summaries

### Project Structure

```
ticket_poc/
├── main.py                     # Entry point (processes one or many tickets from JSON)
├── tickets.json                # Example tickets input
├── config.py                   # Centralized settings (env vars, models, paths)
├── requirements.txt            # Python dependencies
├── agents/
│   ├── orchestrator_agent.py   # Central coordinator
│   ├── knowledge_agent.py      # Semantic knowledge retrieval
│   ├── resolver_agent.py       # Executes resolution via connectors
│   ├── communication_agent.py  # Customer updates
│   └── escalator_agent.py      # Escalation path
├── connectors/
│   ├── base.py                 # Base connector adapter
│   └── postgres.py             # Example Postgres connector (simulated)
├── knowledge/
│   └── vector_store.py         # FAISS + SentenceTransformers index
├── memory/
│   └── ticket_memory.py        # In-memory ticket storage
└── utils/
    ├── ticket_state.py         # Ticket state management
    ├── llm.py                  # Gemini API wrapper
    └── metrics.py              # Lightweight metrics & timers
```

## Setup

### Prerequisites

- Python 3.8+
- pip (or pipenv/uv)
- Gemini API key

### Installation

1. **Install dependencies with Pipenv:**
   ```bash
   pipenv install
   pipenv shell
   ```

   **Or with pip:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Copy `.env.template` to `.env` and set your values:
   ```
   cp .env.template .env
   ```
   Example:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-1.5-pro
   EMBED_MODEL=all-MiniLM-L6-v2
   KB_INDEX_PATH=kb.index
   KB_META_PATH=kb_meta.json
   ENV=dev
   LOG_LEVEL=INFO
   ```

### Running the PoC

```bash
python main.py
```

## Current Implementation

This is a **minimal PoC** with the following characteristics:

- ✅ **Gemini integration** for strategy/plan generation
- ✅ **FAISS vector database** for semantic knowledge search
- ✅ **System connectors** (Postgres adapter simulated)
- ✅ **Configuration management** via config.py + .env
- ✅ **Lightweight metrics** (timers + counters in JSON)
- ✅ **Multi-ticket** input via tickets.json

## Ticket Lifecycle

1. **Initial Analysis:** Orchestrator receives and analyzes the ticket
2. **Strategy Development:** Plan generated with Gemini
3. **Knowledge Gathering:** Knowledge Agent performs semantic search with FAISS
4. **Resolution Attempt:** Resolver executes technical tasks (via connectors)
5. **Communication:** Customer is notified of resolution or status
6. **Escalation:** If resolution fails, ticket is escalated with context

## Example Output

```
🎫 Starting Ticket Resolution PoC
🗂️  Loaded 3 tickets from tickets.json

Processing ticket: TICKET-001 - Database connection issues
🧠 Orchestrator: Starting analysis of ticket TICKET-001
📋 Strategy: (Gemini-generated plan)
🔍 Gathering knowledge...
📚 Knowledge Agent: Searching for information about 'Database connection issues'
✅ Found 5 relevant documents
🔧 Resolver Agent: Attempting resolution for 'Database connection issues'
  → Pinged Postgres (simulated)
  → Checked connection pool metrics (simulated)
  → Restarted connection pool (simulated)
📧 Communication Agent: Notifying customer about resolution
  → Email sent to user@company.com
💾 Ticket snapshot persisted (resolved).

✅ Ticket TICKET-001 completed with status: resolved
Resolution: Database connection pool restarted successfully. Connection timeouts resolved.

{"metric": "ticket_total_seconds", "seconds": 0.8421}
{"metric": "tickets_started", "count": 1}
{"metric": "tickets_resolved", "count": 1}
```

## Integration Points for Full Implementation

(✔️ = implemented in the PoC, 🔜 = future work for production)

- ✔️ **LLM Integration (Gemini):** Strategy generation via Gemini (utils/llm.py), with fallback when API key is not set.
- ✔️ **Knowledge Base (Vector Search):** FAISS + SentenceTransformers for semantic retrieval (knowledge/vector_store.py).
- ✔️ **System Connectors (Simulated):** Example Postgres connector in connectors/postgres.py used by the ResolverAgent.
- ✔️ **Configuration Management:** Centralized in config.py + .env for models, paths, and environment flags.
- ✔️ **Metrics & Monitoring (Lightweight):** Timing and counters in JSON (utils/metrics.py).
- 🔜 **Real System Connectors:** Integrate with real systems (databases, Kubernetes, monitoring tools, etc.) with safe guards.
- 🔜 **Communication Channels:** Real email (SMTP), Slack, ServiceNow/Jira via API or webhooks.
- 🔜 **Persistent Storage:** Replace in-memory state with a database (e.g., SQLite, Postgres, Redis).
- 🔜 **Security & Auth:** Proper secrets management and authentication/authorization per environment.
- 🔜 **Robust Error Handling:** Retries, circuit breakers, timeouts, and full observability.
- 🔜 **API/Service Mode:** Expose as a FastAPI service (POST /tickets) with health checks.

## Key Features

- **Autonomous Resolution (PoC):** Orchestrator + Gemini generate a plan and execute safe actions; escalation if resolution fails.
- **Intelligent Escalation:** Provides rich context and summaries to human agents through the EscalatorAgent.
- **Semantic Knowledge Retrieval:** FAISS + embeddings find relevant runbooks and checklists.
- **Modular Multi-Agent Design:** Orchestrator, Knowledge, Resolver (with connectors), Communication, Escalator.
- **Configurable per Environment:** config.py + .env for model selection, file paths, and toggles.
- **Lightweight Metrics:** Step timings and counters emitted as JSON for easy inspection.
- **Multi-ticket Input:** Load and process multiple tickets from tickets.json for batch demos.

## Next Steps

1. Expand connectors (monitoring, logging, infra APIs)
2. Add real communication channels (SMTP, Slack, ServiceNow, etc.)
3. Persist tickets to a real database
4. Strengthen security & authentication
5. Integrate with monitoring (Prometheus, OpenTelemetry)
