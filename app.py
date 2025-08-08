# app.py
import streamlit as st
import os
from utils.extractor import extract_text_from_file
from utils.ner import extract_entities
from utils.rules import load_rules, run_pii_checks, run_keyword_checks
from utils.report import save_json_report, save_html_report
from agent.llm_agent import llm_summarize_with_openai, llm_summarize_with_local, OPENAI_AVAILABLE
from datetime import datetime

st.set_page_config(page_title="DocuGuard AI — Compliance Checker", layout="wide")
st.title("🛡️ DocuGuard AI — Document Compliance Checker")

st.sidebar.header("Options")
use_llm = st.sidebar.checkbox("Use LLM for summary/suggestions (optional)", value=False)
openai_key = st.sidebar.text_input("OpenAI API Key (if using OpenAI)", type="password")
local_llm_cmd = st.sidebar.text_input("Local LLM command (e.g. ollama run model)", value="")  # if using local

uploaded = st.file_uploader("Upload document (PDF, DOCX, TXT)", type=["pdf","docx","txt"])
if uploaded:
    st.info("Extracting text...")
    text, ftype = extract_text_from_file(uploaded)
    st.success(f"Extracted text from {ftype}")

    st.subheader("Preview (first 4000 chars)")
    st.text_area("Document Text", value=text[:4000], height=250)

    # Load rules
    rules = load_rules("rules/rules.json")

    # NER
    st.info("Running Named Entity Recognition...")
    entities = extract_entities(text)

    # Rule checks
    st.info("Running rule-based checks...")
    pii_findings = run_pii_checks(text, rules)
    keyword_findings = run_keyword_checks(text, rules)
    findings = pii_findings + keyword_findings

    st.subheader("Entities")
    st.json(entities)

    st.subheader("Findings")
    st.write(f"{len(findings)} findings detected")
    for f in findings[:200]:
        st.write(f)

    # LLM summary (optional)
    llm_summary = None
    if use_llm:
        st.info("Running LLM summary (may take a while)...")
        try:
            if openai_key:
                if not OPENAI_AVAILABLE:
                    st.error("OpenAI library not installed. Add it to requirements to use OpenAI.")
                else:
                    llm_summary = llm_summarize_with_openai(text, openai_key)
            elif local_llm_cmd.strip():
                cmd_list = local_llm_cmd.strip().split()
                llm_summary = llm_summarize_with_local(cmd_list, text)
            else:
                st.warning("LLM option selected but no API key or local command provided.")
        except Exception as e:
            st.error(f"LLM call failed: {e}")

    # Compile report
    report = {
        "file_name": getattr(uploaded, "name", "uploaded"),
        "timestamp": datetime.utcnow().isoformat(),
        "entities": entities,
        "findings": findings,
        "llm_summary": llm_summary
    }

    # Save and show
    save_json_report(report, out_path=f"output/report_{int(datetime.utcnow().timestamp())}.json")
    html_path = save_html_report(report, file_name=f"output/report_{int(datetime.utcnow().timestamp())}.html")

    st.success("Report created")
    st.markdown(f"- [Download JSON report](/{html_path}) — right-click and save (or find it in `output/`)")
    st.markdown(f"- HTML report saved to `{html_path}` in the repo.")
