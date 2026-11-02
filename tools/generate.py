"""Regenerate the dataset CSV, the FAQ docs page and README tables from the JSON sources.

    python tools/generate.py           write generated files
    python tools/generate.py --check   exit 1 if any generated file is stale
"""

import csv
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "fxfunds_risk_disclosures"

MODEL = json.loads((PKG / "model.json").read_text(encoding="utf-8"))
RISK_FAQ = json.loads((PKG / "risk_faq.json").read_text(encoding="utf-8"))
CSV_FIELDS = ["risk_id", "risk_category", "keywords", "risk_answer", "example", "question", "answer"]


def csv_text(fields, rows):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: r[k] for k in fields})
    return buf.getvalue()


def assets_table():
    lines = ["| Asset (`--asset`) | Name | Typical daily move |", "|-------------------|------|--------------------|"]
    for k, v in MODEL["assets"].items():
        lines.append(f"| `{k}` | {v['name']} | {v['daily_vol']}% |")
    return "\n".join(lines)


def database_rows():
    """One row per related FAQ; a category with no FAQ gets one row with blank question and answer."""
    rows = []
    for r in RISK_FAQ:
        base = {"risk_id": r["id"], "risk_category": r["name"], "keywords": "; ".join(r["keywords"]),
                "risk_answer": r["answer"], "example": r["example"]}
        for q in r["faq"] or [{"question": "", "answer": ""}]:
            rows.append({**base, "question": q["question"], "answer": q["answer"]})
    return rows


def risks_table():
    lines = ["| Risk category | Keywords | Answer |", "|---------------|----------|--------|"]
    for r in RISK_FAQ:
        lines.append(f"| {r['name']} | {', '.join(r['keywords'])} | {r['answer']} |")
    return "\n".join(lines)


def faq_markdown(level="###"):
    out = []
    for r in RISK_FAQ:
        if not r["faq"]:
            continue
        out.append(f"{level} {r['name']}\n")
        for q in r["faq"]:
            out.append(f"**{q['question']}**\n")
            out.append(f"{q['answer']}\n")
    return "\n".join(out).rstrip()


def replace_block(text, name, body):
    pattern = re.compile(rf"(<!-- {name}:START -->\n).*?(<!-- {name}:END -->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"marker {name} not found")
    return pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)


def readme():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    text = replace_block(text, "ASSETS", assets_table())
    text = replace_block(text, "RISKS", risks_table())
    text = replace_block(text, "FAQ", faq_markdown("###"))
    return text


def outputs():
    return {
        ROOT / "dataset/fxfunds_risk_faq.csv": csv_text(CSV_FIELDS, database_rows()),
        ROOT / "docs/faq.md": f"# Risk FAQ\n\nFAQs grouped by risk category.\n\n{faq_markdown('##')}\n",
        ROOT / "README.md": readme(),
    }


def main():
    check = "--check" in sys.argv
    stale = []
    for path, content in outputs().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            stale.append(path.relative_to(ROOT))
            if not check:
                path.write_text(content, encoding="utf-8")
    if check and stale:
        print("Stale generated files:", *stale, sep="\n  ")
        return 1
    print("Up to date." if not stale else f"Wrote {len(stale)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
