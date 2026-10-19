"""Command-line interface: fxfunds-risk / python -m fxfunds_risk_disclosures"""
import json
import sys

from . import (REGISTER, by_category, by_status, documents, documents_for_risk, format_document, get, missing,
               risk, risks, summary)


def main(argv=None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    cmd, rest = (args[0], args[1:]) if args else (None, [])
    arg = rest[0] if rest else ""

    def out_docs(items):
        if as_json:
            print(json.dumps(items, indent=2, ensure_ascii=False))
        elif not items:
            print("No matching documents.")
        else:
            print("\n\n".join(format_document(d) for d in items))

    if cmd == "documents":
        out_docs(documents())
    elif cmd == "missing":
        out_docs(missing())
    elif cmd == "status":
        out_docs(by_status(arg))
    elif cmd == "category":
        out_docs(by_category(arg))
    elif cmd == "show":
        d = get(arg)
        out_docs([d] if d else [])
    elif cmd == "risks":
        items = risks()
        if as_json:
            print(json.dumps(items, indent=2, ensure_ascii=False))
        else:
            for r in items:
                print(f"{r['id']:<14} {r['name']} — {r['consideration']}")
    elif cmd == "risk":
        r = risk(arg)
        if as_json:
            print(json.dumps({**r, "documents": documents_for_risk(arg)} if r else None, indent=2, ensure_ascii=False))
        elif not r:
            print("No matching risk. Run: fxfunds-risk risks")
        else:
            print(f"{r['name']}\n{r['consideration']}\nExample: {r['example']}\n\nDocuments to check:")
            for d in documents_for_risk(arg):
                print(f"  {d['id']} {d['document']} — {d['status']}")
    else:
        s = summary()
        if as_json:
            print(json.dumps(s, indent=2))
            return
        print(f"\n{REGISTER['title']} — last checked {s['last_checked']}")
        print("=" * 60)
        print(f"  Documents tracked: {s['total']}")
        for status in REGISTER["status_values"]:
            print(f"  {status:<13} {s[status]}")
        print("\nUsage:")
        print("  fxfunds-risk missing")
        print("  fxfunds-risk show REG-02")
        print("  fxfunds-risk category Legal")
        print("  fxfunds-risk status located")
        print("  fxfunds-risk risks")
        print("  fxfunds-risk risk leverage")
        print("  fxfunds-risk documents [--json]")
        print(f"\nInformational only, not legal or financial advice. Official website: {REGISTER['official_website']}\n")


if __name__ == "__main__":
    main()
