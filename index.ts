#!/usr/bin/env node
/**
 * FXFunds Risk Disclosure Bot — Node.js library and CLI.
 * Gives a risk percentage for a trade or a USDT transfer at the moment it is checked.
 * Makes no network calls.
 */
import { readFileSync } from "fs";
import { join } from "path";

export interface Asset { name: string; daily_vol: number; market: "fx" | "stocks" | "crypto" }
export interface Network { name: string; pattern: string; aliases: string[] }
export interface Model {
  assets: Record<string, Asset>;
  weights: { wipe: number; loss: number; timing: number };
  scales: { wipe: number; loss: number; bad_day_sigma: number; stop_slippage: number; news_vol: number; news_timing: number };
  levels: { max: number; label: string }[];
  faq_sections: string[];
  networks: Record<string, Network>;
}
export interface FaqEntry { section: string; question: string; answer: string }
export interface RiskCategory { id: string; name: string; keywords: string[]; answer: string; example: string; faq: FaqEntry[] }
export interface Timing { score: number; vol_mult: number; closed: boolean; label: string }

export interface TradeInput {
  asset: string;
  leverage?: number;
  marginPct?: number;
  stopPct?: number;
  vol?: number;
  news?: boolean;
  at?: Date;
}
export interface TradeRisk {
  type: "trade"; asset: string; risk_percent: number; level: string;
  margin_wipe_chance: number; bad_day_loss: number; wipe_move: number; daily_vol: number; timing: string;
}
export interface TransferInput {
  network: string; expected: string; address?: string; firstTime?: boolean; memoRequired?: boolean; memo?: string;
}
export interface TransferRisk {
  type: "transfer"; network: string; expected: string; risk_percent: number; level: string; checks: string[];
}

const DATA_DIR = join(__dirname, "..", "fxfunds_risk_disclosures");
const load = <T>(name: string): T => JSON.parse(readFileSync(join(DATA_DIR, name), "utf8"));

export const MODEL: Model = load("model.json");
export const RISK_FAQ: RiskCategory[] = load("risk_faq.json");

const round1 = (n: number) => Math.round(n * 10) / 10;
const round2 = (n: number) => Math.round(n * 100) / 100;

/** Standard normal CDF (Abramowitz-Stegun 7.1.26, same as the Python build). */
function phi(z: number): number {
  const x = Math.abs(z) / Math.SQRT2;
  const t = 1 / (1 + 0.3275911 * x);
  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
  return 0.5 * (1 + (z >= 0 ? y : -y));
}

export const level = (score: number): string => MODEL.levels.find((l) => score <= l.max)!.label;

export function timing(asset: string, at: Date = new Date()): Timing {
  const market = MODEL.assets[asset].market;
  const day = (at.getUTCDay() + 6) % 7; // Monday = 0
  const hour = at.getUTCHours() + at.getUTCMinutes() / 60;

  if (market === "crypto") {
    if (day >= 5) return { score: 40, vol_mult: 1.0, closed: false, label: "Weekend — thinner crypto liquidity" };
    return { score: 20, vol_mult: 1.0, closed: false, label: "Crypto trades 24/7 — large moves can happen at any hour" };
  }
  if (day === 5 || (day === 6 && hour < 21) || (day === 4 && hour >= 21))
    return { score: 80, vol_mult: 1.5, closed: true, label: "Market closed — price can gap at reopen" };
  if (day === 4 && hour >= 18)
    return { score: 60, vol_mult: 1.2, closed: false, label: "Weekend gap ahead — market closes soon" };
  if (market === "stocks" && !(hour >= 13.5 && hour < 20))
    return { score: 60, vol_mult: 1.3, closed: true, label: "Outside main US exchange hours — price can gap at open" };
  if (market === "fx" && hour >= 21 && hour < 23)
    return { score: 50, vol_mult: 1.1, closed: false, label: "Daily rollover — low liquidity, wider spreads" };
  return { score: 10, vol_mult: 1.0, closed: false, label: "Normal market hours" };
}

export function tradeRisk(input: TradeInput): TradeRisk {
  const asset = input.asset.toLowerCase();
  const leverage = input.leverage ?? 1;
  const marginPct = input.marginPct ?? 100;
  const { stopPct, news = false } = input;
  if (!MODEL.assets[asset]) throw new Error(`Unknown asset '${asset}'. Use: ${Object.keys(MODEL.assets).join(", ")}`);
  if (leverage < 1 || !(marginPct > 0 && marginPct <= 100) || (stopPct !== undefined && stopPct <= 0))
    throw new Error("leverage must be ≥ 1, marginPct in (0, 100], stopPct > 0");

  const s = MODEL.scales, w = MODEL.weights;
  const t = timing(asset, input.at);
  const tScore = Math.min(100, t.score + (news ? s.news_timing : 0));
  const v = (input.vol || MODEL.assets[asset].daily_vol) * t.vol_mult * (news ? s.news_vol : 1);

  const wipeMove = 100 / leverage;
  let wipe = (1 - phi(wipeMove / v)) * 100;
  if (stopPct && stopPct < wipeMove && !t.closed) wipe *= s.stop_slippage;

  let badMove = s.bad_day_sigma * v;
  if (stopPct) badMove = Math.min(badMove, stopPct);
  const lossOfMargin = Math.min(100, badMove * leverage);
  const badDayLoss = (marginPct * lossOfMargin) / 100;

  let score = Math.round(
    w.wipe * Math.min(100, s.wipe * wipe) + w.loss * Math.min(100, s.loss * badDayLoss) + w.timing * tScore,
  );
  score = Math.max(0, Math.min(100, score));
  return {
    type: "trade", asset, risk_percent: score, level: level(score),
    margin_wipe_chance: round1(wipe), bad_day_loss: round1(badDayLoss),
    wipe_move: round2(wipeMove), daily_vol: round2(v),
    timing: t.label + (news ? "; high-impact news due" : ""),
  };
}

export function normalizeNetwork(name: string): string | undefined {
  const n = name.toUpperCase().replace(/ /g, "");
  return Object.keys(MODEL.networks).find((k) => MODEL.networks[k].aliases.includes(n));
}

export function transferRisk(input: TransferInput): TransferRisk {
  const sent = normalizeNetwork(input.network), exp = normalizeNetwork(input.expected);
  if (!sent || !exp) throw new Error(`Unknown network. Use: ${Object.keys(MODEL.networks).join(", ")}`);
  const N = MODEL.networks;
  const checks: [number, string][] = [];
  if (sent !== exp)
    checks.push([100, `Network mismatch — sending on ${N[sent].name} to an address expecting ${N[exp].name}; funds may be lost`]);
  if (input.address && !new RegExp(N[exp].pattern).test(input.address.trim()))
    checks.push([95, `Address does not match the ${N[exp].name} format`]);
  if (input.memoRequired && !input.memo)
    checks.push([85, "Memo / comment required but missing — deposit may not be credited"]);
  if (input.firstTime)
    checks.push([30, "First transfer to this address — send a small test amount first"]);
  if (!checks.length) checks.push([5, "Checks passed — confirm the full address and amount before sending"]);
  checks.sort((a, b) => b[0] - a[0]);
  const score = checks[0][0];
  return { type: "transfer", network: sent, expected: exp, risk_percent: score, level: level(score), checks: checks.map((c) => c[1]) };
}

export const assets = (): Record<string, Asset> => ({ ...MODEL.assets });
export const risks = (): RiskCategory[] => [...RISK_FAQ];
export const risk = (id: string): RiskCategory | undefined => RISK_FAQ.find((r) => r.id === id.toLowerCase());
/** Every FAQ entry, tagged with its risk category, in FAQ section order. */
export const faq = (): (FaqEntry & { risk: string })[] =>
  RISK_FAQ.flatMap((r) => r.faq.map((q) => ({ risk: r.id, ...q })))
    .sort((a, b) => MODEL.faq_sections.indexOf(a.section) - MODEL.faq_sections.indexOf(b.section));

const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/** Risk categories matching a term, keyword matches first. */
export function ask(term: string): RiskCategory[] {
  const t = term.toLowerCase().trim();
  if (!t) return [];
  const word = new RegExp(`\\b${esc(t)}(s|es)?\\b`);
  const byKeyword: RiskCategory[] = [], byText: RiskCategory[] = [];
  for (const r of RISK_FAQ) {
    const kws = r.keywords.map((k) => k.toLowerCase());
    if (kws.some((k) => word.test(k) || new RegExp(`\\b${esc(k)}\\b`).test(t))) byKeyword.push(r);
    else {
      const text = [r.name, r.answer, r.example, ...r.faq.map((q) => `${q.question} ${q.answer}`)].join(" ").toLowerCase();
      if (word.test(text)) byText.push(r);
    }
  }
  return [...byKeyword, ...byText];
}

// ---------------------------------------------------------------- CLI

const USAGE = `fxfunds-risk — FXFunds Risk Disclosure Bot

  fxfunds-risk trade --asset crypto --leverage 20 --margin 10 [--stop 3] [--vol 5] [--news]
  fxfunds-risk transfer --network TRC20 --expected TRC20 [--address T...] [--first-time] [--memo-required --memo X]
  fxfunds-risk assets              supported assets
  fxfunds-risk risks               risk categories
  fxfunds-risk risk leverage       one risk category with its FAQ
  fxfunds-risk ask withdrawal      search the risk database by keyword
  add --json to any command for JSON output`;

function parseFlags(args: string[]): { pos: string[]; flags: Record<string, string | true> } {
  const pos: string[] = [];
  const flags: Record<string, string | true> = {};
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith("--")) {
      const next = args[i + 1];
      if (next !== undefined && !next.startsWith("--")) { flags[a.slice(2)] = next; i++; }
      else flags[a.slice(2)] = true;
    } else pos.push(a);
  }
  return { pos, flags };
}

const num = (v: string | true | undefined): number | undefined => (typeof v === "string" ? Number(v) : undefined);
const str = (v: string | true | undefined): string | undefined => (typeof v === "string" ? v : undefined);

function printRisk(r: RiskCategory) {
  console.log(r.name);
  console.log(`  Answer:   ${r.answer}`);
  console.log(`  Example:  ${r.example}`);
  console.log(`  Keywords: ${r.keywords.join(", ")}`);
  for (const q of r.faq) console.log(`  Q: ${q.question}\n     ${q.answer}`);
}

export function cli(argv: string[]): number {
  const [cmd, ...rest] = argv;
  const { pos, flags } = parseFlags(rest);
  let data: unknown;
  let show: () => void;
  try {
    switch (cmd) {
      case "trade": {
        if (!str(flags.asset)) throw new Error("--asset is required");
        const r = tradeRisk({
          asset: str(flags.asset)!, leverage: num(flags.leverage), marginPct: num(flags.margin),
          stopPct: num(flags.stop), vol: num(flags.vol), news: flags.news === true,
          at: str(flags.at) ? new Date(str(flags.at)!) : undefined,
        });
        data = r;
        show = () => {
          console.log(`Risk: ${r.risk_percent}% (${r.level})`);
          console.log(`  Timing:              ${r.timing}`);
          console.log(`  Margin wipe chance:  ${r.margin_wipe_chance}% in one day`);
          console.log(`  Bad-day loss:        ${r.bad_day_loss}% of balance`);
          console.log(`  Wipe-out move:       ${r.wipe_move}% against you`);
          console.log(`  Daily volatility:    ${r.daily_vol}%`);
        };
        break;
      }
      case "transfer": {
        if (!str(flags.network) || !str(flags.expected)) throw new Error("--network and --expected are required");
        const r = transferRisk({
          network: str(flags.network)!, expected: str(flags.expected)!, address: str(flags.address),
          firstTime: flags["first-time"] === true, memoRequired: flags["memo-required"] === true, memo: str(flags.memo),
        });
        data = r;
        show = () => { console.log(`Risk: ${r.risk_percent}% (${r.level})`); r.checks.forEach((c) => console.log(`  - ${c}`)); };
        break;
      }
      case "assets":
        data = MODEL.assets;
        show = () => Object.entries(MODEL.assets).forEach(([k, a]) =>
          console.log(`${k.padEnd(9)}${a.name.padEnd(17)}typical daily move ${a.daily_vol}%`));
        break;
      case "risks":
        data = RISK_FAQ;
        show = () => RISK_FAQ.forEach((r) => console.log(`${r.id.padEnd(14)}${r.name} — ${r.answer}`));
        break;
      case "risk": {
        const r = risk(pos[0] || "");
        if (!r) { console.error(`No risk category '${pos[0]}'`); return 1; }
        data = r;
        show = () => printRisk(r);
        break;
      }
      case "ask": {
        const f = ask(pos.join(" "));
        data = f;
        show = () => { if (!f.length) console.log("No matching risk category."); f.forEach((r, i) => { if (i) console.log(); printRisk(r); }); };
        break;
      }
      case undefined:
      case "-h":
      case "--help":
      case "help":
        console.log(USAGE);
        return 0;
      default:
        console.error(USAGE);
        return 2;
    }
  } catch (e) {
    console.error((e as Error).message);
    return 1;
  }
  if (flags.json) console.log(JSON.stringify(data, null, 2));
  else show();
  return 0;
}

if (require.main === module) {
  process.exitCode = cli(process.argv.slice(2));
}
