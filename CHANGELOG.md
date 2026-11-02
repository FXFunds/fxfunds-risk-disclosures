# Changelog

## 2.0.0

Fresh rewrite.

- New: `trade` gives a 0–100% risk figure for a trade at the moment it is checked, from leverage, margin, stop loss, volatility, market timing and news.
- New: `transfer` gives a risk % for a USDT transfer (network mismatch, address format, memo, first-time address).
- One risk database (`risk_faq.json` / `fxfunds_risk_faq.csv`): eight risk categories with FAQ keywords, answers, examples and only the related FAQs. Search it with `ask`.
- Removed the document register.
- Docs trimmed to a home page and the FAQ.
- Removed dates and locations from all content.

## 1.0.0

- Initial risk categories, docs, datasets and packages.
