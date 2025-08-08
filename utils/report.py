# utils/report.py
import json
import os
from jinja2 import Template

REPORT_HTML_TEMPLATE = """
<html>
<head><meta charset="utf-8"><title>DocuGuard Report</title></head>
<body>
  <h1>DocuGuard AI — Compliance Report</h1>
  <h2>File: {{ file_name }}</h2>
  <h3>Summary</h3>
  <pre>{{ summary }}</pre>
  <h3>Entities</h3>
  <ul>
  {% for label, items in entities.items() %}
    <li><b>{{ label }}</b>: {{ items|join(', ') }}</li>
  {% endfor %}
  </ul>
  <h3>Findings</h3>
  <ul>
  {% for f in findings %}
    <li>{{ f }}</li>
  {% endfor %}
  </ul>
</body>
</html>
"""

def save_json_report(report: dict, out_path="output/report.json"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

def save_html_report(report: dict, file_name="output/report.html"):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    tpl = Template(REPORT_HTML_TEMPLATE)
    html = tpl.render(
        file_name=report.get("file_name","(uploaded)"),
        summary=report.get("llm_summary","(none)"),
        entities=report.get("entities",{}),
        findings=[json.dumps(f) for f in report.get("findings",[])]
    )
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html)
    return file_name
