# FXFunds Risk Disclosure Bot

Tells you how much risk, as a percentage, a trade or a USDT transfer carries at the moment you check it.

**Official website:** [https://fxfunds.com/](https://fxfunds.com/)

```bash
npm install @fxfunds/risk-disclosures
pip install fxfunds-risk-disclosures

fxfunds-risk trade --asset crypto --leverage 20 --margin 10
fxfunds-risk transfer --network TRC20 --expected TRC20 --first-time
```

| Risk % | Level |
|--------|-------|
| 0–30 | Low |
| 31–60 | Moderate |
| 61–80 | High |
| 81–100 | Very high |

See the [Risk FAQ](faq.md) for FAQs grouped by risk category, or run `fxfunds-risk ask <keyword>`.

This is a reference tool, not financial advice and not an endorsement of FXFunds. The risk percentage is an estimate and does not predict market moves.
