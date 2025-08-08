# Optional LLM wrapper — supports OpenAI or a local command (ollama or other) via subprocess.

# Important: Using LLMs requires keys or local runtime. This file provides optional functions — if you don't have a key/local tool you can still run the rest.

# agent/llm_agent.py
import os
import subprocess
import json

# Optional OpenAI use
try:
    import openai
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False

def llm_summarize_with_openai(text: str, openai_api_key: str, model="gpt-3.5-turbo") -> str:
    if not OPENAI_AVAILABLE:
        raise RuntimeError("openai package not installed")
    openai.api_key = openai_api_key
    prompt = f"Read the document below and provide a short compliance summary (3-5 sentences) and a prioritized list of remediation steps:\n\n{text[:4000]}"
    resp = openai.ChatCompletion.create(
        model=model,
        messages=[{"role":"user", "content": prompt}],
        temperature=0.2,
        max_tokens=500
    )
    return resp["choices"][0]["message"]["content"]

def llm_summarize_with_local(model_cmd: list, text: str) -> str:
    """
    model_cmd: list of command strings to call local LLM, e.g. ['ollama','run','llama2']
    The function will pass the prompt to stdin.
    """
    prompt = f"Summarize compliance issues and suggest fixes for this document:\n\n{text[:4000]}"
    proc = subprocess.run(model_cmd, input=prompt.encode("utf-8"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8"))
    return proc.stdout.decode("utf-8")
