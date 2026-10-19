"""
FXFunds Risk Disclosure Bot
Read the FXFunds official document register and risk categories: which official
documents have been located, which are missing, and which documents to check for
each type of risk. Works offline; no network calls.
Built by FXFunds — https://fxfunds.com/
"""

__version__ = "1.0.0"

import json
from importlib import resources
from typing import Dict, List, Optional

__all__ = ["REGISTER", "RISKS", "STATUS_VALUES", "LAST_CHECKED", "documents", "get", "by_status",
           "by_category", "categories", "missing", "summary", "risks", "risk", "documents_for_risk",
           "format_document"]


def _load(name: str) -> Dict:
    return json.loads(resources.files(__package__).joinpath(name).read_text(encoding="utf-8"))


REGISTER: Dict = _load("register.json")
RISKS: Dict = _load("risks.json")
STATUS_VALUES: Dict = REGISTER["status_values"]
LAST_CHECKED: str = REGISTER["last_checked"]


def documents() -> List[Dict]:
    """All register entries, in register order."""
    return list(REGISTER["documents"])


def get(doc_id: str) -> Optional[Dict]:
    """One register entry by ID, e.g. 'REG-02'. Case-insensitive."""
    return next((d for d in REGISTER["documents"] if d["id"].lower() == doc_id.lower()), None)


def by_status(status: str) -> List[Dict]:
    return [d for d in REGISTER["documents"] if d["status"] == status]


def by_category(category: str) -> List[Dict]:
    """Entries in one category (General, Trading, Payments, Crypto, Legal, Privacy). Case-insensitive."""
    return [d for d in REGISTER["documents"] if d["category"].lower() == category.lower()]


def categories() -> List[str]:
    """Register categories in order of first appearance."""
    seen: List[str] = []
    for d in REGISTER["documents"]:
        if d["category"] not in seen:
            seen.append(d["category"])
    return seen


def missing() -> List[Dict]:
    """Every entry that is not 'located'."""
    return [d for d in REGISTER["documents"] if d["status"] != "located"]


def summary() -> Dict:
    """Counts by status, plus total and last-checked date."""
    out = {"total": len(REGISTER["documents"]), "last_checked": LAST_CHECKED}
    for status in STATUS_VALUES:
        out[status] = len(by_status(status))
    return out


def risks() -> List[Dict]:
    """All risk categories."""
    return list(RISKS["risks"])


def risk(risk_id: str) -> Optional[Dict]:
    """One risk category by ID, e.g. 'leverage'. Case-insensitive."""
    return next((r for r in RISKS["risks"] if r["id"] == risk_id.lower()), None)


def documents_for_risk(risk_id: str) -> List[Dict]:
    """The register entries to check for one risk category."""
    r = risk(risk_id)
    return [get(i) for i in r["register_ids"]] if r else []


def format_document(d: Dict) -> str:
    """Plain-text rendering of one register entry."""
    lines = [f"{d['id']} · {d['document']} ({d['category']})",
             f"Status: {d['status']} — {STATUS_VALUES[d['status']]}",
             f"Should cover: {d['should_cover']}",
             f"Official URL: {d['official_url'] or '—'}",
             f"Last checked: {d['last_checked']}"]
    if d.get("notes"):
        lines.append(f"Notes: {d['notes']}")
    return "\n".join(lines)
