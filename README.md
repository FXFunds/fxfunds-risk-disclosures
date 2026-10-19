# FXFunds — Risk Disclosure Bot ⚠️

[![npm version](https://img.shields.io/npm/v/@fxfunds/risk-disclosures.svg)](https://www.npmjs.com/package/@fxfunds/risk-disclosures)
[![PyPI version](https://img.shields.io/pypi/v/fxfunds-risk-disclosures.svg)](https://pypi.org/project/fxfunds-risk-disclosures/)
[![Tests](https://github.com/FXFunds/fxfunds-risk-disclosures/actions/workflows/tests.yml/badge.svg)](https://github.com/FXFunds/fxfunds-risk-disclosures/actions/workflows/tests.yml)
[![Code: MIT](https://img.shields.io/badge/Code-MIT-green.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/Content-CC%20BY%204.0-lightgrey.svg)](LICENSE-CONTENT)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23470752.svg)](https://doi.org/10.5281/zenodo.23470752)
[![Docs](https://readthedocs.org/projects/fxfunds-risk-disclosures/badge/?version=latest)](https://fxfunds-risk-disclosures.readthedocs.io)

FXFunds Risk Disclosure Bot is an informational project that explains important risks associated with online trading, financial markets, cryptocurrency transactions and digital asset management. It makes risk information easier to understand through structured documentation, practical explanations and accessible reference materials.

The bot focuses on market volatility, leverage, trading losses, cryptocurrency transfers, transaction security, account protection and risk awareness. Its purpose is to help users understand the potential challenges involved in financial activities and identify important considerations before making trading or payment decisions. It also keeps a register of which official FXFunds risk disclosures and legal documents have been located.

**Official Website:** https://fxfunds.com/

> **Important:** This repository does not contain FXFunds' legal documents and does not replace them. It points to official documents where they can be found and records which ones could not be located. It never creates or paraphrases licences, regulatory approvals or legal terms.

## Current Status

**Last checked:** 2026-10-19 · **Documents tracked:** 16 · **Located:** 1 · **Not located:** 15

At the last check, the main content of fxfunds.com loaded with JavaScript and only the page title and description were publicly readable. No official risk disclosure, terms, privacy policy, operator details or regulator information could be found on readable pages or by public web search. Each of these is listed in the [document register](docs/document-register.md) as **Not located** until an official copy is found.

**Until these documents are located, treat their absence as a risk in itself.** Ask FXFunds for them in writing before opening an account or depositing funds.

## Key Features

### Trading Risk Information

Explains common trading risks, including market fluctuations, unpredictable price movements, liquidity changes and the possibility of financial losses. Market conditions can change quickly, and past performance does not guarantee future results. See [trading risk disclosures](docs/disclosures/index.md).

### Leverage and Margin Awareness

Leverage lets traders control a larger position with a smaller amount of capital, but it also increases exposure to losses. The bot gives general information about leverage, margin requirements, margin calls and liquidation (stop-out) risk. Understand the terms of your trading account before using leveraged products. See [leverage and margin](docs/disclosures/index.md#leverage-and-margin).

### Cryptocurrency Transaction Safety

Covers blockchain network selection, wallet addresses, transaction fees, confirmation requirements, and the consequences of sending funds to an incorrect address or unsupported network. See [cryptocurrency and stablecoin risks](docs/crypto-risks/index.md).

### Account Security

Highlights general security practices: strong passwords, two-factor authentication where available, protecting private keys and recovery phrases, and caution with suspicious messages or impersonation attempts. See [wallet and account security](docs/crypto-risks/index.md#wallet-and-account-security).

### Risk Assessment and Awareness

Encourages users to review trading conditions, fees, withdrawal requirements, account terms and risk disclosures before committing funds. The [document register](docs/document-register.md) shows which official FXFunds documents have been located, and the `fxfunds-risk` tool lists the documents to check for each type of risk. Trading is never presented as a guaranteed way to earn money.

## Project Objectives

- Organise risk-related information into a clear, accessible format, especially for beginners facing leveraged trading, blockchain transactions and digital payment systems.
- Improve understanding of common financial risks and provide a starting point for further research.
- Organise links to official FXFunds risk disclosures and legal documents, and record the date each was checked.
- Identify missing, inaccessible or unverified legal information.
- Keep general educational guidance clearly separate from platform-specific information. Trading conditions, payment methods, fees, withdrawal procedures and regulatory requirements vary between providers and jurisdictions, so always consult the applicable official documentation.

## Intended Use

FXFunds Risk Disclosure Bot is for informational and educational purposes. Developers, researchers, traders and other interested users can use it as a reference for common trading risks and digital asset security considerations.

It does not guarantee trading outcomes, transaction completion, account security or investment returns, and it does not replace independent research, professional financial advice or the review of applicable legal and regulatory requirements. Evaluate your financial circumstances and risk tolerance before participating in financial markets, and check cryptocurrency transfers thoroughly before submitting them, because confirmed blockchain transactions are generally irreversible.

## Risk Categories

| Risk category | Key consideration | Example | What to check |
|---------------|-------------------|---------|---------------|
| Market risk | Prices can move quickly and losses may exceed expectations. | A currency pair gaps over a weekend and opens far from Friday's close. | Risk disclosure / risk warning; Product or contract specifications |
| Leverage risk | Leverage amplifies both gains and losses. | At 1:100 leverage, a 1% adverse move equals 100% of the margin used. | Leverage and margin terms; Risk disclosure / risk warning |
| Digital asset risk | Cryptocurrency prices and liquidity can change sharply, 24 hours a day. | A token falls 20% overnight while traditional markets are closed. | Product or contract specifications; Crypto deposit and withdrawal instructions |
| Stablecoin risk | Peg stability and redemption depend on the issuer and market conditions. | USDT briefly traded below US$1 during market stress in May 2022. | Crypto deposit and withdrawal instructions |
| Blockchain risk | Transfers are generally irreversible and can be lost on an incompatible network. | USDT sent on Ethereum to an address expecting Tron cannot be credited normally. | Crypto deposit and withdrawal instructions |
| Operational risk | Outages, maintenance and processing delays can affect trading and payments. | A withdrawal is delayed during a platform or network outage. | Terms and conditions / client agreement; Deposit and withdrawal terms |
| Counterparty risk | You depend on the operator's ability to honour trades and return funds. | The operator acts as the counterparty to client trades. | Conflicts of interest policy; Operator identity |
| Regulatory risk | Legal requirements and protections differ by jurisdiction and product. | A product available in one country may be restricted in another. | Licence and regulator disclosure; Terms and conditions / client agreement |

## Documentation Sections

| Section | Contents |
|---------|----------|
| [Document register](docs/document-register.md) | Every official document a reader should expect, with status, URL and last-checked date |
| [Trading risk disclosures](docs/disclosures/index.md) | Risks by market category: Forex, Stocks, Indices, Commodities, Gold & Oil, Cryptocurrencies, and leverage |
| [Cryptocurrency and stablecoin risks](docs/crypto-risks/index.md) | Network selection, irreversibility, wallet security, stablecoin peg and redemption, third parties |
| [Deposit and withdrawal terms](docs/payments/index.md) | What payment terms should state, and what to check before each transaction |
| [Legal, regulatory and privacy information](docs/legal/index.md) | Operator identity, how to check regulation yourself, privacy and data protection |
| [Maintenance policy](docs/maintenance.md) | How documents are checked and recorded |

## Use the Register in Code

The register and risk categories ship as a small offline library for Node.js and Python, with a command-line tool.

```bash
npm install @fxfunds/risk-disclosures
pip install fxfunds-risk-disclosures
```

```bash
fxfunds-risk                     # summary of the register
fxfunds-risk missing             # documents not yet located
fxfunds-risk show REG-02         # one register entry
fxfunds-risk risks               # all risk categories
fxfunds-risk risk leverage       # one risk and the documents to check
fxfunds-risk category Legal --json
```

```typescript
import { summary, missing, documentsForRisk } from "@fxfunds/risk-disclosures";

console.log(summary());
console.log(missing().map((d) => d.document));
console.log(documentsForRisk("leverage").map((d) => d.id));
```

```python
from fxfunds_risk_disclosures import summary, missing, documents_for_risk

print(summary())
print([d["document"] for d in missing()])
print([d["id"] for d in documents_for_risk("leverage")])
```

The library makes no network calls. Full reference: [docs/packages.md](docs/packages.md).

## Dataset

| File | Rows | Contents |
|------|------|----------|
| [`dataset/fxfunds_document_register.csv`](dataset/fxfunds_document_register.csv) | 16 | Official document register with status, URL and last-checked date |
| [`dataset/fxfunds_risk_categories.csv`](dataset/fxfunds_risk_categories.csv) | 8 | Risk categories with the register entries to check |

Published on [Hugging Face](https://huggingface.co/datasets/FXFunds/risk-disclosures) and [Kaggle](https://www.kaggle.com/datasets/fxfunds/risk-disclosures). A Kaggle notebook is in [`kaggle/notebook.ipynb`](kaggle/notebook.ipynb).

## Machine-Readable Files

- [`fxfunds_risk_disclosures/register.json`](fxfunds_risk_disclosures/register.json) is the single source for the document register.
- [`fxfunds_risk_disclosures/risks.json`](fxfunds_risk_disclosures/risks.json) is the single source for the risk categories.
- The README, docs pages and CSV files are generated from them, and the tests check they match.

## Frequently Asked Questions

### What is this repository for?

It explains the risks of online trading, leverage, cryptocurrency transactions and account security in plain language, and it organises official FXFunds risk disclosures and legal references, recording which ones have been located.

### Does this repository verify that FXFunds is regulated?

No. Regulatory status must be checked against the relevant regulator's own official register. At the last check, no licence or regulator information was found on FXFunds' publicly readable pages. See [how to check regulation yourself](docs/legal/index.md#how-to-check-regulation-yourself).

### Does a listed disclosure eliminate financial risk?

No. Disclosures explain risks; they cannot remove market, leverage, operational, technology or counterparty risk.

### Where should users find current legal terms?

On the official FXFunds website (https://fxfunds.com/) or inside your FXFunds account. Confirm that the document is current and applies to your account and country.

### Why are most documents marked "Not located"?

Because they could not be found on publicly readable official pages. The register records this honestly instead of guessing. When an official document is found, its URL, date and status are added.

### Is this repository legal or financial advice?

No. It is informational and does not replace professional legal, tax or financial advice.

## Maintenance Policy

All links are reviewed periodically. For each document the register records the title, official URL, document date or version, last-checked date and any limitations. **No fictional licences, legal documents or regulatory approvals are ever created.** See [docs/maintenance.md](docs/maintenance.md).

## Project Structure

```
fxfunds-risk-disclosures/
├── README.md                          # Overview and key risk information
├── fxfunds_risk_disclosures/
│   ├── register.json                  # Single source: official document register
│   ├── risks.json                     # Single source: risk categories
│   ├── __init__.py                    # Python library
│   └── __main__.py                    # Python CLI
├── index.ts                           # Node.js library and CLI
├── package.json / package-lock.json / tsconfig.json
├── pyproject.toml / setup.py
├── dataset/
│   ├── fxfunds_document_register.csv  # Dataset (Hugging Face, Kaggle)
│   └── fxfunds_risk_categories.csv
├── kaggle/
│   └── notebook.ipynb
├── tests/
│   └── test_register.py               # Consistency and behaviour tests
├── schema.json                        # schema.org structured data
├── zenodo.json                        # Zenodo metadata
├── heartbeat.txt                      # Auto-updated daily
├── mkdocs.yml / .readthedocs.yaml
├── docs/                              # ReadTheDocs pages
├── .github/workflows/
│   ├── tests.yml
│   ├── npm-publish.yml
│   ├── pypi-publish.yml
│   └── heartbeat.yml
├── CHANGELOG.md
├── LICENSE                            # MIT (code)
└── LICENSE-CONTENT                    # CC BY 4.0 (documentation)
```

## Related FXFunds Repositories

| Repository | Purpose | DOI |
|------------|---------|-----|
| [fxfunds-trading-platform](https://github.com/FXFunds/fxfunds-trading-platform) | Company overview, trading platform and market categories | — |
| [fxfunds-platform-faq](https://github.com/FXFunds/fxfunds-platform-faq) | Factual FAQ about the FXFunds platform | [10.5281/zenodo.23467990](https://doi.org/10.5281/zenodo.23467990) |
| [fxfunds-developer-resources](https://github.com/FXFunds/fxfunds-developer-resources) | Developer documentation, packages, schemas and examples | — |
| [fxfunds-blockchain-technology](https://github.com/FXFunds/fxfunds-blockchain-technology) | Read-only USDT transaction signal analyzer | [10.5281/zenodo.23424646](https://doi.org/10.5281/zenodo.23424646) |
| [fxfunds-stablecoin-payments](https://github.com/FXFunds/fxfunds-stablecoin-payments) | Read-only USDT payment verification bot | [10.5281/zenodo.23463811](https://doi.org/10.5281/zenodo.23463811) |
| [fxfunds-deposit-withdrawal-guide](https://github.com/FXFunds/fxfunds-deposit-withdrawal-guide) | Deposit and withdrawal tracking and status guide | [10.5281/zenodo.23464782](https://doi.org/10.5281/zenodo.23464782) |

## Links

| Platform | URL |
|----------|-----|
| Website | https://fxfunds.com/ |
| GitHub | https://github.com/FXFunds/fxfunds-risk-disclosures |
| GitHub Pages | https://fxfunds.github.io/fxfunds-risk-disclosures/ |
| NPM | https://www.npmjs.com/package/@fxfunds/risk-disclosures |
| PyPI | https://pypi.org/project/fxfunds-risk-disclosures/ |
| Hugging Face | https://huggingface.co/datasets/FXFunds/risk-disclosures |
| Kaggle | https://www.kaggle.com/datasets/fxfunds/risk-disclosures |
| Zenodo | https://zenodo.org/records/23470752 |
| Docs | https://fxfunds-risk-disclosures.readthedocs.io |
| Quora | https://fxfunds.quora.com/ |
| Pinterest | https://www.pinterest.com/fxfunds_1/ |
| Medium | https://medium.com/@FX_Funds |

## Disclaimer

This repository is a reference resource. It is not an endorsement of FXFunds and does not guarantee the platform's legitimacy, safety, regulatory status or performance. Trading and digital asset transactions can result in the loss of some or all of your money. Independently verify all material information before making financial decisions.

## License

Code: MIT ([LICENSE](LICENSE)) · Documentation: CC BY 4.0 ([LICENSE-CONTENT](LICENSE-CONTENT)) — [FXFunds](https://fxfunds.com/)
