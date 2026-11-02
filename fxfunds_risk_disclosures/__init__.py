"""FXFunds Risk Disclosure Bot.

Gives a risk percentage for a trade or a USDT transfer at the moment it is
checked, plus a risk database: risk categories with FAQ keywords, answers and
related FAQs. Makes no network calls.
"""

import json
import math
import re
from datetime import datetime, timezone
from importlib import resources

__version__ = "2.0.0"


def _load(name):
    return json.loads(resources.files(__package__).joinpath(name).read_text(encoding="utf-8"))


MODEL = _load("model.json")
RISK_FAQ = _load("risk_faq.json")


def _phi(z):
    """Standard normal CDF (Abramowitz-Stegun 7.1.26, same as the Node.js build)."""
    x = abs(z) / math.sqrt(2)
    t = 1 / (1 + 0.3275911 * x)
    y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * math.exp(-x * x)
    return 0.5 * (1 + (y if z >= 0 else -y))


def level(score):
    """Return the label for a 0–100 risk percentage."""
    return next(l["label"] for l in MODEL["levels"] if score <= l["max"])


def timing(asset, at=None):
    """Return the timing condition for an asset at a moment (default: now, UTC)."""
    at = (at or datetime.now(timezone.utc)).astimezone(timezone.utc)
    market = MODEL["assets"][asset]["market"]
    day, hour = at.weekday(), at.hour + at.minute / 60  # Monday = 0

    if market == "crypto":
        if day >= 5:
            return {"score": 40, "vol_mult": 1.0, "closed": False, "label": "Weekend — thinner crypto liquidity"}
        return {"score": 20, "vol_mult": 1.0, "closed": False, "label": "Crypto trades 24/7 — large moves can happen at any hour"}
    if day == 5 or (day == 6 and hour < 21) or (day == 4 and hour >= 21):
        return {"score": 80, "vol_mult": 1.5, "closed": True, "label": "Market closed — price can gap at reopen"}
    if day == 4 and hour >= 18:
        return {"score": 60, "vol_mult": 1.2, "closed": False, "label": "Weekend gap ahead — market closes soon"}
    if market == "stocks" and not (13.5 <= hour < 20):
        return {"score": 60, "vol_mult": 1.3, "closed": True, "label": "Outside main US exchange hours — price can gap at open"}
    if market == "fx" and 21 <= hour < 23:
        return {"score": 50, "vol_mult": 1.1, "closed": False, "label": "Daily rollover — low liquidity, wider spreads"}
    return {"score": 10, "vol_mult": 1.0, "closed": False, "label": "Normal market hours"}


def trade_risk(asset, leverage=1, margin_pct=100, stop_pct=None, vol=None, news=False, at=None):
    """Risk percentage for a trade at a moment.

    asset       forex | metals | stocks | futures | crypto
    leverage    e.g. 100 for 1:100
    margin_pct  share of account balance used as margin (0–100)
    stop_pct    stop-loss distance as % of price (optional)
    vol         current daily volatility % (optional; defaults to the asset's typical move)
    news        True if high-impact news is due
    at          datetime to evaluate (default: now)
    """
    asset = asset.lower()
    if asset not in MODEL["assets"]:
        raise ValueError(f"Unknown asset '{asset}'. Use: {', '.join(MODEL['assets'])}")
    if leverage < 1 or not 0 < margin_pct <= 100 or (stop_pct is not None and stop_pct <= 0):
        raise ValueError("leverage must be ≥ 1, margin_pct in (0, 100], stop_pct > 0")

    s, w = MODEL["scales"], MODEL["weights"]
    t = timing(asset, at)
    t_score = min(100, t["score"] + (s["news_timing"] if news else 0))
    v = (vol or MODEL["assets"][asset]["daily_vol"]) * t["vol_mult"] * (s["news_vol"] if news else 1)

    wipe_move = 100 / leverage
    wipe = (1 - _phi(wipe_move / v)) * 100
    if stop_pct and stop_pct < wipe_move and not t["closed"]:
        wipe *= s["stop_slippage"]

    bad_move = s["bad_day_sigma"] * v
    if stop_pct:
        bad_move = min(bad_move, stop_pct)
    loss_of_margin = min(100, bad_move * leverage)
    bad_day_loss = margin_pct * loss_of_margin / 100

    score = round(
        w["wipe"] * min(100, s["wipe"] * wipe)
        + w["loss"] * min(100, s["loss"] * bad_day_loss)
        + w["timing"] * t_score
    )
    score = max(0, min(100, score))
    timing_label = t["label"] + ("; high-impact news due" if news else "")
    return {
        "type": "trade",
        "asset": asset,
        "risk_percent": score,
        "level": level(score),
        "margin_wipe_chance": round(wipe, 1),
        "bad_day_loss": round(bad_day_loss, 1),
        "wipe_move": round(wipe_move, 2),
        "daily_vol": round(v, 2),
        "timing": timing_label,
    }


def normalize_network(name):
    """Return the canonical network key (TON, ERC20, TRC20) or None."""
    n = name.upper().replace(" ", "")
    return next((k for k, v in MODEL["networks"].items() if n in v["aliases"]), None)


def transfer_risk(network, expected, address=None, first_time=False, memo_required=False, memo=None):
    """Risk percentage for a USDT transfer before it is sent."""
    sent, exp = normalize_network(network), normalize_network(expected)
    if not sent or not exp:
        raise ValueError(f"Unknown network. Use: {', '.join(MODEL['networks'])}")
    checks = []
    if sent != exp:
        checks.append((100, f"Network mismatch — sending on {MODEL['networks'][sent]['name']} to an address expecting {MODEL['networks'][exp]['name']}; funds may be lost"))
    if address and not re.match(MODEL["networks"][exp]["pattern"], address.strip()):
        checks.append((95, f"Address does not match the {MODEL['networks'][exp]['name']} format"))
    if memo_required and not memo:
        checks.append((85, "Memo / comment required but missing — deposit may not be credited"))
    if first_time:
        checks.append((30, "First transfer to this address — send a small test amount first"))
    if not checks:
        checks.append((5, "Checks passed — confirm the full address and amount before sending"))
    score = max(c[0] for c in checks)
    return {
        "type": "transfer",
        "network": sent,
        "expected": exp,
        "risk_percent": score,
        "level": level(score),
        "checks": [c[1] for c in sorted(checks, reverse=True)],
    }


def assets():
    """Return supported assets with their typical daily move %."""
    return {k: dict(v) for k, v in MODEL["assets"].items()}


def risks():
    """Return every risk category with its keywords, answer, example and related FAQ."""
    return list(RISK_FAQ)


def risk(risk_id):
    """Return one risk category by id (e.g. 'leverage'), or None."""
    return next((r for r in RISK_FAQ if r["id"] == risk_id.lower()), None)


def faq():
    """Return every FAQ entry, tagged with its risk category, in FAQ section order."""
    order = MODEL["faq_sections"]
    items = [{"risk": r["id"], **q} for r in RISK_FAQ for q in r["faq"]]
    return sorted(items, key=lambda q: order.index(q["section"]))


def ask(term):
    """Return risk categories matching a term, keyword matches first.

    Matches keywords, category name, answer, and FAQ questions and answers.
    """
    t = term.lower().strip()
    if not t:
        return []
    word = re.compile(rf"\b{re.escape(t)}(s|es)?\b")
    by_keyword, by_text = [], []
    for r in RISK_FAQ:
        kws = [k.lower() for k in r["keywords"]]
        if any(word.search(k) or re.search(rf"\b{re.escape(k)}\b", t) for k in kws):
            by_keyword.append(r)
        else:
            text = " ".join([r["name"], r["answer"], r["example"]] + [q["question"] + " " + q["answer"] for q in r["faq"]])
            if word.search(text.lower()):
                by_text.append(r)
    return by_keyword + by_text


__all__ = [
    "trade_risk", "transfer_risk", "timing", "level", "normalize_network",
    "assets", "risks", "risk", "faq", "ask", "__version__",
]
