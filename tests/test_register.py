"""Consistency and behaviour tests for FXFunds Risk Disclosures.
fxfunds_risk_disclosures/register.json and risks.json are the single sources; everything else must match them."""
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import fxfunds_risk_disclosures as rd

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "fxfunds_risk_disclosures"
REGISTER = json.loads((PKG / "register.json").read_text(encoding="utf-8"))
RISKS = json.loads((PKG / "risks.json").read_text(encoding="utf-8"))["risks"]
DOCS = REGISTER["documents"]
IDS = {d["id"] for d in DOCS}
ICON = {"located": "✅ Located", "not-located": "❓ Not located", "inaccessible": "🚫 Inaccessible", "outdated": "🕓 Outdated"}


def read_csv(name):
    with open(ROOT / "dataset" / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_register_structure():
    assert len(DOCS) == len(IDS) == 16
    for d in DOCS:
        assert d["status"] in REGISTER["status_values"], d["id"]
        assert d["document"] and d["should_cover"] and d["last_checked"], d["id"]
        if d["status"] == "located":
            assert d["official_url"] and d["official_url"].startswith("https://"), d["id"]
        if d["status"] == "not-located":
            assert d["official_url"] is None, d["id"]


def test_risks_structure():
    ids = [r["id"] for r in RISKS]
    assert len(ids) == len(set(ids)) == 8
    names = {d["id"]: d["document"] for d in DOCS}
    for r in RISKS:
        assert r["register_ids"] and set(r["register_ids"]) <= IDS, r["id"]
        assert r["what_to_check"] == "; ".join(names[i] for i in r["register_ids"]), r["id"]


def test_register_csv_matches_json():
    rows = read_csv("fxfunds_document_register.csv")
    assert len(rows) == len(DOCS)
    for row, d in zip(rows, DOCS):
        for key in ("id", "category", "document", "should_cover", "status", "last_checked", "notes"):
            assert row[key] == d[key], (d["id"], key)
        assert row["official_url"] == (d["official_url"] or "")
        assert row["status_label"] == ICON[d["status"]]


def test_risks_csv_matches_json():
    rows = read_csv("fxfunds_risk_categories.csv")
    assert [r["id"] for r in rows] == [r["id"] for r in RISKS]
    for row, r in zip(rows, RISKS):
        assert row["register_ids"] == ";".join(r["register_ids"])
        assert row["what_to_check"] == r["what_to_check"]


def test_register_page_lists_every_entry():
    page = (ROOT / "docs" / "document-register.md").read_text(encoding="utf-8")
    for d in DOCS:
        row = f"| {d['id']} | {d['document']} | {d['should_cover']} | {ICON[d['status']]} | {d['official_url'] or '—'} | {d['last_checked']} |"
        assert row in page, d["id"]


def test_readme_and_docs_show_every_risk():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    page = (ROOT / "docs" / "risk-categories.md").read_text(encoding="utf-8")
    for r in RISKS:
        row = f"| {r['name']} | {r['consideration']} | {r['example']} | {r['what_to_check']} |"
        assert row in readme and row in page, r["id"]


def test_python_api():
    s = rd.summary()
    assert s["total"] == 16 and s["located"] == 1 and s["not-located"] == 15
    assert rd.get("reg-02")["document"] == "Risk disclosure / risk warning"
    assert rd.get("REG-99") is None
    assert len(rd.missing()) == 15
    assert [d["id"] for d in rd.by_category("legal")] == ["REG-10", "REG-11", "REG-12", "REG-13", "REG-14"]
    assert rd.categories() == ["General", "Trading", "Payments", "Crypto", "Legal", "Privacy"]
    assert [d["id"] for d in rd.documents_for_risk("leverage")] == ["REG-04", "REG-02"]
    assert rd.documents_for_risk("nope") == []
    assert "Status: not-located" in rd.format_document(rd.get("REG-02"))


def test_python_cli():
    out = subprocess.run([sys.executable, "-m", "fxfunds_risk_disclosures", "risk", "leverage", "--json"],
                         capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    assert data["id"] == "leverage" and [d["id"] for d in data["documents"]] == ["REG-04", "REG-02"]


@pytest.mark.skipif(shutil.which("node") is None or not (ROOT / "index.js").exists(),
                    reason="Build the Node.js package first: npm ci && npm run build")
def test_node_matches_python():
    script = ("const f=require('./index.js');"
              "console.log(JSON.stringify({summary:f.summary(),missing:f.missing().map(d=>d.id),"
              "cats:f.categories(),legal:f.byCategory('legal').map(d=>d.id),"
              "risks:f.risks().map(r=>[r.id,f.documentsForRisk(r.id).map(d=>d.id)]),"
              "fmt:f.format(f.get('REG-01'))}))")
    node = json.loads(subprocess.run(["node", "-e", script], cwd=ROOT, capture_output=True, text=True,
                                     check=True).stdout)
    assert node["summary"] == rd.summary()
    assert node["missing"] == [d["id"] for d in rd.missing()]
    assert node["cats"] == rd.categories()
    assert node["legal"] == [d["id"] for d in rd.by_category("legal")]
    assert node["risks"] == [[r["id"], [d["id"] for d in rd.documents_for_risk(r["id"])]] for r in rd.risks()]
    assert node["fmt"] == rd.format_document(rd.get("REG-01"))
