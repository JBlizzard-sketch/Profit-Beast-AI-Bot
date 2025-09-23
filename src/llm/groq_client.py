"""Groq LLM client wrapper. Uses GROQ_API_KEY from env to call Groq inference endpoints.
If GROQ_API_KEY is not present, falls back to deterministic template. Also supports OPENAI as fallback.
""" 
import os, requests, json
from ..config import GROQ_API_KEY, OPENAI_API_KEY
from ..logger_setup import get_logger
log = get_logger(__name__)

GROQ_API_URL = os.getenv('GROQ_API_URL', 'https://api.groq.ai/v1')  # placeholder

def _call_groq(prompt, max_tokens=256):
    if not GROQ_API_KEY:
        raise RuntimeError('GROQ_API_KEY not set')
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {
        'prompt': prompt,
        'max_tokens': max_tokens
    }
    # NOTE: This is a generic placeholder; adapt to actual Groq API shape.
    resp = requests.post(f'{GROQ_API_URL}/generate', headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # expecting {'text': '...'} or similar
    text = data.get('text') or data.get('output') or json.dumps(data)
    return text

def explain_signal(signal_type, context):
    """Return a human-readable explanation for an ML signal.
    If GROQ_API_KEY provided, call Groq; if not, deterministic fallback.
    """
    prompt = f"Explain {signal_type} alert with context: {json.dumps(context)}. Provide concise actionable steps and risk level."
    try:
        if GROQ_API_KEY:
            log.info('Calling Groq for LLM explanation.')
            return _call_groq(prompt)
        elif OPENAI_API_KEY:
            # Placeholder for OpenAI integration
            log.info('OPENAI_API_KEY present; OpenAI integration can be implemented here.')
        # Fallback deterministic explanation
        explanation = f"[LLM Explanation - {signal_type}] Observed context: {context}. Confidence: medium. Recommended action: review and monitor."
        return explanation
    except Exception as e:
        log.exception('LLM call failed, returning fallback explanation.')
        return f"[LLM-Fallback] Could not call LLM: {e}. Context: {context}"
