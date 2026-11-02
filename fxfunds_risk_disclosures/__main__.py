"""Command-line interface: python -m fxfunds_risk_disclosures (or fxfunds-risk)."""

import argparse
import json
import sys
from datetime import datetime

from . import ask, assets, risk, risks, trade_risk, transfer_risk, __version__


def _print_trade(r):
    print(f"Risk: {r['risk_percent']}% ({r['level']})")
    print(f"  Timing:              {r['timing']}")
    print(f"  Margin wipe chance:  {r['margin_wipe_chance']:g}% in one day")
    print(f"  Bad-day loss:        {r['bad_day_loss']:g}% of balance")
    print(f"  Wipe-out move:       {r['wipe_move']:g}% against you")
    print(f"  Daily volatility:    {r['daily_vol']:g}%")


def _print_transfer(r):
    print(f"Risk: {r['risk_percent']}% ({r['level']})")
    for c in r["checks"]:
        print(f"  - {c}")


def _risk(r):
    print(f"{r['name']}")
    print(f"  Answer:   {r['answer']}")
    print(f"  Example:  {r['example']}")
    print(f"  Keywords: {', '.join(r['keywords'])}")
    for q in r["faq"]:
        print(f"  Q: {q['question']}\n     {q['answer']}")


def _risks(entries):
    if not entries:
        print("No matching risk category.")
    for i, r in enumerate(entries):
        if i:
            print()
        _risk(r)


def build_parser():
    p = argparse.ArgumentParser(prog="fxfunds-risk", description="FXFunds Risk Disclosure Bot")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd")

    t = sub.add_parser("trade", help="risk %% for a trade right now")
    t.add_argument("--asset", required=True, choices=list(assets()))
    t.add_argument("--leverage", type=float, default=1)
    t.add_argument("--margin", type=float, default=100, help="%% of balance used as margin")
    t.add_argument("--stop", type=float, help="stop-loss distance %%")
    t.add_argument("--vol", type=float, help="current daily volatility %%")
    t.add_argument("--news", action="store_true", help="high-impact news due")
    t.add_argument("--at", help=argparse.SUPPRESS)
    t.add_argument("--json", action="store_true")

    x = sub.add_parser("transfer", help="risk %% for a USDT transfer")
    x.add_argument("--network", required=True, help="network you are sending on")
    x.add_argument("--expected", required=True, help="network the address expects")
    x.add_argument("--address")
    x.add_argument("--first-time", action="store_true")
    x.add_argument("--memo-required", action="store_true")
    x.add_argument("--memo")
    x.add_argument("--json", action="store_true")

    for name in ("risks", "assets"):
        s = sub.add_parser(name)
        s.add_argument("--json", action="store_true")
    r = sub.add_parser("risk")
    r.add_argument("id")
    r.add_argument("--json", action="store_true")
    a = sub.add_parser("ask", help="search the risk database by keyword")
    a.add_argument("term")
    a.add_argument("--json", action="store_true")
    return p


def main(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    if not args.cmd:
        p.print_help()
        return 0
    try:
        if args.cmd == "trade":
            at = datetime.fromisoformat(args.at) if args.at else None
            data = trade_risk(args.asset, args.leverage, args.margin, args.stop, args.vol, args.news, at)
            show = _print_trade
        elif args.cmd == "transfer":
            data = transfer_risk(args.network, args.expected, args.address, args.first_time, args.memo_required, args.memo)
            show = _print_transfer
        elif args.cmd == "risks":
            data = risks()
            show = lambda d: [print(f"{r['id']:<14}{r['name']} — {r['answer']}") for r in d]
        elif args.cmd == "assets":
            data = assets()
            show = lambda d: [print(f"{k:<9}{v['name']:<17}typical daily move {v['daily_vol']}%") for k, v in d.items()]
        elif args.cmd == "risk":
            data = risk(args.id)
            if data is None:
                print(f"No risk category '{args.id}'", file=sys.stderr)
                return 1
            show = _risk
        else:
            data = ask(args.term)
            show = _risks
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        show(data)
    return 0


if __name__ == "__main__":
    sys.exit(main())
