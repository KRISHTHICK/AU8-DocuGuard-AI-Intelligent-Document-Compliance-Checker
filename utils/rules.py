#Load JSON rules and run regex checks.
# utils/rules.py
import json
import re
from typing import Dict, List, Any

def load_rules(path="rules/rules.json") -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_pii_checks(text: str, rules: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings = []
    patterns = rules.get("pii_patterns", {})
    for name, pattern in patterns.items():
        for m in re.finditer(pattern, text):
            findings.append({
                "type": "pii",
                "category": name,
                "match": m.group(0),
                "start": m.start(),
                "end": m.end()
            })
    return findings

def run_keyword_checks(text: str, rules: Dict[str, Any]) -> List[Dict[str, Any]]:
    findings = []
    keywords = rules.get("policy_keywords", []) + rules.get("suspicious_terms", [])
    lower = text.lower()
    for kw in keywords:
        if kw.lower() in lower:
            findings.append({
                "type": "keyword",
                "keyword": kw,
                "count": lower.count(kw.lower())
            })
    return findings
