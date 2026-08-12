# EA Track Workbook — Handoff Brief

**Purpose:** move the curriculum out of hand-deployed single-file HTML and into a maintained repository.

**Current state:** two independent Vercel projects, each a single self-contained `index.html` with inlined CSS, data and render script.

| Part | URL | Status |
|---|---|---|
| Part 1 — Lessons 1–18 | ea-track-workbook-tenaglc-6552s-projects.vercel.app | Live. Old lesson copy. Cross-link to Part 2 is broken. |
| Part 2 — OBBBA, Energy, SS, Wisconsin | ea-track-part2-tenaglc-6552s-projects.vercel.app | Live. Rewritten copy, collapsible, correct cross-link. |

---

## 1. Why it needs to move

Three constraints made the current form untenable:

1. **Whole-tree deploys.** Every deployment replaces all files, so touching one lesson means re-sending the entire corpus. This is what forced the split into two projects.
2. **Content and presentation are fused.** Lesson prose lives inside a JavaScript array inside an HTML file. Non-technical editing is impossible and diffs are unreadable.
3. **Annual rot.** Tax figures, Drake screen codes and Wisconsin conformity all change each year. There is no update path that does not involve editing markup.

The target is a repo where a lesson is a file, figures are config, and a build produces the site.

---

## 2. Content model

The lesson object as currently used. This is the schema to formalize.

```ts
type Lesson = {
  id: string;            // stable anchor, e.g. "l7", "w3"
  n: string;             // display number: "7", "6S", "13A", "W1"
  title: string;
  part: 1 | 2;
  section: string;       // "Phase 0" | "Phase 1" | "Ring A" | "Federal" | "Wisconsin"
  attach?: string;       // "Attaches to Lesson 9" — Part 2 only
  wisconsin?: boolean;   // drives the blue treatment

  read: string;          // publication citations, may contain <em>
  objective: string;
  summary: string;       // diagnostic prose, ~120–180 words
  onReturn?: string;
  look: string[];        // "What to look for" — 5–9 items
  detail?: [string, string][];  // label / explanation pairs

  screens: Screen[];
  screenNote?: string;
  lands?: string;        // where it lands on the return

  refs: Ref[];
  golden: string;
  homework: string;
  quiz: string;
};

type Screen = {
  code: string;          // "1A", "8867", "WI screen 3"
  purpose: string;
  where: string;         // "General tab" | "Selector" | "WI General tab"
  verified: boolean;     // false renders a caution marker
};

type Ref = {
  label: string;         // "KB 18890 — Schedule 1-A: Additional Deductions"
  url: string;
  kind: "drake" | "irs" | "wi" | "other";
  lastChecked: string;   // ISO date
};
```

**Gates and dividers** are separate node types in the same ordered array:

```ts
type Gate = { kind: "gate"; label: string; hard: boolean; text: string };
type Divider = { kind: "divider"; label: string; note: string; wisconsin?: boolean };
```

---

## 3. Figures as configuration

This is the single most important architectural decision. **No amount appears in lesson prose.** Every cap, floor, threshold and phaseout lives in one config module keyed by tax year.

```ts
// figures/2025.ts
export default {
  year: 2025,
  federal: {
    ctc: 2200,
    saltCap: 40000,
    saltPhasedownRate: 0.30,
    saltPhasedownThreshold: 500000,
    seniorDeduction: 6000,
    section179Limit: 2500000,
    section179PhaseoutStart: 4000000,
    scheduleBThreshold: 1500,
    mortgageAcquisitionDebt: 750000,
    mortgageAcquisitionDebtMFS: 375000,
    standardDeduction: null,        // TODO
    medicalFloorPct: null,          // TODO
    // ...
  },
  wisconsin: {
    ircConformityDate: "2022-12-31",
    capitalGainTaxablePct: 0.70,
    capitalGainTaxablePctFarm: 0.40,
    tuitionSubtraction: 7649,
    collegeSavings: 5130,
    collegeSavingsMFS: 2560,
    adoptionSubtraction: 15000,
    marriedCoupleCreditRate: 0.03,
    marriedCoupleCreditIncomeCap: 16000,
    lateFilingFee: 50,
    standardDeductionTable: null,   // TODO
    itemizedDeductionCreditRate: null, // TODO
  },
  sunsets: {
    section25C: "2025-12-31",
    section25D: "2025-12-31",
    cleanVehicle: "2025-09-30",
    schedule1A: "2028-12-31",
  }
};
```

Nulls render as a visible "needs filling" marker rather than failing silently. The Figures page is generated from this module, not hand-written.

**Rollover process each year:** copy `figures/2025.ts` to `figures/2026.ts`, null everything that changes, fill from current instructions, flip the active year. Lessons are untouched.

---

## 4. Proposed stack

Matching the existing suite so this is one more app rather than a one-off.

- **Vite + React + TypeScript**
- **Tailwind** with the palette below as tokens
- **shadcn/ui** — `Accordion` replaces the hand-rolled `<details>`, `Command` for the filter, `Checkbox` for progress
- **Content as MDX or JSON** in `content/lessons/`, one file per lesson, loaded at build time
- **Static build**, no server, no API. Consistent with the client-side-only posture across the suite.

### Design tokens

```
paper   #EDEEE8    page background
form    #E3E6DC    rail, section dividers
ink     #14150F    text, disclosure block
rule    #B4B9A8    borders
mute    #5C6152    secondary text
mark    #8C2A11    links, traps, hard gates
tab     #2E4739    accents, soft gates
wi      #1B3A5C    Wisconsin treatment
white   #FAFAF7    cards
gold    #A8842B    golden note rule
```

Type: system sans for body, system mono for screen codes and labels. Screen codes are set in mono deliberately — they are codes, and the monospace treatment is doing semantic work.

### Routes

```
/                     Part 1 index
/lesson/:id           deep link, opens that lesson
/part2                Part 2 index
/figures              Figures & Lines Sheet
/disclosure           full disclosure
/screens              generated screen-code index (see §6)
```

---

## 5. Progress and storage

Currently `localStorage` under key `ea-track-progress`, a flat `{ [lessonId]: boolean }`.

Keep it client-side. No accounts, no server, consistent with firm posture. If multi-student tracking is ever needed, that is a separate decision with real privacy implications — do not add it casually.

Add: export and import progress as JSON, so a student can move machines.

---

## 6. Things worth building that do not exist yet

**Screen-code index.** Generate a page from all `Screen` entries across every lesson: code, purpose, which lessons use it, verified status. Becomes the reference the student actually keeps open, and surfaces unverified codes in one list.

**Verification report.** Build-time check that flags refs with `lastChecked` older than N months and screens with `verified: false`. Prints to console on build.

**Figures diff.** When a new year's figures module is added, generate a changed-values report. That report is the annual update checklist.

---

## 7. Content inventory to port

| Item | Count | Notes |
|---|---|---|
| Part 1 lessons | 19 | Includes 6S Software Orientation. **Still on old copy — needs the summary + look rewrite.** |
| Part 2 lessons | 11 | Already rewritten to current standard. Port these first as the reference implementation. |
| Gates | 6 | Gate 0, Return Lab 1, Gate 1, Return Lab 2, Gate A, plus Part 2 has none |
| Dividers | 5 | Phase 0, Phase 1, Ring A, Federal OBBBA, Wisconsin |
| Drake KB refs | ~55 | All verified reachable. Wisconsin screen refs verified against KB 20050 / 14923 / 11573 / 10817. |
| Figures rows | ~48 | 3 still null — see §8.2 |
| Lessons not yet written | 22 | Rings B–F (19–40) and Wisconsin W6–W8 |

---

## 8. Open items

1. **Part 1 rewrite** — 19 lessons still carry the original copy. The Part 2 lessons are the style reference.
2. **Null figures — resolved down to three.** Filled from Rev. Proc. 2024-40, the Schedule 1-A instructions, and 2025 Wis. Act 15: federal standard deduction and the 65/blind additions, dependent standard deduction, medical floor, IRA limit and all three deduction phaseout ranges, HSA limits and HDHP qualification, student loan cap and phaseout, charitable substantiation and AGI limits, qualifying relative gross income limit, tips and overtime caps, all four Schedule 1-A MAGI phaseouts, the Wisconsin standard deduction maxima, the itemized deduction credit rate (5%), and the Wisconsin single/HOH bracket schedule including the Act 15 second-bracket expansion.

   Still null, and deliberately so: (a) the full federal bracket schedule — read it off the tax table rather than duplicating it here, which is the same "links out, never copy in" rule in §9; (b) the educator expense cap, almost certainly still $300 but not separately confirmed for 2025; (c) the Wisconsin MFJ and MFS 5.30%/7.65% boundaries.
3. **Pub 4012 tab letters** — cited as A through K throughout; needs one pass against the printed edition.
4. **Wisconsin screen codes** — screens 1, 2, 3 and OPT verified. Anything beyond those is inferred from form names and should be confirmed in the installed program.
5. **1040 supplement link** — currently points at the 2024 edition; replace when the current-year PDF is published.
6. **Deployment protection** — confirm whether the Vercel projects require login. Open one in a private window.
7. **Domain** — these belong on tenaglia.tax rather than vercel.app if this becomes a standing firm asset.

---

## 9. Constraints to preserve

- **Client-side only.** No server storage, no client data, no accounts.
- **Not authority.** The disclosure is load-bearing and must survive the port, on every entry point.
- **Links out, never copy in.** Drake screenshots and publication text stay on their own sites. The links are the feature; a pasted screenshot is stale by October.
- **Verification status is visible.** Unverified screen codes are marked as such in the UI, not silently presented as fact.
