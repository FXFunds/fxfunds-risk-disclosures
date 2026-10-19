# Use the Register in Code

The document register and risk categories ship as an offline library for Node.js and Python. Both packages contain the same `register.json` and `risks.json` and make no network calls.

| | Node.js | Python |
|---|---|---|
| Package | [`@fxfunds/risk-disclosures`](https://www.npmjs.com/package/@fxfunds/risk-disclosures) | [`fxfunds-risk-disclosures`](https://pypi.org/project/fxfunds-risk-disclosures/) |
| Install | `npm install @fxfunds/risk-disclosures` | `pip install fxfunds-risk-disclosures` |
| Import | `require("@fxfunds/risk-disclosures")` | `import fxfunds_risk_disclosures` |
| CLI | `npx @fxfunds/risk-disclosures` | `fxfunds-risk` or `python -m fxfunds_risk_disclosures` |
| Runtime | Node.js 18+ | Python 3.9+ |

## Command Line

| Command | Shows |
|---------|-------|
| `fxfunds-risk` | Register summary: total and count by status |
| `fxfunds-risk missing` | Every document not yet located |
| `fxfunds-risk show REG-02` | One register entry |
| `fxfunds-risk category Legal` | Entries in a category |
| `fxfunds-risk status located` | Entries with a status |
| `fxfunds-risk risks` | All risk categories |
| `fxfunds-risk risk leverage` | One risk and the documents to check |
| `fxfunds-risk documents --json` | Everything as JSON |

Categories: `General`, `Trading`, `Payments`, `Crypto`, `Legal`, `Privacy`. Statuses: `located`, `not-located`, `inaccessible`, `outdated`. Risk IDs: `market`, `leverage`, `digital-asset`, `stablecoin`, `blockchain`, `operational`, `counterparty`, `regulatory`.

## API

| Node.js | Python | Returns |
|---------|--------|---------|
| `documents()` | `documents()` | Every register entry |
| `get(id)` | `get(id)` | One entry or `undefined` / `None` |
| `byStatus(status)` | `by_status(status)` | Entries with a status |
| `byCategory(name)` | `by_category(name)` | Entries in a category |
| `categories()` | `categories()` | Category names |
| `missing()` | `missing()` | Entries that are not `located` |
| `summary()` | `summary()` | Total and count by status |
| `risks()` | `risks()` | Every risk category |
| `risk(id)` | `risk(id)` | One risk category |
| `documentsForRisk(id)` | `documents_for_risk(id)` | Register entries to check for a risk |
| `format(entry)` | `format_document(entry)` | Plain-text rendering of an entry |
| `REGISTER`, `RISKS`, `STATUS_VALUES`, `LAST_CHECKED` | same | Raw data |

IDs and categories are case-insensitive. Node.js and Python return the same results; the tests check this.

## Register Entry Fields

| Field | Example |
|-------|---------|
| `id` | `REG-02` |
| `category` | `Trading` |
| `document` | Risk disclosure / risk warning |
| `should_cover` | Risks of each product, leverage, possibility of loss |
| `status` | `not-located` |
| `official_url` | `null` until located |
| `document_date` | `null` until located |
| `last_checked` | 2026-10-19 |
| `notes` | Not located on publicly readable pages or by public web search. |

## Datasets

`dataset/fxfunds_document_register.csv` holds the register with an extra `status_label` column. `dataset/fxfunds_risk_categories.csv` holds the risk categories; `register_ids` is separated by semicolons. Both are published on [Hugging Face](https://huggingface.co/datasets/FXFunds/risk-disclosures) and [Kaggle](https://www.kaggle.com/datasets/fxfunds/risk-disclosures).
