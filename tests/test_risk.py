"""Behaviour and consistency tests."""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

import fxfunds_risk_disclosures as fx
from fxfunds_risk_disclosures.__main__ import main

ROOT = Path(__file__).resolve().parent.parent
WEDNESDAY = datetime(2030, 1, 9, 10, 0, tzinfo=timezone.utc)
SATURDAY = datetime(2030, 1, 12, 10, 0, tzinfo=timezone.utc)
ROLLOVER = datetime(2030, 1, 9, 21, 30, tzinfo=timezone.utc)
STOCKS_NIGHT = datetime(2030, 1, 9, 2, 0, tzinfo=timezone.utc)


def test_generated_files_up_to_date():
    r = subprocess.run([sys.executable, str(ROOT / "tools/generate.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


@pytest.mark.parametrize("args, at, expected", [
    (("crypto", 20, 10), WEDNESDAY, 46),
    (("forex", 100, 10), WEDNESDAY, 39),
    (("forex", 100, 10), SATURDAY, 68),
    (("forex", 500, 50), WEDNESDAY, 82),
    (("forex", 30, 10, 1), WEDNESDAY, 10),
    (("forex", 30, 10, 1), SATURDAY, 24),
])
def test_readme_examples(args, at, expected):
    assert fx.trade_risk(*args, at=at)["risk_percent"] == expected


def test_timing_conditions():
    assert fx.timing("forex", WEDNESDAY)["label"] == "Normal market hours"
    assert fx.timing("forex", SATURDAY)["closed"]
    assert "rollover" in fx.timing("forex", ROLLOVER)["label"]
    assert fx.timing("stocks", STOCKS_NIGHT)["closed"]
    assert not fx.timing("crypto", SATURDAY)["closed"]
    assert fx.timing("crypto", SATURDAY)["score"] > fx.timing("crypto", WEDNESDAY)["score"]


def test_risk_rises_with_leverage_and_news():
    low = fx.trade_risk("forex", 10, 10, at=WEDNESDAY)["risk_percent"]
    high = fx.trade_risk("forex", 200, 10, at=WEDNESDAY)["risk_percent"]
    news = fx.trade_risk("forex", 10, 10, news=True, at=WEDNESDAY)["risk_percent"]
    assert low < high and low < news


def test_stop_loss_lowers_risk():
    no_stop = fx.trade_risk("crypto", 20, 20, at=WEDNESDAY)["risk_percent"]
    stop = fx.trade_risk("crypto", 20, 20, stop_pct=1, at=WEDNESDAY)["risk_percent"]
    assert stop < no_stop


def test_result_bounds_and_levels():
    for asset in fx.assets():
        for lev in (1, 10, 100, 1000):
            r = fx.trade_risk(asset, lev, 100, at=SATURDAY)
            assert 0 <= r["risk_percent"] <= 100
            assert r["level"] == fx.level(r["risk_percent"])
    assert [fx.level(s) for s in (0, 30, 31, 60, 61, 80, 81, 100)] == \
        ["Low", "Low", "Moderate", "Moderate", "High", "High", "Very high", "Very high"]


def test_trade_validation():
    with pytest.raises(ValueError):
        fx.trade_risk("bonds")
    with pytest.raises(ValueError):
        fx.trade_risk("forex", leverage=0.5)
    with pytest.raises(ValueError):
        fx.trade_risk("forex", margin_pct=150)


def test_transfer_risk():
    assert fx.transfer_risk("ERC-20", "trc20")["risk_percent"] == 100
    assert fx.transfer_risk("TRC20", "TRC20", address="0xabc")["risk_percent"] == 95
    assert fx.transfer_risk("TON", "TON", memo_required=True)["risk_percent"] == 85
    assert fx.transfer_risk("tron", "TRC20", first_time=True)["risk_percent"] == 30
    ok = fx.transfer_risk("ETH", "ERC20", address="0x" + "a" * 40)
    assert ok["risk_percent"] == 5 and ok["level"] == "Low"
    assert fx.transfer_risk("TRC20", "TRC20", address="T" + "9" * 33)["risk_percent"] == 5
    with pytest.raises(ValueError):
        fx.transfer_risk("BTC", "TRC20")


def test_risk_database():
    cats = fx.risks()
    assert [r["id"] for r in cats] == ["market", "leverage", "digital-asset", "stablecoin",
                                       "blockchain", "operational", "counterparty", "regulatory"]
    for r in cats:
        assert set(r) == {"id", "name", "keywords", "answer", "example", "faq"}
        assert r["keywords"] and r["answer"]
        for q in r["faq"]:
            assert q["question"].endswith("?") and q["answer"]
    assert len(fx.faq()) == 19
    questions = [q["question"] for q in fx.faq()]
    assert len(questions) == len(set(questions))


@pytest.mark.parametrize("term, expected", [
    ("SEC", ["regulatory"]),
    ("withdrawal", ["stablecoin", "operational"]),
    ("USDT", ["stablecoin", "blockchain"]),
    ("margin call", ["leverage"]),
    ("TRC-20", ["blockchain"]),
    ("custody", ["counterparty"]),
    ("zzz", []),
])
def test_ask(term, expected):
    assert [r["id"] for r in fx.ask(term)] == expected


def test_schema_faq_matches():
    schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
    page = next(n for n in schema["@graph"] if n["@type"] == "FAQPage")
    assert [q["name"] for q in page["mainEntity"]] == [q["question"] for q in fx.faq()]
    assert [q["acceptedAnswer"]["text"] for q in page["mainEntity"]] == [q["answer"] for q in fx.faq()]


def test_no_dates_or_street_addresses():
    month = r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b"
    year = r"\b(19|20)\d{2}\b"
    street = r"\b\d+\s+\w+\s+(Street|St\.|Avenue|Ave\.|Road|Rd\.)\b"
    files = [ROOT / "README.md", *(ROOT / "fxfunds_risk_disclosures").glob("*.json"),
             *(ROOT / "dataset").glob("*.csv"), *(ROOT / "docs").rglob("*.md"),
             ROOT / "schema.json", ROOT / "zenodo.json"]
    for f in files:
        text = f.read_text(encoding="utf-8")
        for pattern in (month, year, street):
            assert not re.search(pattern, text), f"{f.name}: matches {pattern}"


def test_cli(capsys):
    assert main(["trade", "--asset", "crypto", "--leverage", "20", "--margin", "10", "--at", WEDNESDAY.isoformat()]) == 0
    assert "Risk: 46% (Moderate)" in capsys.readouterr().out
    assert main(["transfer", "--network", "ERC20", "--expected", "TRC20", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["risk_percent"] == 100
    assert main(["ask", "withdrawal"]) == 0
    assert "How do FXFunds withdrawals work?" in capsys.readouterr().out
    assert main(["risk", "nope"]) == 1
