#!/usr/bin/env node
/**
 * FXFunds Risk Disclosure Bot
 * Read the FXFunds official document register and risk categories: which official
 * documents have been located, which are missing, and which documents to check for
 * each type of risk. Works offline; no network calls.
 * Built by FXFunds — https://fxfunds.com/
 */

export type Status = "located" | "not-located" | "inaccessible" | "outdated";

export interface RegisterEntry {
  id: string;
  category: string;
  document: string;
  should_cover: string;
  status: Status;
  official_url: string | null;
  document_date: string | null;
  last_checked: string;
  notes: string;
}

export interface Risk {
  id: string;
  name: string;
  consideration: string;
  example: string;
  register_ids: string[];
  what_to_check: string;
}

interface RegisterData {
  title: string;
  official_website: string;
  last_checked: string;
  status_values: Record<Status, string>;
  documents: RegisterEntry[];
}

interface RisksData {
  title: string;
  last_checked: string;
  risks: Risk[];
}

// eslint-disable-next-line @typescript-eslint/no-var-requires
const register: RegisterData = require("./fxfunds_risk_disclosures/register.json");
// eslint-disable-next-line @typescript-eslint/no-var-requires
const riskData: RisksData = require("./fxfunds_risk_disclosures/risks.json");

export const REGISTER: Readonly<RegisterData> = register;
export const RISKS: Readonly<RisksData> = riskData;
export const STATUS_VALUES = register.status_values;
export const LAST_CHECKED = register.last_checked;

/** All register entries, in register order. */
export function documents(): RegisterEntry[] {
  return [...register.documents];
}

/** One register entry by ID, e.g. "REG-02". Case-insensitive. */
export function get(id: string): RegisterEntry | undefined {
  return register.documents.find((d) => d.id.toLowerCase() === id.toLowerCase());
}

export function byStatus(status: Status): RegisterEntry[] {
  return register.documents.filter((d) => d.status === status);
}

/** Entries in one category (General, Trading, Payments, Crypto, Legal, Privacy). Case-insensitive. */
export function byCategory(category: string): RegisterEntry[] {
  return register.documents.filter((d) => d.category.toLowerCase() === category.toLowerCase());
}

/** Register categories in order of first appearance. */
export function categories(): string[] {
  return [...new Set(register.documents.map((d) => d.category))];
}

/** Every entry that is not "located". */
export function missing(): RegisterEntry[] {
  return register.documents.filter((d) => d.status !== "located");
}

/** Counts by status, plus total and last-checked date. */
export function summary(): Record<string, number | string> {
  const out: Record<string, number | string> = { total: register.documents.length, last_checked: LAST_CHECKED };
  for (const status of Object.keys(register.status_values) as Status[]) out[status] = byStatus(status).length;
  return out;
}

/** All risk categories. */
export function risks(): Risk[] {
  return [...riskData.risks];
}

/** One risk category by ID, e.g. "leverage". Case-insensitive. */
export function risk(id: string): Risk | undefined {
  return riskData.risks.find((r) => r.id === id.toLowerCase());
}

/** The register entries to check for one risk category. */
export function documentsForRisk(id: string): RegisterEntry[] {
  const r = risk(id);
  return r ? r.register_ids.map((i) => get(i) as RegisterEntry) : [];
}

/** Plain-text rendering of one register entry. */
export function format(d: RegisterEntry): string {
  const lines = [
    `${d.id} · ${d.document} (${d.category})`,
    `Status: ${d.status} — ${register.status_values[d.status]}`,
    `Should cover: ${d.should_cover}`,
    `Official URL: ${d.official_url ?? "—"}`,
    `Last checked: ${d.last_checked}`,
  ];
  if (d.notes) lines.push(`Notes: ${d.notes}`);
  return lines.join("\n");
}

function main(): void {
  const argv = process.argv.slice(2);
  const json = argv.includes("--json");
  const args = argv.filter((a) => a !== "--json");
  const [cmd, arg = ""] = args;
  const outDocs = (items: RegisterEntry[]) => {
    if (json) { console.log(JSON.stringify(items, null, 2)); return; }
    if (!items.length) { console.log("No matching documents."); return; }
    console.log(items.map(format).join("\n\n"));
  };

  switch (cmd) {
    case "documents": outDocs(documents()); break;
    case "missing": outDocs(missing()); break;
    case "status": outDocs(byStatus(arg as Status)); break;
    case "category": outDocs(byCategory(arg)); break;
    case "show": { const d = get(arg); outDocs(d ? [d] : []); break; }
    case "risks": {
      if (json) { console.log(JSON.stringify(risks(), null, 2)); break; }
      for (const r of risks()) console.log(`${r.id.padEnd(14)} ${r.name} — ${r.consideration}`);
      break;
    }
    case "risk": {
      const r = risk(arg);
      if (json) { console.log(JSON.stringify(r ? { ...r, documents: documentsForRisk(arg) } : null, null, 2)); break; }
      if (!r) { console.log("No matching risk. Run: fxfunds-risk risks"); break; }
      console.log(`${r.name}\n${r.consideration}\nExample: ${r.example}\n\nDocuments to check:`);
      for (const d of documentsForRisk(arg)) console.log(`  ${d.id} ${d.document} — ${d.status}`);
      break;
    }
    default: {
      const s = summary();
      if (json) { console.log(JSON.stringify(s, null, 2)); break; }
      console.log(`\n${register.title} — last checked ${s.last_checked}`);
      console.log("=".repeat(60));
      console.log(`  Documents tracked: ${s.total}`);
      for (const status of Object.keys(register.status_values)) console.log(`  ${status.padEnd(13)} ${s[status]}`);
      console.log("\nUsage:");
      console.log("  fxfunds-risk missing");
      console.log("  fxfunds-risk show REG-02");
      console.log("  fxfunds-risk category Legal");
      console.log("  fxfunds-risk status located");
      console.log("  fxfunds-risk risks");
      console.log("  fxfunds-risk risk leverage");
      console.log("  fxfunds-risk documents [--json]");
      console.log(`\nInformational only, not legal or financial advice. Official website: ${register.official_website}\n`);
    }
  }
}

if (require.main === module) main();
