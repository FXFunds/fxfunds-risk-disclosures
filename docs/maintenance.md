# Maintenance Policy

## Review Schedule

- Every link in the register is reviewed at least **once a quarter**, and whenever FXFunds announces a change.
- The `last_checked` date is updated on every review, even when nothing changed.

## What Is Recorded for Each Document

| Field | Description |
|-------|-------------|
| `document` | Title as published by FXFunds |
| `official_url` | Direct link on an official FXFunds domain |
| `document_date` | Version or effective date shown on the document |
| `last_checked` | Date the link was last opened and reviewed |
| `status` | `located`, `not-located`, `inaccessible` or `outdated` |
| `notes` | Limitations, for example "applies to EU clients only" |

## Rules

1. **Only official sources.** A document counts as located only if it is published by FXFunds on an official FXFunds domain or provided in an FXFunds account.
2. **No fictional documents.** Never create, invent or reconstruct licences, legal terms, regulatory approvals, licence numbers or company details.
3. **Link, don't copy.** Link to official documents; short summaries must be labelled as summaries and must not replace the original.
4. **Keep files in sync.** `fxfunds_risk_disclosures/register.json` is the single source. Update `docs/document-register.md`, `dataset/fxfunds_document_register.csv` and, if affected, the relevant section page, run `pytest`, then add a `CHANGELOG.md` entry.
5. **Record what is missing.** If a document cannot be found or opened, record that rather than removing the entry.

## Updating an Entry

1. Open the official document and note its title, URL and date.
2. Set `status` to `located` and fill in `official_url`, `document_date` and `last_checked` in `fxfunds_risk_disclosures/register.json`.
3. Update the matching row in `docs/document-register.md` and `dataset/fxfunds_document_register.csv`, then run `pytest`.
4. Add a `CHANGELOG.md` entry, for example: `REG-02 Risk disclosure located — <URL> — checked <date>`.
