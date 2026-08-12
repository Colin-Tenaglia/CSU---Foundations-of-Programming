# EA TRACK CURRICULUM — LESSONS 1 THROUGH 18

**Tenaglia & Associates**
Phase 0: Preparer Foundations · Phase 1: One Complete Return · Ring A: Adjustments and Deductions

Reference order in every lesson: **Publication first, then Drake screen, then line items.**

---

## HOW TO USE THIS DOCUMENT

**Publication citations are by lesson name and tab letter, not page number.** Pub 4491 renumbers every year; the lesson titles do not. Pub 4012 tab letters are stable. Verify tab letters against your printed edition on first use and correct this document once.

**Drake screen codes** come from the Drake KB Federal 1040 Screen List, article 20051, last updated March 24, 2026. Verify against your installed year before this goes in front of a student.

**Screen help, every lesson:** open the screen in Drake and press **F1**, or search the screen code at kb.drakesoftware.com. F1 gives the installed year's layout, which no pasted screenshot can do.

**Line numbers** are TY2025 and live in the Figures & Lines Sheet, not in these lessons. When a line moves, one file changes.

**New for TY2025:** Schedule 1-A, Additional Deductions, Drake screen **1A**. Covers the tips, overtime, car loan interest, and senior deductions. Does not exist in older training material. See https://kb.drakesoftware.com/kb/Drake-Tax/18889.htm

**Practice returns ship with the software.** Do not create real returns while learning.

### Standing references

| Resource | Link |
|---|---|
| Federal 1040 Screen List | https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm |
| Data Entry Basics | https://kb.drakesoftware.com/kb/Drake-Tax/13109.htm |
| Creating a New Return | https://kb.drakesoftware.com/kb/Drake-Tax/10221.htm |
| Data Entry Toolbar | https://kb.drakesoftware.com/kb/Drake-Tax/14287.htm |
| Setup Options Overview | https://kb.drakesoftware.com/kb/Drake-Tax/18202.htm |
| Drake Tax Manual, TY2025 | https://www.drakesoftware.com/sharedassets/manuals/draketaxusersmanual.pdf |
| 1040, 709, 706 supplement (2024 ed., check for current) | https://www.drakesoftware.com/sharedassets/manuals/2024/individuals.pdf |
| Video tutorials | https://support.drakesoftware.com/videos/ |

### Setup options to enable for a trainee

Setup > Options > Data Entry: **W-2 wage and withholding verification** (forces re-entry of Boxes 1, 2, 16, 17; mismatches throw EF messages 5477, 5478, 5501, 5503) · **Data Entry toolbar** · **Grid data entry** on DIV, INT, 4562, dependents.

Setup > Options, calculation and view: **Always show tax computation worksheet** · **Always show reason for no EIC**.

---

# PHASE 0 — PREPARER FOUNDATIONS

Run a diagnostic before Lesson 1. Prior work covered income topics; Lessons 3, 5 and 6 were never covered at all.

---

## Lesson 1 — The 1040 Skeleton

**Read:** Pub 4491, *Filing Basics* · Pub 4012, Tab A (Who Must File)

**Objective:** Describe the seven blocks of a 1040 and name what enters each.

**Plain English.** Every return, however complicated, is the same seven moves: total the income, subtract adjustments to get AGI, subtract a deduction to get taxable income, compute the tax, subtract credits, add other taxes, subtract what was already paid. What is left is a refund or a balance due. Everything else is detail hanging off one of those seven.

**On the return.** Pull a blank 1040 and physically draw a line between each block. That marked-up form is the first page of the binder and gets referenced all year.

**Drake.**

| Screen | What it holds | Where |
|---|---|---|
| 1 | Name, address, general information | General tab |
| 2 | Dependent information | General tab |
| 3 | Additional income, Schedule 1 Part I | General tab |
| 4 | Adjustments, Schedule 1 Part II | General tab |
| 1A | Additional deductions, Schedule 1-A | Selector |
| 5 | Additional taxes and credits, Schedules 2 and 3 | General tab |

Screens 1 through 5 are the spine. Everything else attaches to them.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Total income → AGI → taxable income → tax → credits → other taxes → payments → refund or balance due.

**Golden Note.** « A tax return is seven moves in a fixed order, and every form exists to feed one of them. »

**Trap Note.** « Preparers who learn forms without learning the order can fill a form correctly and still put the result in the wrong place. »

**Homework.** Mark up a blank 1040 by block. For five forms of your choice, name which block each one feeds.

**Quiz.** Name the seven blocks in order. Which block does a W-2 feed? Which block does withholding feed, and why is it not the same one?

---

## Lesson 2 — Document Triage

**Read:** Pub 4491, *Income* overview · Pub 4012, Tab D (Income)

**Objective:** Identify the fifteen core information documents on sight and state what each reports.

**Plain English.** Clients hand over a pile. The first skill is not computation, it is sorting. Before anything is entered, you should be able to name every document, say what it reports, and notice what is missing.

**On the return.** Build the binder tabs now. One tab per document, blank form behind each.

**Drake.**

| Document | Screen | Where |
|---|---|---|
| W-2 | W2 | General tab |
| 1099-INT | INT | Selector |
| 1099-DIV | DIV | Selector |
| 1099-NEC | NEC | Selector |
| 1099-MISC | 99M | Selector |
| 1099-G | 99G | Selector |
| 1099-R | 1099 | General tab |
| 1099-B | 99B | Selector |
| 1099-K | 99K | Selector |
| SSA-1099 | SSA | General tab |
| 1098 | 1098 | Selector |
| 1095-A | 1095 | Selector |
| W-2G | W2G | Selector |
| K-1 (1065) | K1P | Selector |
| K-1 (1120-S) | K1S | Selector |

Drake also has a **DOCS** screen, the 1098 and 1099 source document guide. Show it early.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Golden Note.** « Every information document has exactly one home screen in Drake, and knowing the pairing turns data entry into transcription. »

**Trap Note.** « A 1099-MISC and a 1099-NEC look nearly identical, go to different screens, and carry different tax consequences. »

**Homework.** Given twenty mixed documents, sort into piles and name the Drake screen for each.

**Quiz.** Which screen takes a 1099-R? What is the difference between what a 1099-NEC and a 1099-MISC report?

---

## Lesson 3 — Intake and the Client Interview

**Read:** Pub 4491, *Screening and Interviewing* · Form 13614-C and its instructions

**Objective:** Conduct an intake interview using Form 13614-C and identify unresolved items before preparation begins.

**Plain English.** The return is only as good as the interview. Form 13614-C is the IRS intake sheet, it is free, and it is better than anything a firm writes from scratch. Every "unsure" answer a client circles is a question you have to ask out loud.

**On the return.** No entry happens until intake is complete and every unsure box is resolved.

**Drake.**

| Screen | Purpose |
|---|---|
| IDS | Required identification |
| USE | §7216 consent to use return information |
| CONS | §7216 consent to disclose to other firms |
| DISC | §6103(c) consent to disclose e-file information |

Using or disclosing client information without a valid consent is a §7216 problem, not a preference.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Golden Note.** « The interview happens before the software opens, and unresolved intake questions are the single largest source of wrong returns. »

**Trap Note.** « Accepting a client's characterization of a document instead of reading the document. »

**Homework.** Complete a 13614-C from a scripted client. List every follow-up question the form generated.

**Quiz.** What does §7216 govern? Name two intake answers that change which forms you will need.

---

## Lesson 4 — Filing Status

**Read:** Pub 4491, *Filing Status* · Pub 4012, Tab B

**Objective:** Determine correct filing status, including the head of household test and the married-filing-separately consequences.

**Plain English.** Status is chosen once and drives the standard deduction, the brackets, and eligibility for a long list of credits. Head of household is the one people get wrong, because it requires a qualifying person *and* paying more than half the cost of keeping up the home.

**On the return.** Status is selected before anything else because most downstream calculations depend on it.

**Drake.** Screen **1**, filing status field, General tab. Head of household due diligence is captured on **DD1**, which has a dedicated head of household section.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Filing status box, top of Form 1040. Drives standard deduction and bracket selection.

**Golden Note.** « Filing status is chosen first because nearly every number after it depends on which one you picked. »

**Trap Note.** « Assuming an unmarried parent qualifies for head of household without testing who paid more than half the cost of the home. »

**Homework.** Five fact patterns. Determine status and cite the Pub 4012 decision tree step that decided it.

**Quiz.** What two conditions must both be met for head of household? Name three things married filing separately disqualifies.

---

## Lesson 5 — Dependents

**Read:** Pub 4491, *Dependents* · Pub 4012, Tab C

**Objective:** Apply the qualifying child and qualifying relative tests and resolve tiebreakers.

**Plain English.** Two separate tests with different rules. Qualifying child is relationship, age, residency, support, and joint return. Qualifying relative is relationship or member of household, gross income, and support. When two people can claim the same child, the tiebreaker rules decide, not the taxpayers.

**On the return.** Dependents drive CTC, ODC, EITC, dependent care, education credits, and head of household. Getting this wrong contaminates the whole back half of the return.

**Drake.**

| Screen | Purpose | Where |
|---|---|---|
| 2 | Dependent information | General tab |
| 8332 | Release of claim by custodial parent | Selector |
| 2120 | Multiple support declaration | Selector |
| 8862 | Claiming credits after prior disallowance | Selector |

Grid data entry is available on the dependent screen.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Golden Note.** « Qualifying child and qualifying relative are different tests, and a person who fails one may still pass the other. »

**Trap Note.** « Entering a dependent without confirming residency months, which is what actually decides most contested claims. »

**Homework.** Six dependent scenarios including one tiebreaker and one multiple support case.

**Quiz.** List the five qualifying child tests. Who wins under the tiebreaker when a child lived with each parent equally?

---

## Lesson 6 — The Preparer's Role and Due Diligence

**Read:** Pub 4491, *Quality Review* · Circular 230 §10.22 and §10.34 · Form 8867 instructions

**Objective:** State the preparer's due diligence obligations and complete Form 8867.

**Plain English.** A PTIN is required to prepare for compensation. Circular 230 sets the conduct standard. Form 8867 is required when claiming EITC, CTC/ACTC/ODC, AOTC, or head of household, and the §6695(g) penalty applies per credit, per return. This is not paperwork, it is the difference between a return and a liability.

**On the return.** Due diligence runs alongside preparation, not after it.

**Drake.**

| Screen | Purpose |
|---|---|
| 8867 | Paid preparer's due diligence checklist |
| 8867 > Due Diligence Assist link | Guided completion |
| 8867 > Overrides tab | Overrides |
| DD1 | Due diligence questions, includes head of household |
| DD2 | Additional due diligence |
| PIN | Form 8879 e-file signature authorization |
| EF | Federal and state EF selections |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Golden Note.** « Due diligence is a per-credit obligation with a per-credit penalty, and the documentation requirement is separate from getting the answer right. »

**Trap Note.** « Completing 8867 at the end as a formality rather than letting it drive the questions asked during intake. »

**Homework.** Complete an 8867 for a return claiming EITC and CTC. Identify what documentation the file needs.

**Quiz.** Which four items trigger 8867? What is the §6695(g) penalty structure?

---

## Lesson 6S — Software Orientation

**Read:** KB 10221 (Creating a New Return) · KB 13109 (Data Entry Basics) · KB 14287 (Data Entry Toolbar)
https://kb.drakesoftware.com/kb/Drake-Tax/10221.htm
https://kb.drakesoftware.com/kb/Drake-Tax/13109.htm
https://kb.drakesoftware.com/kb/Drake-Tax/14287.htm

**Objective:** Navigate Drake data entry without knowing any tax yet.

No tax content in this lesson. It exists because a trainee fighting the interface cannot think about the return.

**Where screens live.** Screens 1 through 5 are the spine and sit on the **General tab**, along with W2, 1099, SSA, A, 2106 and 2441. Every other screen is reached by typing its code into the selector field at the bottom of any data entry screen. A **highlighted tab** means at least one screen on that tab has been completed, which is the fastest read on what a return already contains.

**Movement.**

| Action | Result |
|---|---|
| Page Up / Page Down | Between multiple instances of the same screen, such as several W2s |
| Next, single instance | Moves to the connected screen: 3 → 4 → 5 |
| Previous | Back to the linked prior screen |
| CTRL+V | Calculate and view |
| CTRL+E | Return to data entry |
| CTRL+W | Open the detail worksheet on the current field |
| CTRL+F | Skip past a field refusing an unsupported code |

**Field mechanics.** A field shaded red generally means a detail worksheet exists behind it. Override and adjustment fields change the program's calculation: positive increases, negative decreases. The **F** box excludes an item from the federal return, with 0 suppressing it entirely, used when data should reach a state return but not the federal. The **ST** dropdown assigns the entry to a state and can generate a state return.

**LookBack.** PY Fields and PY Data show which fields on the open screen had prior-year data and what it was. For a trainee this is the most useful button in the program, because it shows what a competent preparer entered on the same screen last year.

**Golden Note.** « Screens 1 through 5 are the spine, everything else is typed into the selector box, and a highlighted tab tells you what the return already contains. »

**Trap Note.** « Using an override field to force a number instead of finding the entry that produced the wrong one. »

**Homework.** Open a practice return. Visit every screen named in Lessons 1 through 12 without using a mouse for navigation. Find one red-shaded field and open its worksheet.

---

### GATE 0
Sorts twenty mixed documents cold. Correct status and dependents on three fact patterns, unprompted. Completes a 13614-C and names every follow-up question it raises. Navigates Drake without hunting.

---

# PHASE 1 — ONE COMPLETE RETURN

The point of this phase is a finished return, not coverage. Do not let it expand.

---

## Lesson 7 — W-2 Wages

**Read:** Pub 4491, *Income – Wages, Interest, Etc.* · Pub 4012, Tab D

**Objective:** Read every box of a W-2 and identify which boxes affect the return.

**Plain English.** Box 1 is wages. Box 2 is what was already paid in. But Box 12 codes carry retirement contributions, HSA contributions, and deferred comp, and Box 13 checkboxes change IRA deductibility. The boxes people ignore are the ones that change later lessons.

**On the return.** Wages to the income block. Withholding to the payments block. Two different blocks, routinely conflated.

**Drake.**

| Screen | Purpose |
|---|---|
| W2 | Primary entry, one screen per W-2, General tab |
| W2 > Additional Entries | Overflow for many Box 12 codes |
| 4852 | Substitute W-2 when one is missing |
| 8919 | Uncollected SS/Medicare, misclassification |

Turn on wage verification for a trainee. It catches transposition immediately:
https://kb.drakesoftware.com/kb/Drake-Tax/10932.htm
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Box 1 → 1040 line 1a. Box 2 → federal withholding, payments block. Box 12 code W → Form 8889. Box 13 retirement box → affects the IRA deduction in Lesson 15.

**Golden Note.** « Box 1 and Box 2 land in different blocks of the return, and the Box 12 and 13 entries quietly control forms you have not opened yet. »

**Trap Note.** « Entering Box 1 and Box 2 and skipping the rest, which silently breaks the HSA and IRA calculations later. »

**Homework.** Enter three W-2s including one with Box 12 codes D, W and DD. Explain what each code does and does not do.

**Quiz.** What does Box 12 code W represent and which form does it trigger? Why does the Box 13 retirement checkbox matter?

---

## Lesson 8 — Interest and Dividends

**Read:** Pub 4491, *Income – Wages, Interest, Etc.* · Pub 4012, Tab D

**Objective:** Enter interest and dividend income and state when Schedule B is required.

**Plain English.** Interest is generally taxable, with municipal interest as the main exception and savings bonds used for education as a narrower one. Dividends split into ordinary and qualified, and qualified dividends get capital gains rates, which is why the split matters more than the total.

**On the return.** Schedule B is required above the threshold or when a foreign account question applies. The Schedule B Part III foreign account question is the entry point to FBAR and gets missed constantly.

**Drake.**

| Screen | Purpose |
|---|---|
| INT | 1099-INT entry |
| B | Schedule B, including Part III foreign account questions |
| DIV | 1099-DIV entry |
| 8815 | Savings bond interest exclusion |
| 8814 | Parent's election to report child's interest and dividends |

INT and DIV both support grid data entry, faster for brokerage statements with many payers.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Taxable interest and tax-exempt interest → separate 1040 lines. Ordinary and qualified dividends → separate 1040 lines. Qualified dividends feed the capital gains worksheet in Lesson 10.

**Golden Note.** « Tax-exempt interest still gets reported, because it affects the Social Security calculation and other phaseouts even though it is not taxed. »

**Trap Note.** « Entering total dividends without splitting out the qualified portion, which overstates the tax. »

**Homework.** Enter a brokerage 1099 composite containing interest, ordinary and qualified dividends, and tax-exempt interest.

**Quiz.** When is Schedule B required? Why does tax-exempt interest still appear on the return?

---

## Lesson 9 — Standard Deduction

**Read:** Pub 4491, *Standard Deduction and Tax Computation* · Pub 4012, Tab F

**Objective:** Determine the correct standard deduction, including additional amounts, and state when itemizing is considered.

**Plain English.** Everyone gets a deduction. The standard amount depends on filing status, with additional amounts for age 65 and over and for blindness. You itemize only when itemized deductions exceed it. Most returns take the standard deduction, which is why Lesson 17 comes later than a beginner expects.

**On the return.** Automatic in Drake once status, age and blindness are entered. Not something the preparer types.

**Drake.** Screen **1** carries date of birth and the blindness indicators that drive the additional amounts. Screen **A** is opened only when itemizing is actually in play.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Standard or itemized deduction → 1040 deduction line. AGI minus this equals taxable income.

**Golden Note.** « The standard deduction is calculated from information already on screen 1, so entering the birthdate correctly is a deduction issue, not a demographics issue. »

**Trap Note.** « Opening screen A out of habit and producing an itemized return that costs the client money. »

**Homework.** Four taxpayers of varying status and age. State the deduction and what on screen 1 produced it.

**Quiz.** What two conditions produce an additional standard deduction amount? Where are they entered in Drake?

---

## Lesson 10 — Tax Computation

**Read:** Pub 4491, *Standard Deduction and Tax Computation* · Tax table and tax computation worksheet

**Objective:** Compute tax from taxable income and distinguish marginal from effective rate.

**Plain English.** Brackets are marginal. Only the income inside a bracket is taxed at that bracket's rate. Clients believe otherwise almost universally, and explaining it clearly is a client-facing skill, not just a technical one. Qualified dividends and long-term gains are taxed on a separate worksheet at their own rates.

**On the return.** Drake computes this. The preparer's job is to know whether the number is plausible and to explain it.

**Drake.** No direct entry screen. Setup > Options has **Always show tax computation worksheet**. Turn it on during training so he sees the computation rather than a black box.
https://kb.drakesoftware.com/kb/Drake-Tax/18202.htm

**Line items.** Taxable income → tax. Watch for the capital gains worksheet substituting for the tax table when qualified dividends or long-term gains are present.

**Golden Note.** « A bracket applies only to the income inside it, and the effective rate is always lower than the marginal rate. »

**Trap Note.** « Telling a client a raise "put them in a higher bracket" as though all their income reprices. »

**Homework.** Compute tax by hand for three taxpayers, then verify in Drake. Explain any difference.

**Quiz.** For a given MFJ taxable income: what is the marginal rate and what is the effective rate? Why can they differ so much?

---

## Lesson 11 — Child Tax Credit and Schedule 8812

**Read:** Pub 4491, *Child Tax Credit* · Pub 4012, Tabs G and H

**Objective:** Apply CTC, ODC and the additional child tax credit, and distinguish refundable from nonrefundable.

**Plain English.** A nonrefundable credit can reduce tax to zero and no further. A refundable credit can produce a refund beyond what was paid in. CTC is partly each: the nonrefundable portion offsets tax, and the additional child tax credit is the refundable remainder. Other dependent credit covers dependents who fail the CTC age or SSN test.

**On the return.** Dependents entered in Lesson 5 drive this entirely. If Lesson 5 was wrong, this is wrong.

**Drake.**

| Screen | Purpose |
|---|---|
| 2 | Dependents, drives eligibility |
| 8812 | Schedule 8812 |
| 8867 / DD1 | Required due diligence |
| 8862 | If credits were previously disallowed |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Nonrefundable CTC and ODC → credits block. Additional child tax credit → payments block, because refundable credits behave like payments.

**Golden Note.** « Refundable credits sit in the payments block and nonrefundable credits sit in the credits block, and that placement is the entire difference between them. »

**Trap Note.** « Missing that a dependent with an ITIN rather than an SSN gets ODC, not CTC. »

**Homework.** Three families. Compute CTC, ODC and ACTC and state which block each lands in.

**Quiz.** What SSN condition does CTC require? Which part of the child tax credit is refundable?

---

## Lesson 12 — Payments, Refund, and Quality Review

**Read:** Pub 4491, *Finishing the Return* · Pub 4012, Tab K

**Objective:** Complete the payments block and hand off a return that is finished and reviewed.

**Plain English.** Withholding, estimated payments and refundable credits all sit in the payments block. Subtract total tax from total payments and the sign of the answer is the refund or the balance due. Then the return has to be complete and correct enough to hand to the preparer who signs it.

**On the return.** You do not transmit. You do not complete the PIN screen and you do not make EF selections — the signing preparer does that. What you do is run View, read every EF message, and either clear it or flag it. Those messages are how Drake reports that something is wrong, and handing over a return with unread messages is the fastest way to lose a reviewer's trust. Direct deposit details, payment setup and estimated vouchers still get entered, because the signing preparer needs them present and correct.

**Drake.**

| Screen | Purpose |
|---|---|
| DD | Direct deposit information |
| 8888 | Refund allocation across accounts |
| PMT | Electronic funds withdrawal for balance due |
| ES | Estimated payments made and next-year vouchers |
| PIN | Form 8879 signature authorization |
| EF | Federal and state EF selections |
| 9465 | Installment agreement request |

CTRL+V calculates and views. CTRL+E returns to data entry.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Total payments minus total tax. Positive is a refund, negative is a balance due.

**Golden Note.** « Total payments minus total tax is the last arithmetic on the return, and everything before it exists to make those two numbers right. »

**Trap Note.** « Handing off a return without running View and reading the EF messages, which is where Drake tells you what is wrong. »

**Homework.** Finish a return end to end including direct deposit and 8879.

**Quiz.** Name three things that sit in the payments block. What must you check before handing a return to the signing preparer?

---

### RETURN LAB 1
Same return twice: once by hand on paper forms, once in Drake. Compare line by line and explain every difference.

### GATE 1
Two W-2s, interest income, standard deduction, one qualifying child. Unassisted. Under 45 minutes. Zero critical errors.

**Do not advance past this gate.** A student who has not completed a return has nothing to attach Ring A to.

---

# RING A — ADJUSTMENTS AND DEDUCTIONS

Resume the Schedule 1 work here, in its proper place.

---

## Lesson 13 — What an Adjustment Is

**Read:** Pub 4491, *Adjustments to Income* · Pub 4012, Tab E

**Objective:** Explain why an above-the-line adjustment is worth more than an itemized deduction.

**Plain English.** Adjustments come out before AGI. Itemized deductions come out after. Because AGI drives phaseouts for credits, deductions and taxable Social Security, a dollar of adjustment can be worth more than a dollar of itemized deduction. Adjustments also help everyone, while itemized deductions help only those who exceed the standard deduction.

**On the return.** Schedule 1 Part II. New for TY2025, Schedule 1-A carries a separate set of additional deductions.

**Drake.**

| Screen | Purpose |
|---|---|
| 4 | Adjustments, Schedule 1 Part II, General tab |
| 1A | Additional deductions, Schedule 1-A, new for TY2025 |
| 3 | Additional income, Schedule 1 Part I, already covered |

Most Schedule 1 entries come from screens 3 and 4, but data also flows in from 99G, 4797, E, K1P, K1S and K1F.
Schedule 1-A background: https://kb.drakesoftware.com/kb/Drake-Tax/18889.htm
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Total income minus Schedule 1 Part II adjustments equals AGI. AGI then governs nearly every phaseout on the return.

**Golden Note.** « Adjustments reduce AGI itself, so they reduce tax twice: directly, and by loosening every phaseout that AGI controls. »

**Trap Note.** « Treating adjustments and itemized deductions as interchangeable because both reduce taxable income. »

**Homework.** For one taxpayer, model a $2,000 adjustment against a $2,000 itemized deduction and quantify the difference.

**Quiz.** Why is an adjustment generally worth more than a deduction of equal size? Which Drake screen holds Schedule 1-A?

---

## Lesson 14 — Educator, HSA, and Self-Employed Health Insurance

**Read:** Pub 4491, *Adjustments to Income* · Pub 4012, Tab E

**Objective:** Apply the educator expense, HSA and self-employed health insurance adjustments.

**Plain English.** Three unrelated adjustments grouped because they sit together. Educator expenses are capped and require an hours test. The HSA deduction requires high deductible coverage and interacts with any employer contribution already in W-2 Box 12 code W. Self-employed health insurance is limited to the net profit of the business.

**On the return.** The HSA adjustment is only half of Form 8889. The distribution side comes in Lesson 35.

**Drake.**

| Screen | Purpose |
|---|---|
| 4 | Educator expenses |
| 8889 | HSA, contribution and deduction |
| HSA | HSA supporting entries |
| SEHI | Form 7206, self-employed health insurance |
| LTC | Long-term care premiums |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Each flows to its own Schedule 1 Part II line, then into total adjustments.

**Golden Note.** « The HSA deduction and the W-2 Box 12 code W amount are two different things, and entering both as contributions double counts. »

**Trap Note.** « Deducting self-employed health insurance in excess of the business's net profit. »

**Homework.** A teacher with classroom expenses, an HSA with both employer and personal contributions, and a Schedule C filer with premiums.

**Quiz.** What limits the self-employed health insurance deduction? Where does the employer HSA contribution appear before it reaches Form 8889?

---

## Lesson 15 — IRA Deduction

**Read:** Pub 4491, *Adjustments to Income* · Pub 4012, Tab E · Pub 590-A

**Objective:** Determine deductibility of a traditional IRA contribution including coverage and phaseout rules.

**Plain English.** Anyone with earned income can contribute. Whether it is deductible depends on whether the taxpayer or spouse is covered by a workplace plan, and on MAGI against a phaseout range. This is where the W-2 Box 13 retirement checkbox from Lesson 7 comes back and decides the answer.

**On the return.** Deductible contributions are an adjustment. Nondeductible contributions create basis and require Form 8606, which is Lesson 26.

**Drake.**

| Screen | Purpose |
|---|---|
| 4 | IRA deduction entry |
| 8606 | Nondeductible contributions and basis |
| ROTH | Roth contributions and conversions |
| 8880 | Saver's credit, which the same contribution may also generate |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Deductible IRA → Schedule 1 Part II. Nondeductible → Form 8606 Part I, no current deduction, basis carries forward.

**Golden Note.** « The W-2 Box 13 retirement checkbox decides whether an IRA contribution is deductible, which is why Lesson 7 said not to skip it. »

**Trap Note.** « Failing to file Form 8606 for a nondeductible contribution, which loses the basis and causes the client to be taxed twice years later. »

**Homework.** Four taxpayers varying by coverage, filing status and MAGI. Determine deductible amount and any 8606 requirement.

**Quiz.** What two facts determine deductibility? What happens if a nondeductible contribution is never reported on 8606?

---

## Lesson 16 — Student Loan Interest

**Read:** Pub 4491, *Adjustments to Income* · Pub 4012, Tab E · Form 1098-E

**Objective:** Apply the student loan interest deduction and its limits.

**Plain English.** Capped, phased out by MAGI, and unavailable to married filing separately. The loan must have been taken for qualified education expenses of the taxpayer, spouse, or a dependent at the time the debt was incurred. The person legally obligated on the loan is the one who deducts it, which is not always the person paying.

**On the return.** An adjustment, so it helps regardless of whether the client itemizes.

**Drake.** Screen **4**, student loan interest field, General tab. Source document is Form 1098-E.
Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Schedule 1 Part II, subject to the cap and the MAGI phaseout.

**Golden Note.** « The deduction belongs to the person legally obligated on the loan, not necessarily the person who wrote the check. »

**Trap Note.** « Claiming it for a client filing married filing separately, where it is disallowed outright. »

**Homework.** Three scenarios including a parent paying a non-dependent child's loan.

**Quiz.** Who may claim the deduction when a parent pays a former dependent's loan? What filing status disqualifies it entirely?

---

## Lesson 17 — Schedule A: Medical, Taxes, Interest

**Read:** Pub 4491, *Itemized Deductions* · Pub 4012, Tab F

**Objective:** Compute the medical floor, apply the SALT cap, and deduct qualified mortgage interest.

**Plain English.** Medical expenses are deductible only above a percentage-of-AGI floor, which is why they rarely help. State and local taxes are capped, and the client chooses income tax or sales tax, whichever is larger. Mortgage interest is limited by acquisition debt, and home equity interest only counts if the loan was used to buy, build or substantially improve the home.

**On the return.** Only matters if the total will exceed the standard deduction. Check that first.

**Drake.**

| Screen | Purpose |
|---|---|
| A | Schedule A, General tab |
| 1098 | Mortgage interest statement |
| STAX | Sales tax deduction worksheet |
| LTC | Long-term care premiums, medical section |
| 4952 | Investment interest expense |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Medical above the AGI floor. SALT to the cap. Mortgage interest subject to acquisition debt limits.

**Golden Note.** « Run the standard deduction comparison before entering anything on screen A, or you will spend an hour producing a number the client cannot use. »

**Trap Note.** « Deducting home equity interest without confirming the proceeds were used on the home itself. »

**Homework.** A taxpayer with medical expenses, property tax, state income tax and mortgage interest. Determine whether to itemize.

**Quiz.** What is the medical floor and how is it calculated? What are the two SALT options and how do you choose?

---

## Lesson 18 — Schedule A: Charitable and the Itemize Decision

**Read:** Pub 4491, *Itemized Deductions* · Pub 4012, Tab F · Pub 526

**Objective:** Apply charitable limits and substantiation rules, and make the itemize versus standard decision.

**Plain English.** Cash contributions are limited by a percentage of AGI, with a lower limit for appreciated property. Substantiation is the real issue: written acknowledgment is required at a threshold, noncash above a threshold needs Form 8283, and above a higher threshold needs a qualified appraisal. No receipt, no deduction, regardless of whether the gift happened.

**On the return.** Closes Ring A. Excess contributions carry forward and the carryover has to be tracked year to year.

**Drake.**

| Screen | Purpose |
|---|---|
| A | Schedule A, contributions section |
| A > Charitable Contributions Carried over from prior years | Carryover in |
| A > carryover link > Charitable Contributions Carryover for Future | Carryover out |
| 8283 | Noncash contributions |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Line items.** Contributions subject to AGI percentage limits, excess carried forward.

**Golden Note.** « Charitable deductions fail on substantiation far more often than on the limits, and the substantiation requirement rises in steps as the gift grows. »

**Trap Note.** « Losing a carryover between years because it was never entered on the carryover screen. »

**Homework.** A taxpayer with cash gifts, a noncash donation above the 8283 threshold, and a prior-year carryover.

**Quiz.** At what point is a written acknowledgment required? What triggers Form 8283, and what triggers a qualified appraisal?

---

### RETURN LAB 2
Full return: two W-2s, interest and dividends, IRA contribution, student loan interest, and itemized deductions that must be compared against the standard deduction.

### GATE A
Decides itemize versus standard without prompting. Completes Schedule 1 Part II and Schedule A with carryovers tracked.

---

## STILL TO BUILD

Lessons 19 through 40: self-employment, retirement and Social Security, investments and basis, family and education credits, rentals and K-1s, estimated tax and amended returns. Then Phase 3, the EA Part 1 conversion.

## BEFORE THIS GOES TO A STUDENT

1. Verify Pub 4012 tab letters against the printed edition and correct once here.
2. Verify Drake screen codes against the installed year. The source list is dated March 24, 2026.
3. Build the Figures & Lines Sheet. Every capped, floored or phased-out amount referenced above lives there, not in these lessons.
4. Confirm Schedule 1-A content and screen 1A behavior in the installed software, since it is new.
5. Replace the 2024 1040 supplement link with the current-year edition when available.
