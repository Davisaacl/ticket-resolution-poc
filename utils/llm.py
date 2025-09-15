# utils/llm.py
import os
import google.generativeai as genai
from config import settings

api_key = settings.GEMINI_API_KEY
model = settings.GEMINI_MODEL

DEBUG = os.getenv("LLM_DEBUG", "0") == "1"

def _dbg(msg: str):
    if DEBUG:
        print(f"[LLM] {msg}")

def get_gemini():
    api_key = settings.GEMINI_API_KEY          # CHANGED
    if not api_key:
        _dbg("No GEMINI_API_KEY; using fallback.")
        return None
    genai.configure(api_key=api_key)
    model = settings.GEMINI_MODEL              # CHANGED
    _dbg(f"Configured model: {model}")
    return genai.GenerativeModel(model)

def gen_plan(ticket: dict) -> str:
    m = get_gemini()
    if not m:
        # Fallback matches your current behavior
        return f"Analyze {ticket['title']} and gather relevant documentation"
    prompt = f"""You are an orchestrator for enterprise ticket resolution.

Ticket:
id: {ticket['id']}
title: {ticket['title']}
description: {ticket['description']}
priority: {ticket.get('priority','medium')}

Return a concise plan with:
- 3–7 numbered action steps
- information to retrieve (docs, logs, metrics)
- safe automated actions (idempotent)
- success criteria (verifiable)
- escalation triggers (clear)
"""
    try:
        resp = m.generate_content(prompt)
        text = getattr(resp, "text", None)
        return (text or "").strip() or f"Analyze {ticket['title']} and gather relevant documentation"
    except Exception:
        # Never break the PoC
        return f"Analyze {ticket['title']} and gather relevant documentation"
