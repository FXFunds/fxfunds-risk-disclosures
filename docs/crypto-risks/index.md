# Cryptocurrency and Stablecoin Risks

FXFunds project materials describe USDT payments on **TON**, **Ethereum (ERC20)** and **Tron (TRC20)**. This was not confirmed on publicly readable official pages at the last check (2026-10-19), so confirm the supported tokens and networks on the official deposit page before sending funds (register entry REG-09).

## Transfers Are Generally Irreversible

Once a blockchain transaction is confirmed, it usually cannot be cancelled or reversed. A mistake in the address, network or amount may mean the funds cannot be recovered.

## Choose the Right Network

USDT exists separately on each network. The receiving address and the sending network must match.

| Network | Address usually starts with | Fees paid in |
|---------|-----------------------------|--------------|
| Ethereum (ERC20) | `0x` | ETH |
| Tron (TRC20) | `T` | TRX, or energy and bandwidth |
| TON | `EQ` or `UQ` | TON |

Sending USDT on one network to an address expecting another can result in permanent loss. Some platforms also require a memo or comment for deposits; if one is required and missing, the deposit may not be credited automatically.

## Check the Address Carefully

- Copy and paste the address, then compare the first and last several characters.
- Watch for **address poisoning**: attackers send tiny transfers from look-alike addresses so that a wrong address appears in your history. Do not copy addresses from your transaction history.
- Consider a small test transfer before a large one.

## Wallet and Account Security

- Never share private keys, seed phrases, passwords or one-time codes with anyone, including people claiming to be support staff.
- Legitimate platforms do not need your private key or seed phrase to process a deposit or show a transaction status.
- Beware of fake websites, apps and social accounts imitating FXFunds. Type https://fxfunds.com/ yourself.

## Stablecoin Risks

- **Peg risk.** A stablecoin aims to stay at US$1 but can trade above or below it. USDT briefly traded below US$1 during market stress in May 2022.
- **Issuer risk.** USDT is issued by Tether. Its value depends on the issuer's reserves and operations, and the issuer can freeze tokens held at specific addresses.
- **Redemption.** Redeeming USDT directly with the issuer is generally limited to verified customers and subject to minimums and fees; most users rely on exchanges or platforms to convert it.
- **Network risk.** Each network can experience congestion, higher fees or outages that delay transfers.

## Confirmations and Timing

A transfer is credited only after the receiving platform sees enough network confirmations. The number required is set by the platform; FXFunds' requirement was not located publicly. The FXFunds open-source tools use reference defaults of 12 confirmations on Ethereum, 19 on Tron and 1 on TON. These are tool defaults, not platform rules.

## Third-Party Providers

Crypto deposits and withdrawals may rely on wallet providers, payment processors, blockchain data services or exchanges. Their outages, errors, fees or failures can affect your transaction.

## Related Tools

These open-source FXFunds tools are read-only and never move funds:

- [fxfunds-stablecoin-payments](https://github.com/FXFunds/fxfunds-stablecoin-payments) checks a USDT payment against a payment request
- [fxfunds-blockchain-technology](https://github.com/FXFunds/fxfunds-blockchain-technology) validates USDT addresses and transaction hashes and scores transaction signals
