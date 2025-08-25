# -*- coding: utf-8 -*-
"""Generative AI helpers using OpenAI API (optional).
If OPENAI_API_KEY is not configured or library is missing, functions return a message.
"""
from __future__ import annotations
import os
from typing import List, Dict


def _client():
    """Return OpenAI client if possible, else None."""
    if not os.getenv("OPENAI_API_KEY"):
        return None
    try:
        from openai import OpenAI
        return OpenAI()
    except Exception:
        return None


def chat_completion(messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo") -> str:
    """Simple chat completion wrapper."""
    client = _client()
    if client is None:
        return "[OpenAI未設定] OPENAI_API_KEY を設定してください。"
    try:
        res = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        return f"[OpenAIエラー] {e}"


def generate_answer(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Generate answer text from a prompt."""
    return chat_completion([{"role": "user", "content": prompt}], model=model)
