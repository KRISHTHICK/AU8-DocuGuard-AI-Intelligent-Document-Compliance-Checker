# AU8-DocuGuard-AI-Intelligent-Document-Compliance-Checker
Ai Agent

AI Agent Topic:
"DocuGuard AI – Intelligent Document Compliance Checker"

Overview
DocuGuard AI is an AI-powered compliance agent that scans documents (PDF, Word, TXT) for policy violations, sensitive data leaks, or legal non-compliance issues. It can automatically highlight risky sections, generate compliance reports, and suggest fixes — all in natural language.

Key Features
Multi-format Support → PDF, DOCX, TXT.

Compliance Rule Database → Preloaded rules for GDPR, HIPAA, or custom company policies.

NER & Pattern Matching → Detects names, emails, IDs, phone numbers, and sensitive terms.

LLM-Powered Suggestions → Uses an LLM (Ollama or local LLaMA) to recommend edits.

Interactive Dashboard → Streamlit UI with compliance score, risk heatmap, and fixes.

Export Reports → PDF/JSON with compliance details.

Tech Stack
Frontend/UI: Streamlit

Backend/Processing: Python (FastAPI optional)

AI Models: Local LLM (Ollama/TinyLLaMA) + SpaCy for NER

File Handling: PyMuPDF, docx2txt, Pandas

Deployment: GitHub + local execution in VS Code

Workflow
Upload Document → User uploads PDF/DOCX/TXT.

Preprocessing → Extract text using PyMuPDF/docx2txt.

Entity & Rule Check → Use SpaCy + regex to find sensitive data.

LLM Analysis → Pass extracted content & violations to LLM for compliance suggestions.

Report Generation → Create downloadable compliance report in PDF/JSON.

User Interaction → Show flagged content & recommendations in Streamlit.

Possible Use Cases
HR Teams → Scan employee contracts for legal compliance.

Healthcare → Ensure medical reports comply with HIPAA.

Finance → Detect sensitive financial information leaks.

Corporate Policy → Check documents against internal policies.

If you want, I can create the full working code for DocuGuard AI with

Streamlit UI

Local LLM integration

Entity & compliance detection

Downloadable compliance report

so you can run it directly in VS Code and push to GitHub.

Do you want me to go ahead with that build?







You said:
Yes full code


ChatGPT said:
Awesome — I’ll give you a complete, runnable project called DocuGuard AI: a Streamlit app + agent that scans uploaded documents (PDF/DOCX/TXT), performs NER and rule-based checks (PII, IDs, emails, phone numbers, policy keywords), runs optional LLM analysis for remediation suggestions, and produces a downloadable compliance report (JSON + simple HTML/PDF report option).

Below you’ll find:

Project structure

requirements.txt

Every source file (complete code) you can drop into your repo

Example rules.json

How to run (including spaCy model install)

Notes about LLM options (OpenAI or local) and safety

requirements.txt
nginx
Copy
Edit
streamlit
python-docx
PyMuPDF
spacy
pandas
pdfkit
Jinja2
python-dotenv
requests
Optional (LLM):

For OpenAI: openai

For local/ollama usage you may run subprocess calls — no extra pip package required here.
If you want OpenAI in the agent, add openai to requirements.
