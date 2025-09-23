import os
import pytest
from unittest import mock
from src.llm.groq_client import explain_signal
def test_explain_signal_fallback():
    # Ensure deterministic fallback when no GROQ_API_KEY is set
    os.environ.pop('GROQ_API_KEY', None)
    text = explain_signal('rug', {'a':1})
    assert 'LLM Explanation' in text or 'LLM-Fallback' in text
