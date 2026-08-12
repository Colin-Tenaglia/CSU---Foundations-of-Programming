# FORM 1040 PREPARATION GUIDE — TAX YEAR 2025

**Tenaglia & Associates · Individual Returns**

A working guide to preparing a complete individual income tax return, in preparation order, with the governing IRS publication, the Drake Tax data entry path, the affected form lines, and the failure modes for each section.

Reference order in every section: **Publication → return line → Drake screen → field-level detail.**

---

# HOW TO USE THIS DOCUMENT

**This is a preparation guide, not a course.** It follows the return from the top of page 1 to the signature block. Work it in order the first few times. After that, use the section index and Appendix A (document → screen map) as a desk reference.

**Publication citations are by document and topic name, not page number.** Pub 4491 and Pub 17 renumber pages every year; chapter and lesson titles are stable. Pub 4012 tab letters are stable but should be checked once against your printed edition.

**Every section ends with a quiz.** Answers are in Appendix G. The quizzes test the two things that actually go wrong in practice: knowing which fact controls the outcome, and knowing where that fact is entered.

**Drake screen codes** are given as `SCREEN` in bold caps. Codes marked **†** are the ones still unconfirmed against a Drake source; everything unmarked has been checked against the Drake knowledge base. Confirm any screen by pressing **F1** inside it, or by searching the code in the Federal 1040 Screen List (KB 20051). Drake adds, splits, and retires screens between versions, so a dagger is a prompt to verify, not a claim that the screen does not exist.

**Screen help, always:** open the screen in Drake and press **F1**. F1 returns the installed year's layout and field help. No document, including this one, can do that.

**Dollar figures are TY2025** and are collected in Appendix C. Where a figure appears in the body, it is repeated from Appendix C for readability. When a figure changes, Appendix C is the only place that has to be edited.

**New for TY2025 — read this before anything else.** The One Big Beautiful Bill Act (OBBBA, enacted July 2025) changed the individual return more than any year since 2018. The changes that touch nearly every return:

| Change | Where it lands | Section |
|---|---|---|
| **Schedule 1-A**, a new form: qualified tips, qualified overtime, car loan interest, senior deduction | Form 1040 line 13b | Part 7 |
| SALT cap raised to $40,000 with an income phase-down | Schedule A | 8.3 |
| Standard deduction increased above the ordinary inflation step | Form 1040 line 12 | 8.1 |
| Child tax credit raised to $2,200; SSN now required for the *taxpayer* | Schedule 8812 | 11.2 |
| QBI deduction made permanent | Form 8995 / 8995-A | Part 9 |
| 100% bonus depreciation restored; §179 cap raised | Schedule C, E, F | 5.8 |
| Energy and clean vehicle credits terminated during 2025 | Schedule 3 | 11.7 |
| 1099-K reporting threshold restored to $20,000 / 200 transactions | Schedule C, 1 | 5.13 |

Training material written before mid-2025 does not contain any of this. Treat any pre-2025 checklist as suspect until reconciled against Part 7 and Appendix C.

**Practice returns ship with the software.** Do not learn on live client data.

---

### Standing references

**IRS**

| Resource | Use |
|---|---|
| Pub 17, *Your Federal Income Tax* | The comprehensive individual return reference. Start here when a question is substantive rather than procedural. |
| Pub 4012, *Volunteer Resource Guide* | Decision trees and charts. Fastest path to a defensible answer on status, dependents, and credits. |
| Pub 4491, *VITA/TCE Training Guide* | Topic-by-topic training text, organized like a return. |
| Instructions for Form 1040 | Line-by-line authority. The final word on what goes on a line. |
| irs.gov/forms-pubs | Current-year forms, instructions, and prior-year archive. |
| irs.gov/e-file-providers/quick-alerts | E-file outages, schema changes, form availability. |

**Topic publications, cited in the section that needs them**

Pub 501 (status, dependents, standard deduction) · Pub 502 (medical) · Pub 503 (dependent care) · Pub 505 (withholding and estimated tax) · Pub 523 (home sale) · Pub 526 (charitable) · Pub 527 (rental) · Pub 529 (miscellaneous deductions) · Pub 535 / Pub 334 (business expenses, small business) · Pub 550 (investment income and expenses) · Pub 551 (basis) · Pub 559 (survivors and decedents) · Pub 590-A and 590-B (IRA contributions, IRA distributions) · Pub 596 (EITC) · Pub 915 (Social Security) · Pub 936 (mortgage interest) · Pub 946 (depreciation) · Pub 970 (education) · Pub 972 successor material in the Schedule 8812 instructions (child tax credit) · Pub 974 (premium tax credit) · Circular 230 (practice before the IRS).

**Drake**

| Resource | Link |
|---|---|
| Federal 1040 Screen List | https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm |
| Data Entry Basics | https://kb.drakesoftware.com/kb/Drake-Tax/13109.htm |
| Creating a New Return | https://kb.drakesoftware.com/kb/Drake-Tax/10221.htm |
| Data Entry Toolbar | https://kb.drakesoftware.com/kb/Drake-Tax/14287.htm |
| Setup Options Overview | https://kb.drakesoftware.com/kb/Drake-Tax/18202.htm |
| Schedule 1-A (TY2025) | https://kb.drakesoftware.com/kb/Drake-Tax/18889.htm |
| W-2 wage verification | https://kb.drakesoftware.com/kb/Drake-Tax/10932.htm |
| 2025 Changes for Form 1040 and Related Schedules | https://kb.drakesoftware.com/kb/Drake-Tax/18910.htm |
| Schedule 1-A: Additional Deductions (TY2025) | https://kb.drakesoftware.com/kb/Drake-Tax/18890.htm |
| Guide to 1098 and 1099 Informational Returns | https://kb.drakesoftware.com/kb/Drake-Tax/11742.htm |
| Drake Tax Manual | https://www.drakesoftware.com/sharedassets/manuals/draketaxusersmanual.pdf |
| Drake 101 — Data Entry (PDF) | https://kb.drakesoftware.com/kb/Resources/PDFs-Finished/Drake_101_Data_Entry.pdf |
| Video tutorials | https://support.drakesoftware.com/videos/ |

**Per-section KB articles are collected in Appendix H**, indexed to the guide section they support. All KB URLs follow the pattern `https://kb.drakesoftware.com/kb/Drake-Tax/<number>.htm`, so an article number is a complete reference. Article numbers are stable across years; their content is revised annually, so read them against the installed version.

---

# PART 0 — SETUP BEFORE THE FIRST RETURN

### 0.1 Software options to set once

**Setup > Options > Data Entry**

| Option | Why |
|---|---|
| W-2 wage and withholding verification | Forces re-entry of Boxes 1, 2, 16, 17. Mismatches throw EF messages (5477, 5478, 5501, 5503†) before the return is transmitted. Catches transposition, which is the single most common data entry error. |
| Data Entry toolbar | Puts calculate, view, split, and help within reach without menu diving. |
| Grid data entry on DIV, INT, 4562, and dependents | Turns a brokerage composite or a fixed asset list into spreadsheet-style entry. |
| Enable Windows standard keystrokes | Makes copy/paste behave the way the rest of the machine does. |

**Setup > Options > Calculation & View/Print**

| Option | Why |
|---|---|
| Always show tax computation worksheet | Shows how the tax was produced instead of a single number. Turn this on permanently. |
| Always show reason for no EIC | Answers "why didn't EIC generate" without diagnosis. |
| Print Schedule A only when required | Prevents shipping an itemized schedule the client did not use. |
| Autocalculate on exiting data entry | Keeps the totals current as you work. |

**Setup > Options > Optional Documents / Billing** — set the engagement letter, privacy policy, and consent forms to generate automatically so they are never omitted.

**Setup > Firm, Preparer, ERO** — PTIN, EFIN, firm information. A missing or wrong PTIN is a preparer penalty issue, not a formatting issue.

### 0.2 Navigation and field mechanics

Screens **1** through **5** are the spine of the return and sit on the **General** tab, along with **W2**, **1099**, **SSA**, **A**, **2106**, **2441**, and — new for TY2025 — **1A**. Screens are distributed across tabs by topic; confirmed tabs include **General**, **Adjustments** (where the K-1 QBI screen **K199** lives), and **Health Care** (**95A** and **8962**). **Any screen can also be opened by typing its code into the selector field** at the bottom of any data entry screen, which is faster than hunting tabs and is how this guide expects you to navigate. Where a screen's tab is not stated below, use the selector.

A **highlighted tab** means at least one screen on that tab has data — the fastest read on what a return already contains.

Several screens carry **sub-tabs** that hold fields easy to miss: **W2 > Additional Entries** (extra Box 12, Box 14, and state entries), **2 > Due Diligence**, **8863 > Educational Institutions**, **8867 > Overrides**, and **K1P > 1065 K1 13-20**.

| Keystroke | Result |
|---|---|
| Page Up / Page Down | Move between multiple instances of the same screen (several W-2s, several 1099-Rs) |
| CTRL+V | Calculate and view |
| CTRL+E | Return to data entry from view |
| CTRL+W | Open the detail worksheet behind the current field |
| CTRL+F | Move past a field that is rejecting an unsupported code |
| ESC | Save and exit the current screen |
| F1 | Screen help for the installed year |
| F3 | Flag a field for review; flagged returns will not be marked complete until cleared |

**Field conventions.**

- A **red-shaded field** generally has a detail worksheet behind it (CTRL+W). Enter the detail, not a keyed total, whenever the worksheet exists — it is what prints on the supporting statement.
- **Override** fields replace a calculated number. **Adjustment** fields modify it: positive increases, negative decreases. Using either one is an admission that you could not find the entry that produced the wrong number. Find the entry.
- The **F** box excludes an item from the federal return; `0` suppresses it entirely. Used when data must reach a state return but not the federal.
- The **ST** dropdown assigns an entry to a state and can generate a state return. Wrong ST codes are the leading cause of unexpected state returns.
- The **TS/TSJ** box assigns an item to Taxpayer, Spouse, or Joint. On an MFJ return this is invisible until you split the return or hit a per-person limit, and then it decides the answer. Set it on every screen, every time.
- **LookBack (PY Fields / PY Data)** shows which fields on the open screen carried prior-year data and what it was. On a returning client this is the fastest completeness check available.

### 0.3 The order of operations

Preparation order is not a preference. Later sections consume earlier answers.

1. Intake, identity, consents (Part 1)
2. Taxpayer and spouse data — screen **1** (Part 2)
3. Filing status (Part 3)
4. Dependents (Part 4)
5. All income (Part 5)
6. Adjustments to income → AGI (Part 6)
7. Schedule 1-A additional deductions (Part 7)
8. Standard vs. itemized (Part 8)
9. QBI deduction → taxable income (Part 9)
10. Tax computation (Part 10)
11. Nonrefundable credits (Part 11)
12. Other taxes (Part 12)
13. Payments and refundable credits (Part 13)
14. Refund or balance due, next-year estimates (Part 14)
15. Due diligence (Part 15)
16. Quality review, signatures, transmission (Part 16)

AGI is the hinge. Nearly every phaseout on the return is measured against AGI or a MAGI derived from it, so anything that changes income or adjustments changes results downstream. When you fix an income item late, re-check every credit.

### Quiz 0

1. Which two Setup options should be on for every return regardless of preparer experience, and what does each prevent?
2. What is the practical difference between an override field and an adjustment field?
3. On an MFJ return, what does the TS/TSJ box control, and when does getting it wrong first become visible?
4. A field is shaded red. What does that tell you, and what keystroke do you use?
5. Why is AGI described as the hinge of the return?

---

# PART 1 — INTAKE, IDENTITY, AND CONSENT

**Read:** Pub 4491, *Screening and Interviewing* · Form 13614-C and instructions · Circular 230 §10.22 (diligence as to accuracy), §10.34 (standards for returns)

### 1.1 The interview

The return is only as good as the interview, and the interview happens before the software opens. Form 13614-C is the IRS intake and interview sheet. It is free, it is better than anything a firm will write from scratch, and every box a client marks "unsure" is a question you have to ask out loud and resolve before entry begins.

The intake answers that most often change which forms you will need:

- Marital status **and** the date of any change during the year → filing status, Part 3
- Anyone lived with the taxpayer who is not on last year's return → dependents, Part 4
- Self-employment or gig income of any size, including cash → Schedule C, 5.8
- Health coverage purchased through the Marketplace → Form 1095-A and Form 8962, mandatory, 12.6
- Any foreign account, foreign income, or foreign address → Schedule B Part III, FinCEN 114, Form 8938, 5.3
- Digital asset activity → the digital asset question on page 1, 5.13
- Retirement distributions, rollovers, or conversions → 5.5 and 6.6
- A move, a home sale, or a rental → 5.7, 5.9
- Student loan payments, tuition paid, or a 1098-T → 6.7, 11.4
- Estimated tax payments made → 13.2
- An IRS notice, a prior-year amendment, or a disallowed credit → Part 17

### 1.2 Identity and eligibility

Verify photo identification and Social Security cards or ITIN letters for everyone on the return. An SSN that is wrong by one digit produces a reject at best and a misdirected refund at worst.

TY2025 raises the stakes: several benefits now require a valid SSN for the **taxpayer**, not only for the dependent. This is new and is a frequent source of surprise denials. See 11.2 (child tax credit) and Part 7 (Schedule 1-A deductions).

An **Identity Protection PIN (IP PIN)** must be entered if the IRS issued one. A return missing a required IP PIN rejects; a return with last year's IP PIN also rejects.

### 1.3 Consent — §7216 and §6103(c)

Using or disclosing a client's return information without a valid, signed, correctly worded consent is a criminal provision under §7216 and a penalty under §6713. It is not a formality and it is not covered by a general engagement letter.

| Consent | Governs |
|---|---|
| Consent to **use** | Using return information for anything other than preparing the return — cross-selling, marketing, a related service |
| Consent to **disclose** | Giving return information to anyone outside the firm, including a lender, another preparer, or the client's advisor |
| §6103(c) disclosure | Authorizing the IRS to disclose e-file information to a designated party |

Consents must be signed before the use or disclosure occurs, must state the purpose, and must not be bundled into an unrelated document. In Drake, the taxpayer may sign the USE and DISC screens electronically and the signed consent prints with the return — **the preparer cannot sign or date these on the taxpayer's behalf.** Blank §7216 forms are also available at **Tools > Blank Forms**, searching "7216."

KB: 10866 (consent forms) · 13355 (Drake E-Sign) · 11688 (alternative electronic signatures)

### 1.4 Drake — intake, identity, and consents

| Screen | Where | What it holds | Notes |
|---|---|---|---|
| **IDS**† | Selector | Taxpayer and spouse identification documents: type, number, issuing authority, issue and expiration dates | Some states require ID information for e-file. Blank ID fields are a common state-only reject. |
| **PIN** | Selector | Form 8879 signature dates, taxpayer and spouse PINs, ERO PIN | Also see 16.4 |
| **USE** | Selector | Consent to **use** tax return information | The taxpayer can e-sign the screen and the signed consent prints with the return. **The preparer may not sign or date it on the taxpayer's behalf.** |
| **CONS** | Selector | Consent to **disclose** tax return information to other firms | Built for sub-EFIN / master-EFIN franchise and network arrangements |
| **DISC** | Selector | Consent to disclose on behalf of the taxpayer | The preparer may not sign this for the taxpayer either |
| **MISC** | Selector | Miscellaneous codes, IP PIN fields, third-party designee, prior-year comparison controls | The IP PIN for taxpayer, spouse, and dependents lives here in most versions† |
| **ADMN**† | Selector | Return tracking, preparer and reviewer assignment, due diligence status | Firm workflow, not a tax form |
| **NOTE** | Selector | Notes attached to the return; can be set to prevent the return from being marked complete | Use for unresolved intake items so the return cannot ship with an open question |
| **PDF** | Selector | Attach PDF documents to the e-filed return | Required for certain elections and appraisals |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Accepting the client's characterization of a document instead of reading the document. "It's a retirement thing" covers a 1099-R rollover, a Roth conversion, and an early distribution with a penalty.
- Beginning data entry with unresolved "unsure" boxes on the 13614-C. Every one of them is a fact that decides a form.
- Treating the engagement letter as a §7216 consent. It is not.
- Carrying forward last year's IP PIN. It changes annually.

### Quiz 1

1. What does §7216 govern, and what is the difference between a consent to use and a consent to disclose?
2. Name four intake answers that change which forms the return will require.
3. What happens to a return that omits a required IP PIN, and what happens if the prior year's IP PIN is used?
4. Which Drake screen prevents a return from being marked complete while an open question exists?
5. New for TY2025: name one benefit that requires a valid SSN for the taxpayer and not only for a dependent.

---

# PART 2 — TAXPAYER DATA AND RETURN SETUP

**Read:** Instructions for Form 1040, *Filing Requirements* and the top-of-form instructions · Pub 501, *Who Must File*

### 2.1 What screen 1 actually controls

Screen **1** looks like a demographics screen. It is not. Entries here silently decide the standard deduction, credit eligibility, and several e-file requirements.

| Field on screen 1 | What it drives |
|---|---|
| Filing status | Standard deduction, brackets, and eligibility for most credits (Part 3) |
| Taxpayer / spouse **date of birth** | Additional standard deduction at 65 (8.1), senior deduction on Schedule 1-A (7.5), EITC age tests (13.4), IRA and retirement rules (6.6) |
| Taxpayer / spouse **date of death** | Final return handling, signature requirements, Form 1310 |
| **Blind** checkboxes | Additional standard deduction (8.1) |
| **Dependent of another** checkbox | Caps the standard deduction at the dependent's limited amount (8.1) and blocks several credits |
| SSN / ITIN | Credit eligibility and reject risk (1.2) |
| Address, including foreign address | State return generation, foreign filing rules |
| Presidential Election Campaign | No effect on tax; ask, do not assume |
| Digital asset question | Page 1 of the 1040, required on every return (5.13) |
| Third-party designee | Whether the IRS may discuss the return with the preparer |
| State / resident information | Which state returns generate |

**Filing requirement.** Not everyone must file, but a taxpayer below the filing threshold often *should* file — refundable credits, withholding refunds, and starting the assessment statute all require a filed return. Pub 501 has the threshold chart; note that the threshold is generally the standard deduction for the status, and that self-employment income of $400 or more creates a filing requirement regardless of the threshold.

### 2.2 Drake — return setup

| Screen | Where | What you enter |
|---|---|---|
| **1** | General | Names, SSNs, DOBs, dates of death, address, filing status, blindness, dependent-of-another, presidential campaign, digital asset question, third-party designee |
| **2** | General | Dependents, one per entry; grid entry available (Part 4) |
| **MISC** | Selector | IP PINs†, miscellaneous codes, prior-year comparison, elections |
| **PREP**† | Selector | Preparer override when the return is not prepared by the default preparer |
| **ADMN**† | Selector | Workflow and tracking |
| **ES** | Selector | Prior-year overpayment applied and estimates paid (13.2) |
| **STATE tabs** | Tabs | State-specific data entry |

**Starting the return.** Create the return by SSN (KB 10221). If the client filed with the firm last year, the prior-year return should be **carried forward**, which brings basis, carryovers, depreciation, and prior-year comparison with it. A returning client entered as a new return loses every carryover silently — no message, no flag. This is one of the most expensive mistakes available in the software.

Carryovers that only survive if the return is properly carried forward: capital loss carryover, charitable contribution carryover, passive activity loss carryover, NOL, §179 carryover, depreciation basis and prior depreciation, AMT credit, foreign tax credit carryover, and prior-year state overpayment applied.

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Typing a birth year in the wrong century. Drake will accept it; the additional standard deduction and senior deduction will be wrong.
- Leaving the "dependent of another" box unchecked for a student whose parents claim them. This overstates the standard deduction by thousands.
- Starting a returning client as a new return.
- Leaving the digital asset question unanswered. It is required on every return.

### Quiz 2

1. Name four downstream calculations that depend on the date of birth entered on screen 1.
2. A 19-year-old college student earned $6,000 and is claimed by their parents. What must be checked on screen 1, and what does it change?
3. What creates a filing requirement even when income is below the standard deduction threshold?
4. List five carryovers that are lost if a returning client is set up as a new return instead of carried forward.
5. Where is the digital asset question answered, and on which returns is it required?

---

# PART 3 — FILING STATUS

**Read:** Pub 4012, Tab B · Pub 501, *Filing Status* · Pub 4491, *Filing Status*

### 3.1 The five statuses

Status is determined by the taxpayer's situation **on December 31**, with two exceptions: a taxpayer whose spouse died during the year may still file jointly for that year, and a married taxpayer living apart may qualify as head of household under the abandoned spouse rules.

| Status | Core requirement |
|---|---|
| **Single** | Unmarried on 12/31 and does not qualify for HOH or QSS |
| **Married filing jointly (MFJ)** | Married on 12/31, both agree to file jointly and both sign. Also available for the year a spouse dies. |
| **Married filing separately (MFS)** | Married on 12/31, filing apart. Default when spouses will not or cannot file jointly. |
| **Head of household (HOH)** | Unmarried (or treated as unmarried), **paid more than half the cost of keeping up the home**, **and** a qualifying person lived in the home more than half the year |
| **Qualifying surviving spouse (QSS)** | Spouse died in one of the two prior years, taxpayer has a dependent child, has not remarried, and pays more than half the cost of the home |

### 3.2 Head of household — the test people fail

HOH requires **both** conditions, and preparers routinely test only the first:

1. A **qualifying person** — generally a qualifying child who lived with the taxpayer more than half the year, or a dependent parent (who does not have to live with the taxpayer), or certain qualifying relatives who do.
2. The taxpayer **paid more than half the cost of keeping up the home** — rent or mortgage interest, property tax, insurance, repairs, utilities, and food eaten in the home. Not clothing, education, medical, vacations, or the value of the taxpayer's own labor.

An unmarried parent whose child lives with them is not automatically HOH. If a grandparent, partner, or public assistance paid more than half the household cost, the test fails.

**Treated as unmarried (abandoned spouse).** A married taxpayer may file HOH if the spouse did not live in the home for the last six months of the year, the taxpayer paid more than half the cost, and a qualifying child lived with them more than half the year. All of it, not some of it.

### 3.3 MFS — what it costs

Choosing MFS is rarely neutral. It disallows or restricts:

- Earned income credit — disallowed
- Education credits (AOTC and lifetime learning) — disallowed
- Student loan interest deduction — disallowed
- Dependent care credit — disallowed except under the living-apart rules
- Traditional IRA deduction — phaseout range collapses to $0–$10,000 if covered by a plan
- Roth contributions — phaseout collapses to $0–$10,000
- Premium tax credit — disallowed except in domestic abuse or abandonment situations
- Social Security taxation — the base amount drops to zero if the spouses lived together at any point in the year, so benefits are taxed much sooner
- SALT cap and capital loss limit — halved
- If one spouse itemizes, the other **must** itemize, even if their itemized total is zero

MFS is still correct in specific cases: separated spouses who cannot cooperate, liability protection from a spouse's known problems, income-driven student loan repayment strategies, and occasionally a large medical expense against one spouse's lower AGI. Run it both ways rather than assuming.

### 3.4 Drake — filing status

| Screen / field | Where | Detail |
|---|---|---|
| **1**, Filing Status dropdown | General | Codes 1–5 correspond to Single, MFJ, MFS, HOH, QSS† |
| **1**, spouse fields | General | Enable when status is 2 or 3. MFS requires the spouse's name and SSN. |
| **1**, "lived apart from spouse all year" indicator† | General | Drives the MFS Social Security base amount and PTC exceptions |
| **DD1** | Selector | Head of household due diligence section — required with 8867 (Part 15) |
| **MFS Split / Return > Split** | Toolbar | Splits an MFJ return into two MFS returns for comparison. Run this before advising. |
| **8958**† | Selector | Community property allocation, required for MFS in community property states |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Community property states** (AZ, CA, ID, LA, NV, NM, TX, WA, WI) require income to be split between MFS returns regardless of who earned it. Filing MFS in these states without Form 8958 produces two wrong returns.

**Traps.**

- Claiming HOH on the strength of a dependent alone, without testing household cost.
- Using the MFJ standard deduction for a QSS by memory rather than confirming the status is still available — QSS runs for the two years *after* the year of death, and the year of death itself is MFJ.
- Filing MFS in a community property state without Form 8958.
- Forgetting that if one MFS spouse itemizes, the other must.

### Quiz 3

1. What two conditions must **both** be satisfied for head of household, and which one is usually skipped?
2. Name five items married filing separately disallows or restricts.
3. A taxpayer's spouse died in March 2025. What is the filing status for TY2025, and what is it for TY2026 if there is a dependent child?
4. Under the abandoned spouse rules, what three facts must all be true for a married taxpayer to file HOH?
5. Which Drake tool compares MFJ against MFS, and which form is required for MFS in a community property state?

---

# PART 4 — DEPENDENTS

**Read:** Pub 4012, Tab C · Pub 501, *Dependents* · Pub 4491, *Dependents*

Dependents drive the child tax credit, the credit for other dependents, EITC, the dependent care credit, education credits, and head of household. An error here contaminates the entire back half of the return.

### 4.1 Two separate tests

Every dependent is either a **qualifying child** or a **qualifying relative**. Different tests, different results. A person who fails one may still pass the other.

**Qualifying child — all five must be met**

| Test | Requirement |
|---|---|
| Relationship | Child, stepchild, foster child, sibling, step-sibling, or a descendant of any of these |
| Age | Under 19, or under 24 and a full-time student for at least five months, or permanently and totally disabled at any age |
| Residency | Lived with the taxpayer **more than half the year**; temporary absences for school, illness, military, or detention count as time at home |
| Support | The **child** did not provide more than half of their **own** support |
| Joint return | The child does not file a joint return, except to claim a refund of withholding |

**Qualifying relative — all four must be met**

| Test | Requirement |
|---|---|
| Not a qualifying child | Of this taxpayer or anyone else |
| Relationship or household | A listed relative (no residency requirement), or any person who lived with the taxpayer the **entire** year as a member of the household |
| Gross income | The person's gross income is below the exemption threshold for the year (Appendix C) |
| Support | The **taxpayer** provided more than half of the person's total support |

Note the support test runs in opposite directions between the two tests. That reversal is the single most common conceptual error in this area.

### 4.2 Tiebreakers

When two people can claim the same qualifying child and cannot agree, the tiebreaker rules decide — not the taxpayers, and not whoever files first.

1. A parent wins over a non-parent.
2. Between two parents, the one with whom the child lived longer wins.
3. If residency is equal, the parent with the higher AGI wins.
4. If no parent can claim the child, the person with the highest AGI wins — but only if that AGI is higher than any parent's AGI.

### 4.3 Divorced and separated parents

The **custodial parent** is the parent with whom the child lived the greater number of nights. The custodial parent may release the dependency claim with **Form 8332**, which transfers the child tax credit and credit for other dependents to the noncustodial parent.

It does **not** transfer: head of household, EITC, the dependent care credit, or the exclusion for dependent care benefits. Those stay with the custodial parent, always. A divorce decree is not a substitute for Form 8332 for any decree executed after 2008.

### 4.4 Drake — dependents

| Screen | Where | What you enter | Notes |
|---|---|---|---|
| **2** | General | One dependent per entry: name, SSN, relationship, DOB, months lived in home, student and disabled indicators, childcare expense amount, dependent code | Grid entry available. The **months in home** field is the field that decides most contested claims. |
| **2**, dependent code field | General | Controls whether the dependent is treated as a qualifying child, other dependent, or non-dependent (claimed only for HOH or EITC)† | A dependent with an ITIN gets ODC, not CTC |
| **2**, "not a dependent but qualifies for EIC/HOH" indicator† | General | Lets a person count for HOH or EITC without being claimed as a dependent |
| **8332** | Selector | Release or revocation of claim by the custodial parent | Attach the signed 8332 as a PDF (screen **PDF**) when e-filing |
| **2120**† | Selector | Multiple support declaration where several people together provide support |
| **8862** | Selector | Claiming EITC, CTC/ACTC/ODC, or AOTC after a prior disallowance | Omitting it when required is an automatic reject or denial |
| **DD1** / **DD2** | Selector | Due diligence questions supporting the dependent-driven credits (Part 15) |
| **8867** | Selector | Paid preparer due diligence checklist (Part 15) |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Entering a dependent without confirming **months lived in the home**. Residency is what actually decides contested claims, and Drake will happily compute credits from a blank or defaulted value.
- Reversing the support test between qualifying child and qualifying relative.
- Assuming a divorce decree substitutes for Form 8332.
- Giving the noncustodial parent head of household or EITC along with the released dependency.
- Missing that a dependent with an ITIN rather than an SSN valid for employment qualifies for ODC, not CTC.
- Failing to file Form 8862 after a prior disallowance.

### Quiz 4

1. List the five qualifying child tests.
2. In which direction does the support test run for a qualifying child, and in which direction for a qualifying relative?
3. A child lived with each parent exactly half the year. Who claims the child, and on what basis?
4. Form 8332 is signed by the custodial parent. Which tax benefits transfer and which four do not?
5. Which field on Drake screen 2 most often decides a contested claim, and what is the consequence of leaving it at its default?
6. When is Form 8862 required, and what happens if it is omitted?

---

# PART 5 — INCOME

**Read:** Pub 4012, Tab D · Pub 17, *Income* chapters · Pub 525, *Taxable and Nontaxable Income*

Income is reported on Form 1040 lines 1 through 8, with line 8 pulling the total of Schedule 1 Part I. The governing rule is that **all income is taxable unless a Code section excludes it** — never the other way around. Do not go looking for a section that makes something taxable.

**Completeness before accuracy.** The most damaging income error is not a wrong number, it is a missing document. Before entering anything, reconcile the client's documents against three sources: last year's return (via LookBack / prior-year comparison), the client's own list, and where available an IRS wage and income transcript. Missing income produces a CP2000 notice twelve to eighteen months later, with interest.

---

## 5.1 Wages — Form W-2

**Read:** Pub 4491, *Income — Wages, Interest, Etc.* · Pub 4012, Tab D · Instructions for Form W-2

### What matters on the form

| Box | Contents | Consequence |
|---|---|---|
| 1 | Wages, tips, other compensation | Form 1040 line 1a |
| 2 | Federal income tax withheld | Payments block, line 25a — a **different block** from Box 1 |
| 3 / 5 | Social Security and Medicare wages | Reconcile to Box 1; large differences mean deferrals or pre-tax benefits |
| 4 / 6 | Social Security and Medicare tax withheld | Excess SS tax from multiple employers is a **refundable credit** (13.5) |
| 7 / 8 | Social Security tips / allocated tips | Allocated tips are not in Box 1 and must be added via Form 4137 (12.3) |
| 10 | Dependent care benefits | Flows to Form 2441; excess over the exclusion becomes taxable wages |
| 11 | Nonqualified plans | Affects Social Security earnings tests |
| 12 | Coded items — see below | Several of these control forms you have not opened yet |
| 13 | Statutory employee / **Retirement plan** / Third-party sick pay | The retirement box decides IRA deductibility (6.6) |
| 14 | Other — employer's discretion | State disability, union dues, after-tax HSA, clergy items, TY2025 qualified overtime and tips reporting |
| 15–20 | State and local | Drives state returns; check the ST code |

**Box 12 codes that change the return**

| Code | Meaning | Where it goes |
|---|---|---|
| **W** | Employer + employee HSA contributions through a cafeteria plan | Form 8889 — **already excluded** from Box 1, do not deduct again (6.4) |
| **D, E, G, H, S** | Elective deferrals (401(k), 403(b), 457, SIMPLE) | Already excluded from Box 1; may support the saver's credit (11.5) |
| **AA, BB, EE** | Designated Roth contributions | After-tax, already in Box 1; supports the saver's credit |
| **DD** | Cost of employer-sponsored health coverage | Informational only. Not deductible, not income. |
| **P** | Excludable moving expense reimbursements | Military only |
| **Q** | Nontaxable combat pay | Elective inclusion for EITC purposes (13.4) |
| **T** | Adoption benefits | Form 8839 |
| **R** | Archer MSA contributions | Form 8853 |
| **J** | Nontaxable sick pay | Excluded from Box 1 |
| **L** | Substantiated employee business expense reimbursements | Not income |
| **M / N** | Uncollected SS/Medicare on group-term life | Flows to other taxes |
| **Z / K** | Nonqualified deferred comp failures / golden parachute excess | Additional tax |

### Drake

| Screen | Where | Detail |
|---|---|---|
| **W2** | General | One screen per W-2. Page Down for the next. Enter every box that has data, not just 1 and 2. |
| **W2**, TS box | General | Assign to taxpayer or spouse. Wrong assignment breaks the SS wage base, the IRA coverage test, and the excess SS tax credit. |
| **W2**, Box 12 grid | General | Code and amount. Additional Entries expands when a W-2 has more codes than fit. |
| **W2**, Box 14 grid | General | Free-form. Some entries need a specific Drake code to route correctly (e.g. state disability to Schedule A). |
| **W2**, state grid (Boxes 15–20) | General | ST code decides which state return the wages land on |
| **W2**, special tax treatment / clergy fields† | General | Clergy, statutory employee, and foreign employer handling |
| **4852** | Selector | Substitute for a missing or incorrect W-2. Requires documented attempts to obtain the real one. |
| **8919** | Selector | Uncollected Social Security and Medicare on wages when a worker was misclassified as a contractor |
| **4137** | Selector | Unreported tip income (12.3) |

Turn on **wage and withholding verification** (0.1) — it forces re-entry of Boxes 1, 2, 16, and 17 and catches transposition at the point of entry.
KB: https://kb.drakesoftware.com/kb/Drake-Tax/10932.htm · Screen help: F1

**Traps.**

- Entering Boxes 1 and 2 and skipping the rest. This silently breaks HSA, IRA, saver's credit, and dependent care.
- Adding a Box 12 code W amount as an HSA contribution on Form 8889 line 2. It belongs on line 9. Double-counting it produces an excess contribution penalty.
- Ignoring Box 13 retirement. It decides whether an IRA contribution is deductible.
- Assigning both spouses' W-2s to the taxpayer on an MFJ return.
- Treating Box 12 code DD as anything other than information.

### Quiz 5.1

1. Box 1 and Box 2 land in two different blocks of the return. Name them and explain why the distinction matters.
2. What does Box 12 code W represent, which form does it trigger, and on which line of that form does it belong?
3. Why does the Box 13 retirement plan checkbox matter, and which later section consumes it?
4. Two employers, combined Social Security wages above the wage base. What is the result and where does it appear?
5. A client's W-2 shows allocated tips in Box 8. What must be done, and what form is required?

---

## 5.2 Tip income

**Read:** Pub 531, *Reporting Tip Income* · Instructions for Form 4137 · **TY2025: Schedule 1-A Part II (Part 7 of this guide)**

Tips are wages. Tips reported to the employer appear in W-2 Box 1 and Box 7 and require nothing further. Two situations require more:

- **Unreported tips** — cash tips the employee never reported to the employer. Form **4137** computes the Social Security and Medicare tax the employer did not withhold, and the tips are added to wages.
- **Allocated tips (Box 8)** — the employer allocated a share of gross receipts to the employee. These are **not** in Box 1. They must be reported unless the employee's records prove a lower amount.

**New for TY2025.** A deduction of up to $25,000 for **qualified tips** is available on Schedule 1-A Part II. It is a deduction against income, not an exclusion — the tips still appear in wages, still carry Social Security and Medicare tax, and still count in AGI. Only the deduction reduces taxable income. See 7.2 for the occupation list, the SSN requirement, the MFJ requirement, and the phaseout.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **W2**, Boxes 7 and 8 | General | Reported and allocated tips |
| **4137** | Selector | Unreported tips; computes SS and Medicare tax to Schedule 2 |
| **1A**† | Selector | TY2025 qualified tips deduction (Part 7) |
| **C** | Selector | Tips received by a self-employed person are business receipts, not W-2 tips |

### Quiz 5.2

1. What is the difference between reported tips, allocated tips, and unreported tips, and which of the three is already in Box 1?
2. Which form computes the employee's share of Social Security and Medicare on unreported tips, and where does that tax land on the return?
3. For TY2025, does the qualified tips deduction reduce AGI, Social Security tax, or taxable income? State which and why it matters.

---

## 5.3 Interest income

**Read:** Pub 550, *Investment Income and Expenses* · Pub 4012, Tab D · Instructions for Schedule B

### What goes where

- **Taxable interest** → Form 1040 line 2b
- **Tax-exempt interest** → line 2a. Reported but not taxed. It still matters: it enters the Social Security taxability calculation (5.6), the premium tax credit MAGI, and several other phaseouts.
- **Original issue discount (OID)**, Form 1099-OID, is interest accrued but not paid. It is taxable currently.
- **US savings bond interest** may be excludable when used for qualified education — Form **8815**, subject to a MAGI phaseout and unavailable to MFS.
- **Nominee interest** — interest received on behalf of someone else is reported and then backed out with a nominee adjustment.
- **Accrued interest paid** at purchase of a bond reduces the reportable interest.
- **Private activity bond interest** is tax-exempt for regular tax but is an AMT preference item (10.5).

### Schedule B is required when

- Taxable interest **or** ordinary dividends exceed $1,500, **or**
- The taxpayer had a foreign account or foreign trust interest, **or**
- Certain other conditions in the Schedule B instructions (nominee distributions, bond premium, seller-financed mortgage interest).

### Foreign accounts — Schedule B Part III

Part III is the entry point to two separate foreign reporting regimes and gets missed constantly.

| Regime | Threshold | Filed |
|---|---|---|
| **FinCEN Form 114 (FBAR)** | Aggregate foreign account value exceeded $10,000 at any point during the year | Filed with FinCEN, **not** with the return |
| **Form 8938** | Higher, status- and residence-dependent thresholds (Appendix C) | Filed **with** the return |

The two can both apply, either can apply alone, and the penalties for missing an FBAR are severe and non-discretionary.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **INT** | Selector | 1099-INT entry, one payer per entry; grid entry available for brokerage composites |
| **INT**, tax-exempt fields | Selector | Separate boxes for tax-exempt interest and for the private activity portion (AMT) |
| **INT**, nominee / accrued interest / OID adjustment fields† | Selector | Adjustments that reduce reportable interest with a printed explanation |
| **B** | Selector | Schedule B, including the Part III foreign account and trust questions |
| **8815** | Selector | Series EE/I savings bond interest exclusion for education |
| **8814** | Selector | Parent's election to report a child's interest and dividends on the parent's return |
| **1099-OID entry**† | Selector | Confirm placement in the installed year; commonly entered on INT |
| **FBAR / 114**† | Selector | FinCEN 114 preparation, transmitted separately from the 1040 |
| **8938** | Selector | Statement of specified foreign financial assets |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Omitting tax-exempt interest because it is not taxed. It changes the taxation of Social Security and several MAGI tests.
- Answering the Schedule B Part III foreign account question "no" by default without asking.
- Netting accrued interest paid against the wrong payer.
- Treating an FBAR as satisfied by filing Form 8938, or vice versa.

### Quiz 5.3

1. Under what three conditions is Schedule B required?
2. Why is tax-exempt interest reported on a return if it is not taxed? Name two calculations it enters.
3. What is the FBAR threshold, where is the form filed, and how does it differ from Form 8938?
4. Which Drake screen holds the foreign account question, and which part of Schedule B is it?
5. A client cashed savings bonds to pay tuition. What form may exclude the interest, and what disqualifies the exclusion?

---

## 5.4 Dividends

**Read:** Pub 550 · Pub 4012, Tab D

**Ordinary dividends** → Form 1040 line 3b. **Qualified dividends** → line 3a, a subset of line 3b, taxed at long-term capital gain rates rather than ordinary rates. The split is the whole point; the total alone tells you nothing about the tax.

To be qualified, a dividend must be paid by a domestic or qualified foreign corporation and the underlying stock must satisfy a **holding period** — generally more than 60 days within the 121-day window surrounding the ex-dividend date. Payers apply this test, but a client who sold shortly after a dividend may have a Box 1b amount that overstates what actually qualifies.

Other 1099-DIV boxes that matter:

| Box | Item | Treatment |
|---|---|---|
| 2a | Total capital gain distributions | Long-term gain; may go directly to line 7 without Schedule D if there is nothing else |
| 2b–2d | Unrecaptured §1250, collectibles (28%), §1202 gain | Special rates; forces Schedule D and its worksheets |
| 3 | Nondividend distribution (return of capital) | Not income. Reduces basis. When basis reaches zero, further distributions are capital gain. |
| 5 | §199A dividends | Feed the QBI deduction (Part 9) even with no business |
| 7 | Foreign tax paid | Form 1116 or the de minimis direct credit (11.6) |
| 11 | Exempt-interest dividends | Same treatment as tax-exempt interest (5.3) |
| 12 | Private activity bond interest dividends | AMT preference |

### Drake

| Screen | Where | Detail |
|---|---|---|
| **DIV** | Selector | 1099-DIV entry, one payer per entry; grid entry available |
| **DIV**, Box 1a / 1b fields | Selector | Ordinary and qualified. Entering only 1a overstates tax. |
| **DIV**, Box 2a–2d | Selector | Capital gain distributions and the special-rate categories |
| **DIV**, Box 3 | Selector | Nondividend distribution; track basis outside the software |
| **DIV**, Box 5 | Selector | §199A dividends → Form 8995 |
| **DIV**, Box 7 + **1116** | Selector | Foreign tax credit |
| **B** | Selector | Schedule B when ordinary dividends exceed $1,500 |
| **8814** | Selector | Parent's election for a child's dividends |

**Traps.**

- Entering the total in Box 1a and leaving 1b blank. This is the most expensive keystroke in this section — it prices qualified dividends at ordinary rates.
- Treating a nondividend distribution as income instead of a basis reduction.
- Missing Box 5 §199A dividends, which produce a QBI deduction for a client with no business at all.

### Quiz 5.4

1. What is the relationship between Form 1040 line 3a and line 3b?
2. What is the holding period requirement for a qualified dividend, and why can a payer's Box 1b still overstate the taxpayer's qualified amount?
3. What is a nondividend distribution and what happens when basis reaches zero?
4. Which 1099-DIV box produces a deduction on a return with no business income, and which form does it feed?

---

## 5.5 Retirement distributions — Form 1099-R

**Read:** Pub 590-B, *Distributions from IRAs* · Pub 575, *Pension and Annuity Income* · Pub 4012, Tab D

Form 1040 lines 4a/4b (IRAs) and 5a/5b (pensions and annuities). The **a** line is the gross distribution, the **b** line is the taxable amount. When they differ, the return must show why.

### Reading the form

| Box | Item | Notes |
|---|---|---|
| 1 | Gross distribution | Goes to the "a" line |
| 2a | Taxable amount | Often equals Box 1 |
| 2b | "Taxable amount not determined" / "Total distribution" | When 2b is checked, the payer does not know the basis. **You** must compute it. |
| 4 | Federal withholding | Payments block |
| 5 | Employee contributions / Roth basis / insurance premiums | Recovery of after-tax money |
| 7 | **Distribution code** | The single most important box on the form |
| IRA/SEP/SIMPLE box | Marks the distribution as an IRA | Determines whether line 4 or line 5 applies |

**Distribution codes worth memorizing**

| Code | Meaning | Consequence |
|---|---|---|
| 1 | Early distribution, no known exception | 10% additional tax unless an exception applies on Form 5329 |
| 2 | Early distribution, exception applies | No penalty |
| 3 | Disability | No penalty |
| 4 | Death | No penalty; beneficiary rules apply |
| 7 | Normal distribution | Ordinary treatment |
| G | Direct rollover | Not taxable; line "a" shows the amount, line "b" shows zero, and **ROLLOVER** prints beside it |
| H | Direct rollover of designated Roth to a Roth IRA | Not taxable |
| J / T / Q | Roth IRA distributions — early, exception applies, qualified | Q is fully tax-free; J and T require ordering rules |
| B | Designated Roth account | Different from a Roth IRA |
| S | Early SIMPLE distribution within 2 years | 25% additional tax, not 10% |

### The situations that require judgment

- **60-day (indirect) rollover.** The client received a check, then redeposited it within 60 days. The 1099-R shows code 1 or 7 and a taxable amount. The return must show the rollover, and there is a one-rollover-per-12-months limit across all IRAs.
- **Basis in a traditional IRA.** Nondeductible contributions create basis reported on Form 8606. Every subsequent distribution is partly a nontaxable return of that basis, computed pro rata across **all** traditional IRAs. If Form 8606 was never filed, the client is taxed twice — and the fix is a chain of amended returns.
- **Roth conversion.** Taxable now, tax-free later, reported on Form 8606 Part II.
- **Qualified charitable distribution (QCD).** Age 70½ or older, paid directly from the IRA to the charity. The 1099-R gives no indication whatsoever. The distribution is excluded from income — better than a charitable deduction, because it reduces AGI. Ask about it; the form will never tell you.
- **Required minimum distributions.** Failure to take an RMD triggers an excise tax on Form 5329 (reduced from the historical 50% to 25%, and to 10% if corrected timely).
- **Inherited accounts.** Post-2019 deaths generally fall under the 10-year rule, with annual RMDs required in some cases. This is a research question, every time.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **1099** | General | Form 1099-R entry. One screen per form. |
| **1099**, Box 7 and IRA/SEP/SIMPLE box | General | Drives penalty, form routing, and whether the amount is an IRA or a pension |
| **1099**, "Exclude here; distribution is reported elsewhere" / rollover fields† | General | Marks a rollover so it prints correctly |
| **1099**, state grid | General | State withholding and the ST code |
| **8606** | Selector | Nondeductible contributions, basis, distributions from basis, Roth conversions |
| **ROTH**† | Selector | Roth contribution and conversion tracking, basis history |
| **5329** | Selector | Early distribution penalty and its exceptions; missed RMD excise tax |
| **8880** | Selector | Saver's credit; certain distributions reduce it |
| **SSA** | General | Social Security — a different form and a different line (5.6) |
| **1310**† | Selector | Refund due a deceased taxpayer |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Entering Box 1 into a taxable field when a rollover occurred, converting a nontaxable transaction into income.
- Accepting Box 2a when Box 2b "taxable amount not determined" is checked and the client has IRA basis.
- Never asking about QCDs for a client over 70½ who gives to charity.
- Missing the SIMPLE two-year 25% rate and applying 10%.
- Assuming a code 1 distribution is always penalized. Form 5329 exceptions include first-time home purchase (IRA only), higher education (IRA only), medical expenses above the AGI floor, disability, separation from service at 55 (plan only), and substantially equal periodic payments.

### Quiz 5.5

1. What is the difference between line 4a and line 4b, and what should print next to the line when a direct rollover occurred?
2. What does distribution code G mean? Code 1? Code S, and what rate does it carry?
3. Box 2b is checked "taxable amount not determined" and the client made nondeductible IRA contributions for years. What must you do, and which form holds the answer?
4. What is a QCD, what are its requirements, and why is it better than a charitable deduction?
5. Name four exceptions to the 10% early distribution penalty and the form that reports them.

---

## 5.6 Social Security and railroad retirement — Form SSA-1099

**Read:** Pub 915, *Social Security and Equivalent Railroad Retirement Benefits* · Pub 4012, Tab D

Form 1040 line 6a is the gross benefit, line 6b the taxable portion. Between zero and 85% of benefits are taxable, determined by **provisional income**:

> Provisional income = AGI excluding Social Security + **tax-exempt interest** + certain exclusions + **one-half of the Social Security benefit**

Compared against base amounts (Appendix C), this produces a 0%, 50%, or 85% inclusion tier. Two consequences follow:

- Tax-exempt interest raises the tax on Social Security even though it is not itself taxed. A client who "moved everything into munis to lower taxes" may have raised them.
- Because additional income both is taxed and drags benefits into taxation, the marginal rate in the phase-in range can substantially exceed the bracket rate. This matters for Roth conversion and distribution planning.

**MFS.** If the spouses lived together at any time during the year, the base amount is **zero** and up to 85% of benefits are taxable immediately.

**Lump-sum election.** When benefits for a prior year are paid in the current year, the taxpayer may elect to compute the taxable amount using the prior year's income. Reported on line 6c. Requires prior-year figures.

**Not the same thing:** SSI (supplemental security income) is not taxable and is not reported at all. Disability benefits paid under Social Security **are** reported on SSA-1099 and follow the same rules.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **SSA** | General | Net benefits, Medicare premiums (Boxes 3 and 5), federal withholding, repayments |
| **SSA**, Medicare premium fields | General | Medicare Parts B and D premiums flow to Schedule A medical (8.2) |
| **SSA**, lump-sum election fields† | General | Prior-year amounts for the line 6c election |
| **RRB**† | Selector | Railroad retirement, Tier 1 and Tier 2 handled differently |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Entering the net check amount instead of the gross benefit. Medicare premiums are withheld from the check, and they are a medical deduction, not a reduction of benefits.
- Omitting tax-exempt interest, which understates the taxable benefit.
- Missing the MFS-lived-together rule.
- Reporting SSI.

### Quiz 5.6

1. Write the provisional income formula. Which non-taxable item appears in it, and why does that surprise clients?
2. What are the two possible inclusion tiers above zero?
3. Spouses filing MFS lived together for part of the year. What is the base amount and what is the effect?
4. Medicare premiums are withheld from the client's benefit. What amount is entered on the SSA screen, and where do the premiums go?
5. What is the lump-sum election and on which line does it appear?

---

## 5.7 Capital gains, losses, and basis

**Read:** Pub 550 · Pub 551, *Basis of Assets* · Pub 523, *Selling Your Home* · Instructions for Schedule D and Form 8949

Form 1040 line 7, from Schedule D. Every sale needs three facts: **proceeds, basis, and holding period.** The broker supplies the first, may or may not supply the second, and reports the third — but the client's own records govern when the broker's basis is not reported to the IRS.

### The mechanics

- **Short-term** — held one year or less. Taxed at ordinary rates.
- **Long-term** — held more than one year. Taxed at 0%, 15%, or 20% depending on taxable income (Appendix C), plus possible 3.8% NIIT (12.5).
- Short-term and long-term net separately, then against each other.
- A **net capital loss** deducts up to $3,000 per year ($1,500 MFS) against ordinary income. The remainder carries forward indefinitely, retaining its character. **The carryover is lost if the return is not carried forward properly** (2.2).
- **Wash sale** — a loss on a security sold and repurchased (or purchased) within 30 days before or after is disallowed and added to the basis of the replacement. Brokers report wash sales only within one account at one broker; cross-account and IRA repurchases are the client's problem and yours.
- **Special rates:** collectibles at 28%, unrecaptured §1250 gain at 25%, §1202 qualified small business stock exclusions.

### Form 8949 categories

Transactions are grouped by whether basis was reported to the IRS:

| Box | Meaning |
|---|---|
| A / D | Basis **reported** to the IRS (short / long) |
| B / E | Basis **not reported** to the IRS (short / long) |
| C / F | No 1099-B received (short / long) |

Category A and D transactions with no adjustments can be summarized directly on Schedule D without listing each sale. Everything else needs detail.

### Basis, the part that requires work

| Situation | Basis rule |
|---|---|
| Purchase | Cost plus commissions and acquisition costs |
| Inherited | **Fair market value at date of death** (step-up), and the holding period is automatically long-term |
| Gift | Donor's basis carried over for gain; FMV at gift for loss — the dual-basis rule |
| Stock split / dividend reinvestment | Basis spreads across all shares; reinvested dividends were already taxed and **are** basis |
| Mutual fund shares | Specific identification, FIFO, or average cost — the method matters and must be consistent |
| Employer stock (ESPP, RSU, ISO) | The compensation element already in W-2 Box 1 **is** basis. Brokers frequently omit it, which double-taxes the client. |

The employer stock case is the highest-value catch in this section. A broker 1099-B for RSU shares often shows a basis of zero or of the discounted purchase price, while the client already paid tax on the spread through their W-2.

### Sale of a principal residence

Under §121, up to $250,000 of gain ($500,000 MFJ) is excluded if the taxpayer owned and used the home as a principal residence for two of the last five years, and has not used the exclusion in the prior two years. Partial exclusions apply for a move due to health, employment, or unforeseen circumstances. A sale with fully excluded gain and no 1099-S need not be reported; if a 1099-S was issued, report it and show the exclusion.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **8949** | Selector | Individual transaction detail: description, dates, proceeds, basis, adjustment code and amount, Form 8949 box |
| **8949**, adjustment code field | Selector | W (wash sale), B (incorrect basis), H (home sale exclusion), and others — the code drives the printed column |
| **D** | Selector | Schedule D totals, summarized entries, and special-rate items |
| **D2** | Selector | Capital loss carryovers in and out, plus **direct entry on Schedule D lines 1a and 8a** — the summary route for category A and D transactions with basis reported and no adjustments. Enter total proceeds and total basis rather than keying every sale. |
| **DIV**, Box 2a | Selector | Capital gain distributions, which may reach line 7 without Schedule D |
| **HOME**† | Selector | Sale of principal residence and the §121 exclusion |
| **4797** | Selector | Sale of business property and depreciation recapture (5.8) |
| **6252** | Selector | Installment sales |
| **8824**† | Selector | Like-kind exchange, real property only after 2017 |
| **6781**† | Selector | §1256 contracts and straddles |
| **8960** | Selector | Net investment income tax (12.5) |
| **Import** | Toolbar | Broker 1099-B import, where supported, avoids keying hundreds of transactions |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Accepting a zero or understated basis on employer stock.
- Losing a capital loss carryover between years.
- Missing wash sales across accounts or into an IRA, where the loss is permanently lost rather than deferred.
- Treating inherited property as carryover basis.
- Reporting a home sale gain without testing §121, or omitting a reported 1099-S entirely.
- Forgetting that reinvested mutual fund dividends are basis, which inflates gain on every sale.

### Quiz 5.7

1. What three facts does every sale require, and which one is most often wrong?
2. State the basis rule for inherited property, for gifted property with a gain, and for gifted property with a loss.
3. What is the annual capital loss deduction limit, what happens to the excess, and what causes it to be lost?
4. A client sold RSU shares. The 1099-B reports basis of $0. What is likely wrong and how do you fix it?
5. What are the requirements of the §121 exclusion, and what are the exclusion amounts?
6. What is a wash sale, what happens to the disallowed loss, and what makes an IRA repurchase worse than an ordinary one?

---

## 5.8 Self-employment — Schedule C

**Read:** Pub 334, *Tax Guide for Small Business* · Pub 535 successor guidance on business expenses · Pub 463 (travel, meals) · Pub 587 (business use of home) · Pub 946 (depreciation) · Instructions for Schedule C and Schedule SE

Schedule C flows to Schedule 1 Part I, then to Form 1040 line 8. It also drives self-employment tax (Schedule SE, 12.2), the SE health insurance deduction (6.5), self-employed retirement deductions (6.6), and the QBI deduction (Part 9).

### Scope

A Schedule C exists when there is a trade or business carried on with continuity and a profit motive. It is required regardless of whether a 1099-NEC or 1099-K was issued and regardless of amount. Cash income is income.

**TY2025 note:** the 1099-K reporting threshold was restored to more than $20,000 **and** more than 200 transactions. Clients who received 1099-Ks in prior years may not receive one now. The income is reported either way.

**Hobby vs. business.** If there is no profit motive, income is reported as other income and **no expenses are deductible** — the miscellaneous itemized deduction that used to allow them is suspended. The nine-factor test is in the regulations; the presumption is a profit in three of five years.

### The income and expense structure

| Part | Contents |
|---|---|
| I | Gross receipts, returns, cost of goods sold, gross profit |
| II | Expenses by category, lines 8–27 |
| III | Cost of goods sold detail — beginning inventory, purchases, labor, materials, ending inventory |
| IV | Vehicle information when not filing Form 4562 |
| V | Other expenses, itemized |

**Expense areas that require care**

- **Vehicle.** Standard mileage (70¢ per business mile for 2025) or actual expenses. The choice in the first year of use constrains later years — a vehicle placed in service with actual expenses and MACRS depreciation cannot switch to standard mileage. Contemporaneous mileage records are required; a year-end estimate is not substantiation.
- **Meals.** 50% deductible when business-related and not lavish. Entertainment remains fully nondeductible.
- **Home office.** Requires **exclusive and regular** use as the principal place of business. Simplified method at $5 per square foot up to 300 square feet, or actual expenses on Form 8829. The deduction cannot create or increase a loss; the excess carries forward.
- **Depreciation.** Assets over the de minimis threshold are capitalized. TY2025 restored **100% bonus depreciation** for qualifying property acquired after January 19, 2025, and raised the §179 limit (Appendix C). Bonus applies automatically unless elected out; §179 is elected and is limited by business income.
- **Contract labor.** Payments of $600 or more to non-corporate service providers require Form 1099-NEC. Schedule C lines 59–60† ask whether the filing requirement applied and whether the forms were filed. Answering carelessly is a due diligence problem.
- **Startup costs.** Up to $5,000 deductible in year one, with the remainder amortized over 15 years.
- **What is not deductible:** the owner's own salary or draw, federal income tax, personal portions of anything, life insurance where the business is the beneficiary, political contributions, and fines or penalties.

### Losses

A Schedule C loss offsets other income, but check: at-risk limits (Form 6198), passive activity limits if the taxpayer does not materially participate (Form 8582), and the excess business loss limitation (Form 461), which caps the deductible loss and converts the excess to an NOL carryforward.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **C** | Selector | One screen per business. Business code, name, EIN, accounting method, material participation, receipts, expenses by line, 1099 filing questions |
| **C**, "business income is QBI" / QBI fields† | Selector | Controls whether the activity feeds Form 8995 (Part 9) |
| **4562** | Selector | Depreciation and amortization; asset-by-asset detail; §179 and bonus elections. Link each asset to the correct activity with the **multi-form code**. Use this detail screen, **not** the override screens 6–9, which exist only for depreciation computed outside Drake. |
| **AUTO**† | Selector | Vehicle detail — mileage, actual expenses, business use percentage. Also linked by multi-form code. |
| **8829** | Selector | Business use of home; simplified or actual method |
| **SE** | Selector | Schedule SE; usually automatic, used for adjustments, optional methods, and clergy |
| **SEHI** | Selector | Self-employed health insurance (Form 7206), limited to net profit (6.5) |
| **SEP**† | Selector | Self-employed SEP, SIMPLE, and qualified plan deduction (6.6) |
| **8995** / **8995A** | Selector | QBI deduction (Part 9) |
| **99M** / **NEC** | Selector | 1099-MISC and 1099-NEC source entry; link to the Schedule C with a multi-form code |
| **99K**† | Selector | 1099-K entry, routed to the correct activity |
| **6198**† | Selector | At-risk limitation |
| **8582** | Selector | Passive activity loss limitation |
| **461**† | Selector | Excess business loss limitation |
| **ES** | Selector | Estimated tax for the following year (14.3) |

**The multi-form code** is the mechanism that ties a 4562 asset, an AUTO entry, or a 1099 to a specific Schedule C when there is more than one business. Leaving it blank on a multi-business return attaches everything to the first activity. Check it every time.

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Deducting the owner's draw as an expense.
- Claiming a home office without exclusive use, or claiming one that creates a loss.
- Switching a vehicle from actual expenses to standard mileage.
- Deducting 100% of a cell phone, a vehicle, or an internet connection with obvious personal use.
- Reporting gross 1099-K receipts and separately reporting the same sales as cash receipts, double-counting income.
- Leaving the multi-form code blank on a return with two businesses.
- Answering the 1099 filing requirement questions without asking the client.
- **Two software-specific depreciation traps.** Omitting the asset's **Life** on screen 4562 generates EF message 2408 and blocks e-file. And a description beginning with the word **LAND** suppresses the depreciation calculation entirely — enter "BUILDING AND LAND," never "LAND AND BUILDING." The second one fails silently. (KB 11881, 14188)

KB: 11794 (4562 screen vs. screens 6-9) · 11881 (§179, limits, EF message 2408) · 14188 (description keywords) · 10108 (depreciation calculation) · 11565 (recapture) · 10893 (auto expenses) · 10520 (1099-K data entry) · 10519 (SE health insurance)

### Quiz 5.8

1. When is a Schedule C required, and does the absence of a 1099-NEC change the answer?
2. What are the two vehicle expense methods, and what is the trap in the first year a vehicle is placed in service?
3. State the two requirements for a home office deduction and what happens when the deduction would create a loss.
4. What is the difference between §179 and bonus depreciation in how they are claimed and how they are limited?
5. Income has no profit motive. Where is it reported and what happens to the related expenses?
6. What is the multi-form code and what goes wrong when it is left blank?

---

## 5.9 Rental and royalty income — Schedule E Part I

**Read:** Pub 527, *Residential Rental Property* · Pub 925, *Passive Activity and At-Risk Rules* · Pub 946 · Instructions for Schedule E

### Structure

Each property is reported separately with its type, address, fair rental days, and personal use days. Income is rent received; expenses run advertising, auto and travel, cleaning, commissions, insurance, legal, management fees, mortgage interest, other interest, repairs, supplies, taxes, utilities, depreciation, and other.

**Repair vs. improvement** is the recurring judgment. A repair keeps the property in operating condition and is deducted now. An improvement betters, restores, or adapts the property and is capitalized and depreciated. The tangible property regulations provide safe harbors (de minimis, small taxpayer, routine maintenance) that are worth knowing because they resolve most of these.

**Depreciation is not optional.** Residential rental property is depreciated over 27.5 years, commercial over 39, straight-line, mid-month convention, land excluded. If depreciation is not claimed, gain on sale is still computed as though it had been (**allowed or allowable**), so skipping it costs the deduction and keeps the recapture.

**Personal use.** If the taxpayer uses the property personally for more than the greater of 14 days or 10% of rental days, expenses are limited and the property may fall under the vacation home rules. Under 15 rental days in the year, the income is not reported at all and no expenses are deducted.

### Passive losses

Rental activity is passive by default. Losses are suspended unless:

- The **$25,000 active participation allowance** applies — available to a taxpayer who actively participates (approves tenants, sets terms), phased out between $100,000 and $150,000 of modified AGI, or
- The taxpayer is a **real estate professional** meeting both the 750-hour test and the more-than-half-of-personal-services test, or
- The property is disposed of in a fully taxable transaction, which releases all suspended losses.

Suspended losses carry forward and are tracked on Form 8582. Losing that carryover between years is a real and common error.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **E** | Selector | One screen per property: type, address, fair rental and personal use days, active participation indicator, income and expenses |
| **E**, QBI fields† | Selector | Whether the rental qualifies as a trade or business for §199A, including the safe harbor |
| **4562** | Selector | The building, improvements, appliances, and land — linked by multi-form code to the property |
| **8582** | Selector | Passive activity loss limitation and suspended loss carryforward |
| **6198**† | Selector | At-risk |
| **4797** | Selector | Sale of the rental property, with §1250 recapture |
| **K1P** / **K1S** / **K1F** | Selector | Rental and other activity arriving through a partnership, S corporation, or trust (5.10) |
| **99M** | Selector | Rents reported on a 1099-MISC Box 1 |
| **4835**† | Selector | Farm rental income where the landlord does not materially participate |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Capitalizing nothing, or capitalizing everything, instead of applying the improvement standard.
- Omitting depreciation and assuming the client keeps the basis.
- Including land in the depreciable basis.
- Missing personal use days, which the client will not volunteer.
- Losing suspended passive losses on carryforward, or failing to release them on a disposition.

### Quiz 5.9

1. What distinguishes a repair from an improvement, and what is the consequence of getting it wrong?
2. Explain "allowed or allowable" and why skipping depreciation does not help the client.
3. What is the $25,000 special allowance, who qualifies, and over what income range does it phase out?
4. A property is rented for 12 days during the year and used personally the rest. How is it reported?
5. Which form tracks suspended passive losses, and what event releases them?

---

## 5.10 Pass-through income — Schedules K-1

**Read:** Instructions for Schedule K-1 (Forms 1065, 1120-S, 1041) · Pub 541 (partnerships) · Pub 925 · Form 7203 instructions

A K-1 is a routing document. Each box directs an item to a different place on the 1040, and the character of the income is determined at the entity level and preserved through to the individual return.

| Source | Form | Common destinations |
|---|---|---|
| Partnership | K-1 (1065) | Ordinary business income → Schedule E Part II; guaranteed payments → SE tax; separately stated interest, dividends, capital gains, §179, charitable, §199A |
| S corporation | K-1 (1120-S) | Ordinary business income → Schedule E Part II, **not** subject to SE tax; separately stated items |
| Estate or trust | K-1 (1041) | Interest, dividends, capital gains, other income, deductions in the final year |

**Basis and loss limitations run in order:** basis first, then at-risk, then passive. A loss must clear all three to be deducted.

- **S corporation shareholders** must file **Form 7203** to report stock and debt basis when claiming a loss, receiving a distribution, disposing of stock, or receiving a loan repayment. Shareholder basis is the shareholder's responsibility, not the corporation's, and it is frequently untracked.
- **Partners** track outside basis, which differs from the capital account reported on the K-1.

**Guaranteed payments** to a partner are subject to self-employment tax. S corporation distributions are not, but a shareholder-employee must take **reasonable compensation** on a W-2 — an S corporation K-1 with substantial ordinary income and no W-2 wages to the owner is an examination flag.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **K1P** | Selector | Partnership K-1; box-by-box entry mirroring the form |
| **K1S** | Selector | S corporation K-1 |
| **K1F** | Selector | Estate or trust K-1 |
| **K1P/K1S**, §199A and basis tabs† | Selector | QBI components (Part 9) and basis worksheets |
| **7203**† | Selector | S corporation shareholder stock and debt basis |
| **6198**† | Selector | At-risk |
| **8582** | Selector | Passive loss limitation and carryforward |
| **8995** / **8995A** | Selector | QBI aggregation and computation |
| **1116** | Selector | Foreign taxes reported on a K-1 |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Entering only the ordinary income box and ignoring the separately stated items, which is where the §199A information, the charitable contributions, the §179, and the foreign taxes live.
- Treating the K-1 capital account as tax basis.
- Deducting a loss without a basis computation or Form 7203.
- Subjecting S corporation ordinary income to self-employment tax.
- Missing K-1 footnotes, which frequently carry the §199A detail and state apportionment.

### Quiz 5.10

1. In what order do the three loss limitations apply to a K-1 loss?
2. Which form reports S corporation shareholder basis, and when is it required?
3. Which is subject to self-employment tax: a partnership guaranteed payment, or S corporation ordinary income? Explain both.
4. Why is the K-1 capital account not the same as tax basis?
5. Name three items that arrive as separately stated K-1 items and go somewhere other than Schedule E Part II.

---

## 5.11 Farm income — Schedule F

**Read:** Pub 225, *Farmer's Tax Guide* · Instructions for Schedule F

Schedule F reports farm income and expenses, structured like Schedule C but with agriculture-specific rules: crop insurance deferral elections, weather-related livestock sale deferrals, prepaid farm supplies limits, and income averaging on **Schedule J**. Farm rental income where the landlord does not materially participate goes on **Form 4835**, not Schedule F, and is not subject to SE tax.

Farmers who meet the two-thirds-of-gross-income test have a special estimated tax rule: a single installment due January 15, or no estimate at all if the return is filed and the tax paid by March 1.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **F** | Selector | Schedule F income and expenses |
| **4835**† | Selector | Farm rental, non-material participation |
| **J**† | Selector | Farm income averaging |
| **4562** | Selector | Farm assets, linked by multi-form code |
| **SE** | Selector | Self-employment tax, including the farm optional method |

### Quiz 5.11

1. What distinguishes Schedule F from Form 4835, and what is the SE tax consequence?
2. What does Schedule J do?
3. What is the special estimated tax rule for qualifying farmers?

---

## 5.12 Unemployment, state refunds, and other government payments

**Read:** Pub 525 · Instructions for Schedule 1

- **Unemployment compensation** (Form 1099-G Box 1) is fully taxable on Schedule 1 Part I. There is no exclusion for TY2025. Withholding is optional and most clients decline it, which is why unemployment years produce balances due.
- **State and local income tax refunds** (Form 1099-G Box 2) are taxable only to the extent the tax produced a benefit in the prior year — the **tax benefit rule**. A client who took the standard deduction last year has no taxable refund. A client who itemized but was capped by SALT may have only a partial inclusion. The prior-year return is required to answer this.
- **Agricultural payments, taxable grants, and RTAA payments** appear in other 1099-G boxes and route to Schedule F or other income.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **99G** | Selector | Form 1099-G: unemployment, state refunds, withholding, and the prior-year information that drives the tax benefit computation |
| **99G**, state refund worksheet fields† | Selector | Prior-year itemized deduction, standard deduction, and SALT figures |
| **3** | General | Schedule 1 Part I additional income |

**Trap.** Reporting the full state refund as income without running the tax benefit worksheet. On a standard-deduction client the correct amount is zero, and Drake will not know that unless the prior-year data is present or entered.

### Quiz 5.12

1. Is unemployment compensation taxable for TY2025, and is withholding automatic?
2. Under what circumstance is a state income tax refund entirely nontaxable?
3. What prior-year figures are required to compute the taxable portion of a state refund?

---

## 5.13 Other income, digital assets, and the catch-all

**Read:** Pub 525 · Instructions for Schedule 1, Part I

Schedule 1 Part I collects income that has no line of its own. The items that come up:

| Item | Treatment |
|---|---|
| **Gambling winnings** (W-2G and unreported) | Fully taxable as other income. Losses are deductible **only** as an itemized deduction and **only** up to winnings. A client who breaks even but takes the standard deduction pays tax on the full winnings. |
| **Jury duty pay** | Taxable; pay surrendered to an employer is an offsetting adjustment |
| **Prizes and awards** | Taxable at fair market value |
| **Cancellation of debt** (Form 1099-C) | Taxable unless excluded — bankruptcy, insolvency, qualified principal residence, qualified farm or business debt. Insolvency requires a balance sheet at the moment before discharge, and the exclusion is claimed on **Form 982**. |
| **Alimony received** | Taxable **only** under divorce instruments executed on or before 12/31/2018 and not modified to adopt the new rules |
| **Hobby income** | Taxable; expenses not deductible (5.8) |
| **Executor and director fees** | Often self-employment income, not other income |
| **Scholarship amounts exceeding qualified expenses** | Taxable; may need to be identified as SCH |
| **Net operating loss carryforward** | Negative other income |
| **Medicaid waiver payments** | May be excludable under Notice 2014-7 while still counting for EITC by election |

### Digital assets

Page 1 of Form 1040 carries a required yes/no question about digital asset transactions. It must be answered on every return.

- **Selling or exchanging** digital assets is a capital transaction → Form 8949 and Schedule D.
- **Trading one token for another** is a taxable disposition, not a like-kind exchange.
- **Mining, staking, and payment for services** produce ordinary income at fair market value on receipt, and self-employment income if conducted as a business.
- **Merely buying and holding**, or transferring between the taxpayer's own wallets, is a "no" answer for the checkbox purpose but should still be documented.

Basis tracking for digital assets is the client's burden, and broker reporting is still incomplete. Expect to work from exchange reports.

### Drake

| Screen | Where | Detail |
|---|---|---|
| **3** | General | Schedule 1 Part I: other income lines, including a detail worksheet for miscellaneous items (CTRL+W) |
| **W2G** | Selector | Gambling winnings and withholding |
| **A** | General | Gambling losses in the other itemized deductions section (8.5) |
| **99C**† | Selector | Cancellation of debt |
| **982** | Selector | Exclusion of discharged debt and reduction of tax attributes |
| **1** | General | Digital asset question |
| **8949** | Selector | Digital asset dispositions |
| **99M** | Selector | 1099-MISC items that are not self-employment |
| **99K**† | Selector | 1099-K routing |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Netting gambling winnings against losses. They are reported gross, and the losses need Schedule A.
- Reporting a 1099-C as taxable without testing insolvency.
- Applying post-2018 alimony rules to a 2016 divorce, or the reverse.
- Assuming a token-for-token trade is not a taxable event.
- Leaving the digital asset question blank.

### Quiz 5.13

1. A client won $8,000 and lost $8,000 at a casino, and takes the standard deduction. What is the tax result and why?
2. Name four exclusions available for cancellation of debt income and the form that claims them.
3. What determines whether alimony received is taxable?
4. Is trading one cryptocurrency for another a taxable event? What about moving coins between the taxpayer's own wallets?
5. Where on the return is the digital asset question, and on which returns must it be answered?

---

## 5.14 Income that is not reported

Knowing what to leave off is as important as knowing what to include. None of the following is reported as income, though several affect other calculations:

- Gifts and inheritances received (the recipient reports nothing; income *from* inherited property is reported)
- Life insurance proceeds paid by reason of death
- Child support received
- Qualified Roth distributions
- Return of capital / nondividend distributions (basis reduction instead)
- Municipal bond interest (reported on line 2a but not taxed)
- Workers' compensation
- Supplemental security income (SSI)
- Most personal injury settlements for physical injury or sickness (but not punitive damages or interest)
- Qualified scholarships used for tuition and required fees
- Employer-provided health coverage (W-2 Box 12 code DD)
- Qualified HSA distributions used for medical expenses
- Rental of a residence for fewer than 15 days
- Qualified charitable distributions from an IRA

### Quiz 5.14

1. A client received $40,000 from a parent's estate and $1,200 of interest earned on the account after death. What is reported?
2. Which is reported and which is not: child support, alimony under a 2015 decree, workers' compensation, punitive damages?
3. Why does municipal bond interest appear on the return at all?

---

# PART 6 — ADJUSTMENTS TO INCOME (SCHEDULE 1 PART II)

**Read:** Pub 4012, Tab E · Pub 17, *Adjustments to Income* · Pub 4491, *Adjustments to Income*

Total income minus adjustments equals **AGI**, Form 1040 line 11.

## 6.1 Why adjustments are worth more than deductions

Adjustments come out **before** AGI. Itemized deductions come out **after**. Three consequences:

1. Adjustments help every taxpayer. Itemized deductions help only those whose total exceeds the standard deduction.
2. Because AGI governs nearly every phaseout on the return — EITC, education credits, IRA deductibility, student loan interest, the premium tax credit, the medical floor, the Schedule 1-A deductions, NIIT, the passive rental allowance — a dollar of adjustment can be worth more than a dollar of deduction.
3. Most state returns start from federal AGI, so an adjustment usually reduces state tax as well, while a federal itemized deduction may not.

The practical version: when there is a choice between structuring something as an adjustment or a deduction, the adjustment wins nearly every time.

## 6.2 The list

| Adjustment | Key limit or condition |
|---|---|
| Educator expenses | Capped (Appendix C); K–12, 900 hours in a school year |
| Certain business expenses of reservists, performing artists, fee-basis officials | Form 2106; the only survivors of the employee business expense deduction |
| Health savings account deduction | Form 8889; requires HDHP coverage (6.4) |
| Moving expenses | **Armed Forces on active duty under PCS orders only** |
| Deductible part of self-employment tax | Automatic — one-half of SE tax (12.2) |
| Self-employed SEP, SIMPLE, and qualified plans | Computed from net SE income (6.6) |
| Self-employed health insurance | Limited to net profit of the business (6.5) |
| Penalty on early withdrawal of savings | From Form 1099-INT Box 2 |
| Alimony paid | Pre-2019 instruments only; requires recipient SSN and instrument date |
| IRA deduction | Coverage and MAGI tests (6.6) |
| Student loan interest | Capped and phased out; MFS disallowed (6.7) |
| Archer MSA deduction | Form 8853 |
| Other write-in adjustments | Jury duty pay surrendered, §501(c)(18) contributions, attorney fees for certain claims, and others listed in the Schedule 1 instructions |

Note that the charitable deduction for non-itemizers and the tips, overtime, car loan interest, and senior deductions are **not** adjustments — the TY2025 items are on Schedule 1-A and come out after AGI (Part 7). This distinction matters because it means they do **not** loosen AGI-based phaseouts.

## 6.3 Educator expenses

Up to the annual cap (Appendix C) per eligible educator, doubled on a joint return when both spouses qualify. Eligible: kindergarten through grade 12 teacher, instructor, counselor, principal, or aide who worked at least 900 hours during a school year. Qualifying costs include books, supplies, computer equipment and software, other classroom materials, and professional development. Amounts above the cap are not deductible anywhere — the itemized deduction that used to absorb them is suspended.

## 6.4 Health savings accounts — Form 8889

An HSA deduction requires coverage under a **high deductible health plan** and no disqualifying other coverage (including Medicare, and including a spouse's general-purpose FSA).

The structure of Form 8889 causes most of the errors:

- **Line 2** — contributions the *taxpayer* made directly, with after-tax dollars. These produce the deduction.
- **Line 9** — **employer** contributions, which includes everything run through a cafeteria plan and reported in **W-2 Box 12 code W**. These were already excluded from Box 1. They reduce the remaining contribution room but produce **no additional deduction**.

Entering the Box 12 code W amount on line 2 double-counts it and generates a phantom excess contribution and a 6% excise tax.

**Last-month rule.** A taxpayer covered by an HDHP on December 1 may contribute the full annual amount for the year, but must remain HDHP-eligible through the following December (the testing period) or the excess becomes income plus a 10% additional tax.

**Distributions** are the other half of the form: tax-free when used for qualified medical expenses, taxable plus 20% when not. Form 1099-SA reports them.

## 6.5 Self-employed health insurance — Form 7206

Deductible for the taxpayer, spouse, dependents, and children under 27. Three limits:

1. **Net profit** of the business the plan is established under. There is no deduction against a Schedule C loss.
2. The deduction is **not** allowed for any month the taxpayer was eligible for an employer-subsidized plan through their own or a spouse's employer.
3. Premiums claimed here cannot also be claimed on Schedule A.

For S corporation shareholders owning more than 2%, the premiums must be included in the shareholder's W-2 wages to be deductible here. If the corporation paid the premiums without running them through payroll, the deduction is not available.

**Circular reference warning.** When a client has both self-employed health insurance and the premium tax credit, the two are computed against each other iteratively. Drake handles this, but verify the result rather than assuming.

## 6.6 Retirement contributions

### Traditional IRA

Anyone with earned income (wages or net self-employment income) may contribute up to the annual limit, plus a catch-up at 50 and older (Appendix C). A spouse with little or no earned income may contribute on a joint return under the **spousal IRA** rules. Contributions may be made until the unextended filing deadline.

**Deductibility** turns on two facts:

1. Whether the taxpayer or spouse is **covered by a workplace retirement plan** — this is the **W-2 Box 13 retirement checkbox** from 5.1, and it is the reason that box mattered.
2. **MAGI** against the phaseout range for the filing status and coverage situation (Appendix C). There are three separate ranges: taxpayer covered, taxpayer not covered but spouse covered, and MFS.

If not deductible, the contribution is still permitted and creates **basis**, reported on **Form 8606 Part I**. Failing to file Form 8606 loses the basis and causes the client to be taxed a second time on the same money when it is eventually distributed — often decades later, when reconstructing it is nearly impossible.

### Roth IRA

Not deductible, so it produces no adjustment, but the contribution is subject to its own MAGI phaseout and may support the saver's credit (11.5). A **backdoor Roth** — a nondeductible traditional contribution followed by a conversion — requires Form 8606 and is subject to the **pro rata rule**, which measures the conversion against **all** traditional, SEP, and SIMPLE IRA balances. A client with an existing pre-tax IRA balance does not get a tax-free backdoor conversion, regardless of what they read.

### Self-employed plans

SEP, SIMPLE, and solo 401(k) contributions for a self-employed person are deducted here rather than on Schedule C, and are computed on net earnings **after** the deduction for one-half of SE tax — a circular computation the software performs. SEP contributions may be made up to the extended due date.

## 6.7 Student loan interest

**Read:** Pub 970, *Tax Benefits for Education* · Form 1098-E

Capped at $2,500, phased out by MAGI (Appendix C), and **disallowed entirely for MFS**. Also unavailable to anyone who can be claimed as a dependent by another taxpayer.

The loan must have been taken out for **qualified education expenses of the taxpayer, spouse, or a dependent at the time the debt was incurred** — the later dependency status does not matter. Qualified expenses include tuition, fees, room and board, books, and required equipment, reduced by tax-free assistance.

The deduction belongs to the person **legally obligated on the loan**, which is not always the person writing the check:

- A parent who pays a loan on which only the child is obligated deducts nothing, and the child is treated as having received a gift and made the payment — so the child may deduct it if the child is not claimed as a dependent.
- A parent legally obligated on the loan who pays it deducts it, provided the student was their dependent when the debt was incurred.
- A co-signer who is legally obligated and actually pays may deduct it.

Interest includes capitalized interest and loan origination fees allocable to interest, not only the amount on the 1098-E. Voluntary payments of interest during a deferral period qualify.

## 6.8 Alimony paid

Deductible only under divorce or separation instruments **executed on or before December 31, 2018** and not later modified to adopt the post-TCJA rules. The deduction requires the **recipient's SSN** and the **date of the original instrument** on the return; omitting the SSN can cost the deduction outright.

Payments must be cash, must end at the recipient's death, must not be designated as child support, and must not be for property settlement. Any amount tied to a contingency relating to a child is child support regardless of what the instrument calls it.

### Drake — adjustments

| Screen | Where | Detail |
|---|---|---|
| **4** | General | Schedule 1 Part II: educator expenses, IRA deduction, student loan interest, alimony paid (with recipient SSN and instrument date), penalty on early withdrawal, write-in adjustments |
| **8889** | Selector | HSA. Line 2 for taxpayer contributions; line 9 receives W-2 Box 12 code W automatically |
| **HSA**† | Selector | Supporting HSA entries and distributions (Form 1099-SA) |
| **8853** | Selector | Archer MSA and long-term care contracts |
| **SEHI** | Selector | Self-employed health insurance, Form 7206 |
| **LTC**† | Selector | Long-term care premiums, age-based limits |
| **SEP**† | Selector | Self-employed SEP, SIMPLE, and qualified plan deduction |
| **8606** | Selector | Nondeductible IRA contributions, basis, conversions |
| **ROTH**† | Selector | Roth contribution and conversion history and basis |
| **8880** | Selector | Saver's credit generated by the same contributions |
| **5329** | Selector | Excess contribution and early distribution penalties |
| **2106** | General | Reservist, performing artist, and fee-basis official expenses |
| **3903**† | Selector | Moving expenses, military only |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Entering the W-2 Box 12 code W HSA amount as a taxpayer contribution.
- Deducting self-employed health insurance in excess of net profit, or when an employer plan was available.
- Failing to file Form 8606 for a nondeductible IRA contribution.
- Running a backdoor Roth without accounting for existing pre-tax IRA balances.
- Deducting alimony under a post-2018 instrument.
- Deducting moving expenses for a civilian.
- Missing the IRA deduction because the Box 13 checkbox was never entered, or claiming it when the checkbox should have been entered.

### Quiz 6

1. Explain in two sentences why an adjustment is generally worth more than an itemized deduction of the same size.
2. Which two facts determine whether a traditional IRA contribution is deductible, and where does the first one come from?
3. On Form 8889, what is the difference between line 2 and line 9, and what happens if a Box 12 code W amount is entered on line 2?
4. What three limits apply to the self-employed health insurance deduction?
5. A client makes a $7,000 nondeductible traditional IRA contribution and converts it to a Roth the next day. They also hold $93,000 in a rollover IRA. What portion of the conversion is taxable, and what rule produces that answer?
6. What happens if Form 8606 is never filed for a nondeductible contribution?
7. Who may deduct moving expenses for TY2025?
8. A parent pays the student loan of a child who is no longer a dependent, and only the child is legally obligated on the loan. Who may deduct the interest, and what filing status disqualifies the deduction entirely?
9. What two items must appear on the return to support an alimony deduction, and what determines whether the instrument qualifies at all?

---

# PART 7 — SCHEDULE 1-A, ADDITIONAL DEDUCTIONS (NEW FOR TY2025)

**Read:** Instructions for Schedule 1-A (Form 1040) · IRS newsroom guidance, *Schedule 1-A, Additional Deductions* · Drake KB 18889

Schedule 1-A is new for TY2025 and carries four OBBBA deductions. Its total lands on **Form 1040 line 13b**, alongside the QBI deduction on line 13a, and is subtracted **after** AGI.

## 7.1 How Schedule 1-A works

**Three structural facts that govern all four deductions:**

1. They are **below-the-line** deductions but are **not itemized deductions**. A taxpayer taking the standard deduction gets them too.
2. Because they come out after AGI, they **do not loosen any AGI-based phaseout**. They reduce taxable income and nothing else.
3. Each has its own MAGI phaseout, and each requires a **valid SSN**. Tips, overtime, and the senior deduction require a married taxpayer to **file jointly**. **Car loan interest is the exception** — the statute imposes no joint-filing condition, and the $10,000 cap then applies to each spouse's separate return. Secondary sources disagree on this point; the final regulations published 2 January 2026 govern, so confirm before advising a couple to file separately in order to use it.

These deductions are also **temporary**, applying to tax years 2025 through 2028 unless extended.

| Schedule 1-A part | Deduction | Cap (TY2025) |
|---|---|---|
| I | Modified AGI computation used by all four | — |
| II | Qualified tips | $25,000 |
| III | Qualified overtime compensation | $12,500 single / $25,000 MFJ |
| IV | Car loan interest | $10,000 |
| V | Enhanced deduction for seniors | $6,000 per qualifying individual |

## 7.2 Qualified tips

Available to employees and to self-employed individuals in occupations that **customarily and regularly received tips** on or before December 31, 2024, as listed in the Treasury-published occupation list. Cash tips, charged tips, and tip-sharing amounts qualify; service charges do not.

- Cap: $25,000
- The deduction cannot exceed the taxpayer's income from the tipped work; for a self-employed person it is further limited to the net income of the business.
- Phaseout begins at MAGI above the threshold (Appendix C) and reduces the deduction as income rises.
- Specified service trades or businesses are excluded on the self-employed side.
- **The tips remain wages** for Social Security, Medicare, and AGI. This is a deduction only.

## 7.3 Qualified overtime

Only the **premium portion** of overtime required by the Fair Labor Standards Act — the extra half in "time and a half," not the whole overtime payment. A client who reports $10,000 of overtime pay generally has roughly $3,333 of qualified premium.

- Cap: $12,500, or $25,000 on a joint return
- Same MAGI phaseout thresholds as tips
- Overtime paid under a contract or state law but not required by the FLSA does not qualify
- Employers report the amount, generally in W-2 Box 14 or on a separate statement for TY2025

## 7.4 Car loan interest

Interest on a loan used to buy a **new** personal-use vehicle, where the loan is secured by a first lien on the vehicle and the vehicle's **final assembly occurred in the United States**.

- Cap: $10,000 of interest
- The **VIN is required** on Schedule 1-A. No VIN, no deduction.
- Used vehicles, leases, business vehicles, and refinancings of pre-existing loans generally do not qualify
- Loan must originate after December 31, 2024
- Its own MAGI phaseout, lower than the tips and overtime thresholds (Appendix C)

## 7.5 Enhanced senior deduction

A deduction of $6,000 for each taxpayer age 65 or older by the end of the tax year — $12,000 on a joint return where both spouses qualify.

- **In addition to** the existing additional standard deduction for age 65 (8.1). They are two separate benefits and both apply.
- Available whether the taxpayer itemizes or takes the standard deduction.
- Phases out above the MAGI thresholds in Appendix C.
- Requires a valid SSN; married taxpayers must file jointly.

### Drake — Schedule 1-A

| Screen | Where | Detail |
|---|---|---|
| **1A** | **General** | Schedule 1-A: tips, overtime, car loan interest, and senior deduction, plus the MAGI computation in Part I |
| **1A**, line 14a | General | Qualified overtime compensation included in **Form W-2 Box 1** |
| **1A**, line 14b | General | Qualified overtime compensation included in **Form 1099-NEC Box 1 or Form 1099-MISC Box 3** — the self-employed and contractor side, easy to miss |
| **1A**, vehicle section | General | Up to **four vehicles**, each with a taxpayer/spouse selector, the VIN, and the **loan origination date**, which must be after 12/31/2024 |
| **1** | General | Dates of birth, which drive the senior deduction |
| **W2**, Boxes 7 and 14 | General | Source of reported tips and employer-reported qualified overtime |
| **C** | Selector | Self-employed tip income and the business net income limit |

The Schedule 1-A total carries to **Form 1040 line 13b** (Form 1040-SR line 13b; Form 1040-NR line 13c).

KB: 18890 (Schedule 1-A) · 18874 (overtime) · 18926 (car loan interest) · 18889 (New Tax Bill) · 18910 (2025 changes for Form 1040) · Screen help: F1

**Because this schedule is new, confirm its behavior in the installed software before relying on it in front of a client.** Verify that the deduction appears on Form 1040 line 13b, that the MAGI phaseouts compute, and that the senior deduction stacks with the additional standard deduction rather than replacing it.

**Traps.**

- Deducting the full overtime amount rather than the FLSA premium portion.
- Treating the senior deduction as a replacement for the age-65 additional standard deduction.
- Claiming tips, overtime, or the senior deduction on an MFS return. Car loan interest is the one that survives MFS.
- Omitting the VIN.
- Assuming the tips deduction reduces Social Security and Medicare tax. It does not.
- Assuming these deductions loosen an AGI-based phaseout elsewhere on the return. They do not.

### Quiz 7

1. Where does the Schedule 1-A total land on Form 1040, and is it before or after AGI?
2. A taxpayer takes the standard deduction. Can they claim the Schedule 1-A deductions? Why does the answer surprise people?
3. A client earned $18,000 of overtime pay. Approximately how much is potentially deductible, and what governs that?
4. Name four requirements of the car loan interest deduction.
5. A 68-year-old single client takes the standard deduction. Which two age-based benefits apply, and are they alternatives or cumulative?
6. Why does the tips deduction not reduce the client's Social Security tax?
7. Which filing status disqualifies three of the four Schedule 1-A deductions, and which one survives it?

---

# PART 8 — DEDUCTIONS: STANDARD VS. ITEMIZED

**Read:** Pub 501, *Standard Deduction* · Pub 4012, Tab F · Instructions for Schedule A · Pub 502, 526, 936

Form 1040 line 12. The taxpayer takes the **greater** of the standard deduction or total itemized deductions — with the exception that if one MFS spouse itemizes, the other must, and certain taxpayers (dual-status aliens, short-year filers) cannot use the standard deduction at all.

## 8.1 The standard deduction

The base amount depends on filing status (Appendix C). Three modifiers:

- **Age 65 or older** — an additional amount per qualifying person, keyed to the date of birth on screen 1. A taxpayer born on January 1 is treated as reaching 65 on December 31 of the prior year.
- **Blind** — an additional amount per qualifying person, keyed to the blindness checkboxes on screen 1.
- **Dependent of another** — the standard deduction is limited to the greater of a floor amount or earned income plus a small increment, capped at the ordinary standard deduction (Appendix C).

The additional amounts stack: an unmarried taxpayer who is both 65 and blind gets two of them; a married couple where both are 65 gets two.

The senior deduction on Schedule 1-A (7.5) is **separate** and additional.

**On the return this is automatic.** In Drake, nothing is typed. The number is produced entirely from screen 1 — filing status, dates of birth, blindness checkboxes, and the dependent-of-another indicator. That is why 2.1 treats screen 1 as a deduction screen.

## 8.2 Schedule A — medical and dental

**Read:** Pub 502

Deductible only to the extent total qualified expenses exceed **7.5% of AGI**. Because of the floor, medical rarely produces a deduction except in years with a major event or for low-AGI retirees.

Deductible: doctors, dentists, hospitals, prescription drugs, insulin, health and dental insurance premiums (including Medicare Parts B, C, and D and the taxable portion of Part A), long-term care insurance premiums subject to age-based limits, medical mileage at the standard rate, lodging while receiving care subject to a nightly cap, capital improvements for medical necessity to the extent they exceed the increase in property value, and qualified long-term care services.

Not deductible: cosmetic surgery, nonprescription drugs other than insulin, general health items, gym memberships without a specific diagnosis, and anything reimbursed by insurance, an FSA, or an HSA.

Two frequent misses: **Medicare premiums withheld from Social Security benefits** (found on the SSA-1099, 5.6), and premiums paid with after-tax dollars by a retiree.

## 8.3 Schedule A — taxes paid (SALT)

The deduction covers **state and local income tax OR general sales tax** (the taxpayer's choice, whichever is larger), plus **real estate tax** and **personal property tax**.

**TY2025:** the SALT cap rose to **$40,000** ($20,000 MFS), with a phase-down for higher incomes that reduces the cap but not below the prior $10,000 floor (Appendix C). This is the change most likely to move a client from the standard deduction to itemizing for the first time since 2017 — check every client with meaningful state tax and property tax, including ones who have taken the standard deduction for years.

The sales tax election uses either actual receipts or the IRS optional tables plus tax on specified large purchases (vehicles, boats, home building materials). It is usually chosen by clients in states with no income tax, or in a year with a large vehicle purchase.

Not deductible: federal income tax, Social Security and Medicare tax, transfer taxes, homeowners association fees, and assessments for local benefits that increase property value.

## 8.4 Schedule A — interest paid

**Read:** Pub 936

- **Qualified residence interest** on **acquisition debt** — debt incurred to buy, build, or substantially improve a qualified residence (main home plus one other), secured by that residence. The limit is $750,000 of acquisition debt ($375,000 MFS), with pre-December 16, 2017 debt grandfathered at $1,000,000.
- **Home equity interest** is deductible **only** if the proceeds were used to buy, build, or substantially improve the residence securing the loan. A HELOC used to pay off credit cards or buy a car is not deductible, no matter what the 1098 shows. The 1098 does not report how the money was used; the client does.
- **Points** paid on a purchase are generally deductible in full in the year paid; points on a refinance are amortized over the loan term. Unamortized points from an earlier refinance are deducted in full when that loan is paid off.
- **Investment interest expense** (Form 4952) is limited to net investment income, with an indefinite carryforward. Electing to treat qualified dividends and long-term gains as ordinary income to increase the limit is a trade worth computing, not assuming.

## 8.5 Schedule A — charitable contributions and other

**Read:** Pub 526

**AGI limits** (Appendix C): cash to public charities at 60% of AGI, appreciated capital gain property at 30%, and lower percentages for gifts to certain organizations and for gifts of appreciated property to non-public charities. Excess carries forward five years, retaining its category.

**Substantiation is where charitable deductions actually fail**, more often than the limits:

| Gift | Requirement |
|---|---|
| Any cash gift | Bank record or written receipt — a canceled check alone is not enough for larger gifts |
| $250 or more | **Contemporaneous written acknowledgment** from the charity stating whether goods or services were provided. Obtained before the return is filed or the due date, whichever is earlier. Cannot be cured later. |
| Noncash over $500 | **Form 8283 Section A** |
| Noncash over $5,000 | **Form 8283 Section B** plus a **qualified appraisal** |
| Vehicle donation | Form 1098-C; the deduction is generally limited to gross proceeds of the charity's sale |

Not deductible: gifts to individuals, political contributions, the value of donated services or time, raffle tickets, and the portion of a payment representing goods received.

**Other itemized deductions** — the short list that survived: gambling losses to the extent of winnings, casualty losses from federally declared disasters, impairment-related work expenses, unrecovered annuity investment at death, and estate tax paid on income in respect of a decedent. Unreimbursed employee expenses, tax preparation fees, and investment expenses remain suspended.

## 8.6 Making the decision

Run the comparison **before** entering anything on Schedule A. Drake will compute both and take the larger, but time spent entering a $9,000 itemized total for a client with a $31,500 standard deduction is time spent producing nothing.

The clients where itemizing is realistic in TY2025: homeowners with a mortgage in high-tax states (now more likely given the $40,000 SALT cap), taxpayers with a catastrophic medical year, taxpayers with large charitable giving, and disaster-loss years.

There is a state wrinkle: several states require itemized deductions on the state return to match the federal election, or allow state itemizing even when the federal return takes the standard deduction. Check whether itemizing federally at a small loss produces a larger state benefit — Drake will show the federal answer but the decision is a combined one.

### Drake — deductions

| Screen | Where | Detail |
|---|---|---|
| **1** | General | Filing status, DOB, blind, dependent-of-another — the entire standard deduction computation |
| **A** | General | Schedule A: medical, taxes, interest, contributions, other. Detail worksheets (CTRL+W) behind most lines. **Schedule A is not produced unless itemized deductions exceed the standard deduction or the schedule is forced** (KB 16988) — so its absence in View is an answer, not an error. |
| **A**, sales tax fields | General | Election between income tax and sales tax |
| **STAX** | Selector | Optional sales tax table computation and large-purchase entries. Mark *Print the General Sales Tax Worksheet* to review the computation as **Wks STAX** in View. |
| **Wks SALT** | View | The state and local tax limitation worksheet — read it to see how the TY2025 cap and phase-down were applied (KB 15833) |
| **A**, prior-year carryover fields | General | Charitable contribution carryover **in** from prior years |
| **A**, carryover-to-future link† | General | Charitable carryover **out** to next year — verify this populates before rollover |
| **1098**† | Selector | Mortgage interest statement detail, including outstanding principal for the acquisition debt limit |
| **8283** | Selector | Noncash contributions; Section B requires appraiser and donee signatures and often a PDF attachment |
| **4952** | Selector | Investment interest expense and the election to include qualified dividends and capital gains |
| **LTC**† | Selector | Long-term care premiums flowing to the medical section |
| **4684**† | Selector | Casualty and theft losses, federally declared disasters |
| **SSA** | General | Medicare premiums flowing to medical |
| **W2G** / **3** | Selector | Gambling winnings, against which losses are deducted on Schedule A |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Opening screen A out of habit and producing an itemized return that costs the client money.
- Deducting home equity interest without confirming what the proceeds bought.
- Deducting the full 1098 interest when acquisition debt exceeds the limit.
- Missing Medicare premiums in medical.
- Losing a charitable carryover between years because it was never entered on the carryover fields.
- Accepting a client's list of cash donations without acknowledgment letters for gifts of $250 or more.
- Deducting the value of volunteer time.
- Not re-testing itemizing for TY2025 given the higher SALT cap.

### Quiz 8

1. What three items on screen 1 produce the standard deduction, and which one is most often missed on a student's return?
2. Is the Schedule 1-A senior deduction an alternative to the age-65 additional standard deduction, or in addition to it?
3. What is the medical floor, and name two commonly missed medical expenses.
4. What changed about the SALT cap for TY2025, and which clients should be re-tested as a result?
5. A client has a $60,000 HELOC. $40,000 paid for a kitchen remodel and $20,000 paid off credit cards. How much of the interest is deductible and why does the 1098 not answer this?
6. At what gift size is a contemporaneous written acknowledgment required, and can it be obtained after the return is filed?
7. What triggers Form 8283 Section A, Section B, and a qualified appraisal?
8. A client donates 20 hours of professional services worth $3,000. What is the deduction?

---

# PART 9 — QUALIFIED BUSINESS INCOME DEDUCTION (§199A)

**Read:** Instructions for Form 8995 and Form 8995-A · Pub 535 successor QBI guidance

Form 1040 line 13a. A deduction of up to **20% of qualified business income** from a domestic pass-through business — sole proprietorship, partnership, S corporation, and certain rentals — plus 20% of qualified REIT dividends and publicly traded partnership income. Made permanent by OBBBA.

**It is not a business deduction.** It does not reduce self-employment tax, does not appear on Schedule C, and does not affect AGI. It sits alongside the standard or itemized deduction.

## 9.1 The computation, in tiers

**Below the taxable income threshold** (Appendix C): the deduction is the lesser of 20% of QBI or 20% of taxable income less net capital gain. Simple, computed on **Form 8995**. No wage limits, no service business restriction.

**Above the threshold** (Form 8995-A): two things happen.

1. The deduction is limited to the greater of 50% of W-2 wages paid by the business, or 25% of wages plus 2.5% of the unadjusted basis of qualified property.
2. A **specified service trade or business (SSTB)** — health, law, accounting, actuarial science, performing arts, consulting, athletics, financial services, brokerage, and any business whose principal asset is the reputation or skill of its employees or owners — begins to phase out and is eliminated entirely above the top of the range.

Between the threshold and the top of the range, both limitations phase in proportionally.

## 9.2 What counts

QBI includes the net amount of qualified income, gain, deduction, and loss from the business. It **excludes** capital gains and losses, dividends, interest income not allocable to the business, reasonable compensation paid to an S corporation shareholder, and guaranteed payments to a partner.

QBI is reduced by the deductible part of self-employment tax, the self-employed health insurance deduction, and self-employed retirement contributions attributable to the business — a reduction that is easy to overlook when computing by hand.

A **qualified business loss** carries forward and reduces QBI in the following year.

**Rental property** qualifies if it rises to the level of a trade or business under §162. A safe harbor exists requiring 250 hours of rental services per year, separate books and records, and contemporaneous logs. A single triple-net-leased property generally does not qualify.

### Drake — QBI

| Screen | Where | Detail |
|---|---|---|
| **8995** | Selector | Simplified computation for taxpayers below the threshold |
| **8995A**† | Selector | Full computation, wage and property limits, SSTB phase-in |
| **C**, QBI fields† | Selector | Marks the Schedule C as a qualified trade or business and identifies SSTB status |
| **E**, QBI fields† | Selector | Rental QBI treatment and safe harbor election |
| **K199** | **Adjustments** | The dedicated K-1 QBI screen. Select **K1P**, **K1S**, or **K1F** in the *For* box and enter the **multi-form code**, which is required — a blank MFC misroutes the QBI data. |
| **K1P > 1065 K1 13-20** | Tab | Box 20 QBI amounts, including code AD, entered in the Qualified Business Income section |
| **C** / **F**, Override Calculated QBI field | Selector | Schedule C and F activities are treated as qualified trades or businesses **by default**. Enter zero here to exclude an activity you have determined is not one. |
| **DIV**, Box 5 | Selector | §199A REIT dividends, which produce a deduction with no business at all |
| **8995A**, aggregation† | Selector | Election to aggregate businesses to improve the wage and property limits |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Expecting the QBI deduction to reduce self-employment tax.
- Forgetting that the deduction is also capped by 20% of taxable income less net capital gain — a client with mostly capital gains may get far less than 20% of QBI.
- Missing §199A REIT dividends from Box 5 of a 1099-DIV.
- Failing to enter the §199A detail from a K-1, which leaves the deduction at zero with no error message.
- Claiming rental QBI without the trade-or-business analysis or the safe harbor documentation.
- Forgetting to reduce QBI by the SE tax deduction, SEHI, and retirement contributions.

### Quiz 9

1. Does the QBI deduction reduce self-employment tax? Does it reduce AGI? Where does it appear?
2. What are the two limitations that apply above the taxable income threshold, and which one applies only to service businesses?
3. Name four categories of income excluded from QBI.
4. Which three deductions reduce QBI?
5. Which 1099-DIV box produces a QBI deduction for a client who owns no business?
6. What does the rental real estate safe harbor require?

---

# PART 10 — TAX COMPUTATION

**Read:** Instructions for Form 1040, *Tax and Credits* · Tax tables and the Tax Computation Worksheet · Qualified Dividends and Capital Gain Tax Worksheet · Schedule D Tax Worksheet · Instructions for Forms 6251 and 8615

Taxable income (line 15) produces the tax on line 16. Drake computes it. The preparer's job is to know **which** method produced the number, whether it is plausible, and how to explain it.

## 10.1 Marginal vs. effective

Brackets are marginal: only the income falling inside a bracket is taxed at that bracket's rate. Clients almost universally believe otherwise, and "that raise pushed me into a higher bracket so I lost money" is a conversation you will have every year. The effective rate — total tax divided by taxable income — is always lower than the marginal rate.

The marginal rate that matters for planning is frequently **not** the bracket rate. Phaseouts stack on top of it: the Social Security phase-in (5.6), the EITC phase-out, the premium tax credit cliff and phase-out, education credit phaseouts, the QBI phase-in ranges, and the Schedule 1-A phaseouts. A client in the 22% bracket can face an effective marginal rate well above 30% across a phaseout range.

## 10.2 Which computation applies

| Situation | Method |
|---|---|
| Ordinary income only, taxable income under the table limit | Tax table |
| Ordinary income only, above the table limit | Tax Computation Worksheet |
| Any qualified dividends or net long-term capital gain | **Qualified Dividends and Capital Gain Tax Worksheet** — stacks preferential income on top of ordinary income and applies 0/15/20% rates to it |
| 28% collectibles gain, unrecaptured §1250 gain, or §1202 exclusion | **Schedule D Tax Worksheet** |
| Foreign earned income exclusion claimed | Foreign Earned Income Tax Worksheet — the exclusion does not lower the rate on remaining income |
| Child with unearned income above the threshold | **Form 8615**, kiddie tax, computed at the parent's rate |
| Lump-sum distribution, born before 1936 | Form 4972 |

The capital gain worksheets are where a hand computation and Drake diverge most often, and the divergence is nearly always the hand computation's fault.

## 10.3 Kiddie tax — Form 8615

Applies to a child with unearned income above the threshold (Appendix C) who is under 18, or 18 and did not provide more than half their support from earned income, or a full-time student aged 19–23 in the same support situation. The unearned income above the threshold is taxed at the **parent's** marginal rate, which requires the parent's return figures.

**Form 8814** is the alternative: a parent may elect to report a child's interest and dividends on the parent's return, avoiding a separate return for the child. It is available only within limits and often produces a higher total tax, because it can push the parent's AGI up and disturb their own phaseouts. Compute both.

## 10.4 The tax on preferential income

Long-term capital gains and qualified dividends are taxed at 0%, 15%, or 20% based on where they fall when stacked **on top of** ordinary income (Appendix C). Two implications worth explaining to clients:

- Ordinary income can push capital gains from the 0% bracket into 15% without itself changing brackets.
- A retiree with low ordinary income may be able to realize substantial gains at 0% — but the same realization can make Social Security taxable and raise Medicare IRMAA two years later.

## 10.5 Alternative minimum tax — Form 6251

A parallel computation with a different base: certain deductions are added back (state and local taxes, private activity bond interest), an exemption is applied and phased out at higher incomes (Appendix C), and the excess of tentative minimum tax over regular tax is added to the return.

After the TCJA changes, AMT affects far fewer returns than it once did. The remaining common triggers: **incentive stock option exercises** where the spread is an AMT preference in the year of exercise, large state tax deductions in high-tax states, and substantial private activity bond interest. An ISO exercise with no sale is the classic case — no regular tax, a large AMT liability, and a Form 8801 credit in later years.

### Drake — tax computation

| Screen / setting | Where | Detail |
|---|---|---|
| No direct entry screen for the tax itself | — | The tax is computed from taxable income |
| Setup > Options, **Always show tax computation worksheet** | Setup | Displays which method produced the number. Leave it on. |
| **6251** | Selector | AMT adjustments and preferences |
| **8801** | Selector | Credit for prior year minimum tax |
| **8615** | Selector | Kiddie tax; requires parent name, SSN, and taxable income |
| **8814** | Selector | Parent's election to report child's interest and dividends |
| **2555**† | Selector | Foreign earned income exclusion |
| **4972**† | Selector | Lump-sum distribution averaging |
| **View mode > worksheets** | CTRL+V | The capital gain worksheet, tax computation worksheet, and all supporting computations print here |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Telling a client a raise "put them in a higher bracket" as though all their income repriced.
- Using the tax table when qualified dividends or long-term gains are present.
- Filing an 8814 election without comparing it to a separate return for the child.
- Missing an ISO exercise, which produces no regular tax event and a large AMT one.
- Assuming the foreign earned income exclusion lowers the rate on the income that remains. It does not.

### Quiz 10

1. Define marginal rate and effective rate, and explain why the effective rate is always lower.
2. Name three phaseouts that can push a taxpayer's true marginal rate above their bracket rate.
3. Which worksheet applies when a return has qualified dividends, and why does the tax table give the wrong answer?
4. Who is subject to the kiddie tax, and at whose rate is the excess taxed?
5. Name the three most common remaining AMT triggers.
6. A client exercises incentive stock options and holds the shares. What is the regular tax result, the AMT result, and the later-year consequence?

---

# PART 11 — NONREFUNDABLE CREDITS (SCHEDULE 3 PART I)

**Read:** Pub 4012, Tabs G and H · Pub 17, credit chapters · Pub 503, 970, 972 successor guidance

A **nonrefundable** credit reduces tax to zero and no further. A **refundable** credit can produce a refund beyond what was paid in and sits in the payments block (Part 13). That placement is the entire difference between them, and it is why the ordering of credits on the return matters — a nonrefundable credit applied against a tax already reduced to zero is wasted.

## 11.1 Order of application

Nonrefundable credits apply in the order the form prescribes. Some carry forward when unused (the foreign tax credit, the residential clean energy credit, the mortgage interest credit, the prior-year AMT credit); most do not (the dependent care credit, the lifetime learning credit, and the saver's credit are all use-it-or-lose-it). When a client is near zero tax, the credits that expire are the ones to preserve.

## 11.2 Child tax credit and credit for other dependents — Schedule 8812

**TY2025 amounts** (Appendix C): $2,200 per qualifying child under 17 with a Social Security number valid for employment. The credit phases out above the MAGI thresholds. Up to $1,700 per child is refundable as the **additional child tax credit**, computed as 15% of earned income above the earned income floor.

**New for TY2025:** the **taxpayer** must also have a valid SSN — previously only the child's SSN was tested. On a joint return at least one spouse must have one. This will deny the credit on returns that received it in prior years.

**Credit for other dependents:** $500, nonrefundable, for dependents who fail the CTC tests — a child 17 or older, a dependent with an ITIN, a qualifying relative, or a dependent parent.

The dependents entered in Part 4 drive this entirely. If Part 4 is wrong, this is wrong, and Form 8867 due diligence applies (Part 15).

## 11.3 Child and dependent care credit — Form 2441

**Read:** Pub 503

For care expenses that allow the taxpayer (and spouse, if married) to **work or look for work**. Requirements:

- A qualifying person: a dependent under 13, or a spouse or dependent physically or mentally incapable of self-care who lived with the taxpayer more than half the year.
- **Earned income** by both spouses on a joint return. A spouse who is a full-time student or disabled is treated as having a deemed monthly earned income, which is the only way a one-earner couple gets the credit.
- The **provider's name, address, and TIN**. Without it, the credit requires proof of due diligence in trying to obtain it. "Grandma watches the kids" with no TIN and no payment is not a credit.
- Expenses capped (Appendix C) for one and for two or more qualifying persons, reduced by any employer dependent care benefits from W-2 Box 10.
- The credit percentage declines with AGI.
- **MFS is disqualified** except under the living-apart rules.

Overnight camp does not qualify; day camp does. Schooling at kindergarten level and above does not qualify; before- and after-school care does.

## 11.4 Education credits — Form 8863

**Read:** Pub 970

| | American Opportunity Credit | Lifetime Learning Credit |
|---|---|---|
| Maximum | $2,500 per **student** | $2,000 per **return** |
| Refundable | 40%, up to $1,000 | No |
| Years available | First four years of postsecondary education, four times per student | Unlimited |
| Enrollment | At least half-time in a degree program | Any course, including a single course to improve job skills |
| Felony drug conviction | Disqualifies | Does not |
| Qualified expenses | Tuition, fees, **and course materials** including books bought anywhere | Tuition and fees, and materials only if required to be paid to the institution |
| Phaseout | Appendix C | Appendix C |

Only one credit per student per year, and no credit for expenses paid with tax-free scholarship, grant, or 529 earnings. The **1098-T is not reliable** — Box 1 reports amounts paid to the institution, which may straddle academic years, may exclude books, and frequently disagrees with what the taxpayer actually paid. Work from the bursar's account statement.

A planning point worth knowing: a student who includes some scholarship in income (making it taxable) can free up expenses to claim the AOTC, which is frequently a net benefit for a student with little other income.

**MFS is disqualified** for both credits.

## 11.5 Retirement savings contributions credit — Form 8880

Up to a credit of 50%, 20%, or 10% of the first $2,000 contributed ($4,000 MFJ), on a steeply tiered AGI schedule (Appendix C) where a single dollar of additional AGI can drop the rate a full tier. Nonrefundable, no carryforward.

Contributions to a traditional or Roth IRA, 401(k), 403(b), 457, SIMPLE, SEP, and ABLE accounts qualify. **Distributions from those accounts during the testing period reduce the eligible contribution** — the testing period runs from two years before the tax year through the filing date. A client who contributed to a 401(k) and also took a distribution may get nothing.

Not available to a full-time student, a dependent of another, or a taxpayer under 18.

## 11.6 Foreign tax credit — Form 1116

Credit for income tax paid to a foreign country, computed by income category with a limitation based on the ratio of foreign source income to total income. Unused credit carries back one year and forward ten.

**De minimis exception:** if all foreign tax is from passive income reported on 1099-DIV or 1099-INT and the total is at or below $300 ($600 MFJ), the credit may be claimed directly on Schedule 3 without Form 1116. Most clients with a foreign stock fund fall here.

A **deduction** on Schedule A is the alternative and is almost always worse.

## 11.7 Energy and vehicle credits — TY2025 termination dates

This area changed mid-year and the dates matter:

| Credit | Form | TY2025 status |
|---|---|---|
| Energy efficient home improvement (§25C) | 5695 | Terminates for property placed in service after **12/31/2025** |
| Residential clean energy (§25D) — solar, wind, geothermal, battery | 5695 | Terminates for expenditures after **12/31/2025** |
| New clean vehicle (§30D) | 8936 | Terminates for vehicles acquired after **9/30/2025** |
| Previously owned clean vehicle (§25E) | 8936 | Terminates for vehicles acquired after **9/30/2025** |
| Qualified commercial clean vehicle (§45W) | 8936 | Terminates for vehicles acquired after **9/30/2025** |

For TY2025 returns these credits are still claimable for qualifying property placed in service or acquired before the applicable date. **Confirm the acquisition date, not the delivery date or the date of the contract.** For vehicle credits, the credit may also have been transferred to the dealer at the point of sale, in which case the taxpayer still files Form 8936 to reconcile.

## 11.8 The rest

| Credit | Form | Note |
|---|---|---|
| Adoption credit | 8839 | Capped (Appendix C); TY2025 makes a portion refundable for the first time; five-year carryforward for the nonrefundable part |
| Mortgage interest credit | 8396 | Requires a qualified Mortgage Credit Certificate from a state or local agency; reduces the Schedule A interest deduction by the credit amount |
| Elderly or disabled credit | Schedule R | Very restrictive income limits; rarely produces anything |
| Prior year minimum tax credit | 8801 | Recovers AMT paid on deferral items in earlier years |
| Premium tax credit | 8962 | Both a credit and a repayment — see 12.6 |

### Drake — nonrefundable credits

| Screen | Where | Detail |
|---|---|---|
| **5** | General | Schedules 2 and 3 summary entries |
| **8812** | Selector | Child tax credit, ODC, and the additional child tax credit |
| **2441** | General | Dependent care: provider name, address, TIN, amount paid per qualifying person; student/disabled spouse indicators |
| **2**, childcare expense field | General | Per-dependent care expense can be entered here and flows to 2441 |
| **8863** | Selector | Education credits, one section per student: institution name and EIN, 1098-T amounts, adjustments, half-time and prior-AOTC indicators |
| **8880** | Selector | Saver's credit; enter testing-period distributions |
| **1116** | Selector | Foreign tax credit by income category, with carryover fields |
| **5** or **1116** de minimis field† | Selector | Election to claim the small foreign tax credit without Form 1116 |
| **5695** | Selector | Residential energy credits, with carryforward for §25D |
| **8936** | Selector | Clean vehicle credits; VIN required; point-of-sale transfer reconciliation |
| **8839** | Selector | Adoption credit and carryforward |
| **8396**† | Selector | Mortgage interest credit |
| **R**† | Selector | Credit for the elderly or disabled |
| **8801** | Selector | Prior year minimum tax credit |
| **8862** | Selector | Required after a prior disallowance of CTC/ACTC/ODC or AOTC |
| **8867** / **DD1** / **DD2** | Selector | Due diligence (Part 15) |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Missing that a dependent with an ITIN gets ODC, not CTC.
- Missing the new TY2025 taxpayer SSN requirement for the child tax credit.
- Claiming the dependent care credit with no provider TIN and no documented attempt to get one.
- Claiming the dependent care credit when one spouse has no earned income and is neither a student nor disabled.
- Treating the 1098-T Box 1 amount as the qualified expense figure.
- Claiming AOTC for a fifth year, or for a student already claimed four times by anyone.
- Claiming the saver's credit without checking testing-period distributions.
- Claiming a vehicle credit for a vehicle acquired after 9/30/2025.
- Wasting expiring nonrefundable credits by not checking the order of application when tax is near zero.

### Quiz 11

1. What is the structural difference between a nonrefundable and a refundable credit, and where does each sit on the return?
2. TY2025: what is the per-child CTC amount, what is the maximum refundable portion, and what new SSN requirement applies?
3. A married couple has one earner; the other spouse is a full-time student. Can they claim the dependent care credit? What rule decides it?
4. Compare AOTC and LLC on four dimensions: maximum, per-student or per-return, refundability, and years available.
5. Why should you not rely on Form 1098-T Box 1, and what should you use instead?
6. What is the testing period for the saver's credit, and what can eliminate the credit for a client who contributed?
7. When can the foreign tax credit be claimed without Form 1116?
8. A client bought an electric vehicle in November 2025. Is the clean vehicle credit available? What date controls?

---

# PART 12 — OTHER TAXES (SCHEDULE 2)

**Read:** Instructions for Schedule 2 · Instructions for Schedule SE, Forms 5329, 8959, 8960, 8962

Schedule 2 collects taxes that are not the income tax computed in Part 10. Part I holds AMT and excess advance premium tax credit repayment, which flow up near the tax line. Part II holds everything else and flows into total tax.

## 12.1 What lands here

| Tax | Form | Trigger |
|---|---|---|
| Alternative minimum tax | 6251 | 10.5 |
| Excess advance premium tax credit repayment | 8962 | 12.6 |
| Self-employment tax | Schedule SE | 12.2 |
| Unreported Social Security and Medicare on tips | 4137 | 12.3 |
| Uncollected SS/Medicare on wages (misclassification) | 8919 | 5.1 |
| Additional tax on IRAs and other qualified plans | 5329 | 12.4 |
| Household employment taxes | Schedule H | 12.7 |
| First-time homebuyer credit repayment | 5405 | 2008 credit installments |
| Additional Medicare tax | 8959 | 12.5 |
| Net investment income tax | 8960 | 12.5 |
| Recapture items | Various | §179 recapture, education credit recapture, others |

## 12.2 Self-employment tax — Schedule SE

15.3% (12.4% Social Security + 2.9% Medicare) on **92.35%** of net self-employment earnings. The Social Security portion stops at the annual wage base (Appendix C), **reduced by W-2 wages already subject to it** — a client with substantial W-2 wages and a side business may owe only the Medicare portion. The Medicare portion has no ceiling.

One-half of the SE tax is an adjustment (6.2), which is why the deduction appears without anyone entering it.

Net earnings under $400 owe no SE tax. Church employee income has a lower threshold. Clergy have their own regime: wages are not subject to FICA but the minister pays SE tax on both salary and the housing allowance, unless an approved exemption is in place.

## 12.3 Tip taxes — Form 4137

Computes the employee's share of Social Security and Medicare on unreported and allocated tips. Note that the TY2025 tips **deduction** (Part 7) does nothing to reduce this — the tips remain fully subject to payroll tax.

## 12.4 Additional taxes on retirement accounts — Form 5329

| Situation | Tax |
|---|---|
| Early distribution, no exception | 10% (25% for SIMPLE within two years) |
| Excess IRA contribution not withdrawn | 6% per year, each year it remains |
| Excess HSA contribution | 6% per year |
| Failure to take a required minimum distribution | 25%, reduced to 10% if corrected within the correction window |
| Nonqualified HSA distribution | 20% |
| Nonqualified 529 or ESA distribution earnings | 10% |

Form 5329 is also where **exceptions** are claimed. A 1099-R with code 1 is not the end of the analysis — enter the exception code and the penalty disappears.

## 12.5 Additional Medicare tax and net investment income tax

Both are surtaxes at the same MAGI thresholds (Appendix C: $200,000 single/HOH, $250,000 MFJ, $125,000 MFS) and both are frequently missed on returns just over the line.

- **Additional Medicare tax (Form 8959)** — 0.9% on wages, compensation, and self-employment income above the threshold. Employers must withhold it above $200,000 of wages **per employer**, which means a two-earner couple can each be under the withholding trigger while jointly owing the tax. This is the most common source of an unexpected balance due for high-earning couples.
- **Net investment income tax (Form 8960)** — 3.8% on the lesser of net investment income or MAGI over the threshold. Net investment income includes interest, dividends, capital gains, rents, royalties, annuities, and passive business income. It excludes wages, self-employment income, active business income, tax-exempt interest, and qualified retirement distributions. Certain expenses allocable to investment income reduce the base.

## 12.6 Premium tax credit reconciliation — Form 8962

**Read:** Pub 974

If anyone on the return had Marketplace coverage, **Form 1095-A is mandatory** and Form 8962 must reconcile the advance credit paid to the insurer against the credit actually allowed based on final household income and family size.

- If the actual credit exceeds the advance, the excess is a **refundable credit**.
- If the advance exceeded the actual credit, the excess is **repaid** on Schedule 2, subject to a repayment cap that increases with income and disappears entirely at higher incomes.

A return with Marketplace coverage filed without Form 8962 will be rejected or held. This is one of the most common causes of a delayed refund, and the client frequently does not mention the coverage or produce the 1095-A unless asked directly.

**Shared policy allocation** — where a policy covers people on more than one tax return, such as a divorced couple or a young adult on a parent's policy — requires an allocation percentage agreed between the parties. Get it in writing.

## 12.7 Household employment taxes — Schedule H

Required when the taxpayer paid a household employee (nanny, housekeeper, caregiver) cash wages above the annual threshold, or paid $1,000 or more in any calendar quarter, triggering FUTA. The distinction between an employee and an independent contractor turns on control, and a nanny is nearly always an employee. Clients strongly resist this conclusion.

### Drake — other taxes

| Screen | Where | Detail |
|---|---|---|
| **5** | General | Schedule 2 summary and write-in entries |
| **SE** | Selector | Schedule SE, optional methods, clergy, exempt-notary and exempt-clergy indicators |
| **4137** | Selector | Unreported tip taxes |
| **8919** | Selector | Uncollected SS/Medicare on misclassified wages, with reason code |
| **5329** | Selector | Additional taxes and exception codes; separate parts for IRAs, HSAs, MSAs, Coverdell, 529 |
| **8959** | Selector | Additional Medicare tax; pulls wages and SE income automatically |
| **8960** | Selector | Net investment income tax, with fields for allocable deductions |
| **95A** | **Health Care** | Form 1095-A entry, month by month: enrollment premium, SLCSP, advance credit. **One 95A screen per 1095-A**, differentiated by the Marketplace-assigned policy number — if that number exceeds 15 characters, enter only the **last 15**. |
| **8962** | **Health Care** | Premium tax credit reconciliation, shared policy allocation, alternative calculation for the year of marriage. Overrides available for lines 4 and 11–23, which otherwise flow from 95A. |
| **H**† | Selector | Schedule H, household employment taxes |
| **5405** | Selector | First-time homebuyer credit repayment |
| **6251** | Selector | AMT |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Filing a return with Marketplace coverage and no Form 8962.
- Entering the 1095-A annual totals instead of the monthly detail when premiums or SLCSP changed during the year.
- Missing the additional Medicare tax on a two-earner couple where neither employer was required to withhold.
- Missing NIIT on a return just over the threshold with substantial capital gains.
- Accepting a code 1 distribution as automatically penalized without checking 5329 exceptions.
- Treating a household worker as a contractor.
- Forgetting that the Social Security portion of SE tax is reduced by W-2 wages already taxed.

### Quiz 12

1. What percentage of net self-employment earnings is subject to SE tax, and why is it not 100%?
2. A client has $170,000 of W-2 wages and $30,000 of net self-employment income. Which portions of SE tax apply and why?
3. Two spouses each earn $160,000. Do their employers withhold additional Medicare tax? Do they owe it? Explain the gap.
4. What is included in net investment income, and name four things that are excluded.
5. What happens to a return with Marketplace coverage filed without Form 8962?
6. A 1099-R shows code 1 for a distribution used to pay $12,000 of qualifying higher education expenses from an IRA. What is the result and which form gets you there?
7. When is Schedule H required?

---

# PART 13 — PAYMENTS AND REFUNDABLE CREDITS

**Read:** Instructions for Form 1040, *Payments* · Pub 505 · Pub 596

Everything in the payments block behaves like money already paid, whether it was actually paid or not. That is the definition of a refundable credit.

## 13.1 Withholding

| Source | Where reported |
|---|---|
| W-2 Box 2 | Line 25a |
| Form 1099 (all types — R, INT, DIV, G, NEC, MISC, B, K) | Line 25b |
| Schedule K-1, Form W-2G, Form 8959 excess | Line 25c |

Withholding is credited as though paid evenly throughout the year regardless of when it was actually withheld, which makes a late-year withholding increase a legitimate tool for curing an underpayment penalty (14.4).

**Backup withholding** at 24% appears on 1099s when a payee failed to furnish a correct TIN. It is a payment like any other and is frequently overlooked in the 1099 detail.

## 13.2 Estimated tax payments

Four installments, due April 15, June 15, September 15, and January 15 of the following year. Enter the **amounts actually paid and the dates paid** — not the amounts that were supposed to be paid. Drake's underpayment computation (Form 2210) depends on the dates.

Also entered here: an **overpayment applied from the prior year**, which counts as paid on the first installment date, and any payment made with an extension request.

## 13.3 Refundable credits

| Credit | Form | Note |
|---|---|---|
| Earned income credit | Schedule EIC | 13.4 |
| Additional child tax credit | Schedule 8812 | The refundable remainder of the CTC (11.2) |
| American opportunity credit, refundable portion | 8863 | 40%, capped at $1,000 per student |
| Premium tax credit, net | 8962 | 12.6 |
| Excess Social Security tax withheld | — | 13.5 |
| Credit for federal tax on fuels | 4136 | Rare on individual returns |
| Adoption credit, refundable portion | 8839 | New for TY2025 |
| Amount paid with extension | — | Form 4868 payment |

## 13.4 Earned income credit

**Read:** Pub 596

The largest refundable credit and the one with the highest error rate. It requires:

- **Earned income** — wages, self-employment income, and certain disability payments. Not unemployment, not pensions, not investment income, not alimony.
- **Investment income** at or below the annual limit (Appendix C). One dollar over and the entire credit is gone. This is a cliff, not a phaseout.
- A valid **SSN valid for employment** for the taxpayer, spouse, and every qualifying child.
- Filing status other than MFS (except under the living-apart rules).
- No foreign earned income exclusion.
- For a taxpayer with no qualifying children: age between 25 and 64, not a dependent of another, and residence in the US for more than half the year.

**Qualifying child for EITC** uses relationship, age, residency, and joint return — but **not** the support test. A child can be an EITC qualifying child without being the taxpayer's dependent, which is what the "not a dependent but qualifies for EIC" indicator on Drake screen 2 exists for.

The credit rises, plateaus, and phases out with income, so a self-employed client who overstates expenses can reduce their refund, and one who understates them can increase it. That asymmetry is exactly why Form 8867 due diligence exists (Part 15).

**Combat pay election:** nontaxable combat pay (W-2 Box 12 code Q) may be included in earned income for EITC purposes if it produces a larger credit. Compute both ways.

**PATH Act:** the IRS may not issue a refund on a return claiming EITC or ACTC before mid-February. Set the expectation at the time of filing.

## 13.5 Excess Social Security tax

A taxpayer with two or more employers whose combined Social Security wages exceeded the wage base has overpaid Social Security tax. The excess is a refundable credit. This only applies **per person** — combining spouses' wages on a joint return to manufacture an excess is a common error, and it is why the TS box on the W2 screen matters.

An employer that over-withheld on its own has to refund it; the credit does not apply.

### Drake — payments and refundable credits

| Screen | Where | Detail |
|---|---|---|
| **W2** / 1099 screens | Various | Withholding is captured at the source document, not entered separately |
| **ES** | Selector | Estimated payments made with dates, prior-year overpayment applied, extension payment, and next-year estimate computation |
| **EIC**† | Selector | Earned income credit worksheets and the combat pay election |
| **2**, EIC indicators | General | Qualifying child for EITC, including non-dependents |
| **8812** | Selector | Additional child tax credit |
| **8863** | Selector | Refundable AOTC portion |
| **8962** | Selector | Net premium tax credit |
| **8959** | Selector | Excess additional Medicare tax withheld flows to payments |
| **4136**† | Selector | Fuel tax credit |
| **8867** / **DD1** | Selector | Due diligence on EITC, CTC/ACTC/ODC, AOTC, and HOH (Part 15) |
| Setup > Options, **Always show reason for no EIC** | Setup | Prints the disqualifying condition rather than silently omitting the credit |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Entering estimated payments without dates, which produces a wrong Form 2210.
- Missing the investment income cliff for EITC.
- Combining spouses' wages to claim excess Social Security tax.
- Missing backup withholding buried in 1099 detail.
- Failing to warn an EITC/ACTC client about the PATH Act refund delay.
- Forgetting the combat pay election, which can be worth hundreds.
- Overlooking that a child can be an EITC qualifying child without being a dependent.

### Quiz 13

1. Why is a refundable credit placed in the payments block rather than the credits block?
2. Withholding is treated as paid when? Why does that make late-year withholding a tool?
3. Name four types of income that are **not** earned income for EITC.
4. What is the EITC investment income limit and what makes it different from a phaseout?
5. Which EITC test differs from the dependency qualifying child tests, and what does that make possible?
6. Two spouses each earned $150,000 from one employer. Is there excess Social Security tax? Explain.
7. What is the PATH Act refund timing rule and which credits trigger it?

---

# PART 14 — REFUND, BALANCE DUE, AND NEXT YEAR

**Read:** Instructions for Form 1040, *Refund* and *Amount You Owe* · Pub 505 · Instructions for Form 2210

## 14.1 The last arithmetic

Total payments minus total tax. Positive is an overpayment; negative is a balance due. Everything on the return before this exists to make those two numbers right.

## 14.2 Refund delivery

- **Direct deposit** is faster and safer. Verify the routing and account numbers by reading them off a check or a bank document, not from the client's memory. A wrong account number on an accepted return is very difficult to recover.
- The account must be in the taxpayer's name. Depositing a refund into a preparer's account is prohibited.
- **Form 8888** splits a refund across up to three accounts, or buys savings bonds.
- **Applying the overpayment to next year** is entered here and is irrevocable once the return is filed.
- The IRS limits the number of refunds deposited to a single account (three), after which refunds convert to paper checks.

## 14.3 Balance due and payment options

- **Electronic funds withdrawal** scheduled with the e-filed return, on any date up to the deadline.
- **IRS Direct Pay, EFTPS, or card** — the client pays directly.
- **Form 9465 installment agreement**, or the online payment agreement, which is usually faster and cheaper.
- Filing on time and paying late is far less expensive than filing late: the failure-to-file penalty is 5% per month, the failure-to-pay penalty is 0.5% per month. **Always file on time even when the client cannot pay.**
- An **extension (Form 4868)** extends the time to file, never the time to pay. Interest and failure-to-pay penalties run from the original due date regardless.

## 14.4 Estimated tax and the underpayment penalty

The underpayment penalty applies unless a **safe harbor** is met:

- Tax due after withholding and credits is under $1,000, **or**
- Payments equal at least **90%** of the current year's tax, **or**
- Payments equal at least **100%** of the prior year's tax — **110%** if prior-year AGI exceeded $150,000 ($75,000 MFS).

The prior-year safe harbor is the reliable one, because it is a known number.

**Form 2210** computes the penalty and offers the **annualized income installment method** for clients whose income was uneven — a large fourth-quarter capital gain, a mid-year business start, a year-end bonus. Annualizing can eliminate a penalty entirely and is under-used.

**Next-year estimates** should be computed for every client with self-employment income, significant investment income, retirement distributions without withholding, or a balance due this year. Producing vouchers is part of finishing the return, not a separate service.

An alternative worth raising: adjusting W-2 withholding on Form W-4, or requesting withholding on a pension (Form W-4P) or Social Security (Form W-4V), which is treated as paid evenly and can cure a shortfall late in the year.

### Drake — finishing the money

| Screen | Where | Detail |
|---|---|---|
| **DD** | Selector | Direct deposit: routing number, account number, account type, and a re-entry verification field |
| **8888** | Selector | Refund split across accounts or savings bond purchase |
| **PMT** | Selector | Electronic funds withdrawal — account, amount, and requested payment date |
| **ES** | Selector | Estimated payments made, overpayment applied to next year, and next-year estimate computation and voucher options |
| **2210** | Selector | Underpayment penalty, waiver requests, and the annualized income method |
| **9465** | Selector | Installment agreement request |
| **4868**† | Selector | Extension request and payment |
| **W4**† | Selector | Withholding worksheet for the client's employer |
| **BILL** / Setup > Pricing | Setup | Invoice for the engagement |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Keying a routing or account number from memory or from a deposit slip (which often carries a different routing number than a check).
- Scheduling an electronic funds withdrawal for a date after the deadline.
- Applying an overpayment to next year without asking the client.
- Not running the annualized method for a client with lumpy income.
- Telling a client an extension gives them more time to pay.
- Filing late because the client cannot pay, which multiplies the penalty tenfold.

### Quiz 14

1. State the three safe harbors that avoid the underpayment penalty, including the high-income variation.
2. What does an extension extend, and what does it not?
3. Compare the failure-to-file and failure-to-pay penalty rates. What is the practical instruction that follows?
4. Which method on Form 2210 helps a client with a large fourth-quarter capital gain, and why?
5. Why is increasing year-end withholding more effective than making a fourth-quarter estimated payment of the same size?
6. A client wants their refund deposited into their business account and their spouse's account. What are the constraints?

---

# PART 15 — DUE DILIGENCE

**Read:** Form 8867 and instructions · Circular 230 §10.22 (diligence), §10.34 (standards), §10.33 (best practices) · §6695(g)

## 15.1 What is required

A paid preparer must complete **Form 8867** for any return claiming:

- Earned income credit
- Child tax credit, additional child tax credit, or credit for other dependents
- American opportunity credit
- Head of household filing status

The **§6695(g) penalty is per credit, per return**. A single return claiming EITC, CTC, AOTC, and HOH carries four separate penalty exposures. The penalty applies for failing to meet the requirements even when the credit turns out to be correct — the obligation is to the process, not only to the answer.

Four requirements, all of which must be satisfied:

1. **Complete and submit Form 8867** with the return.
2. **Compute the credit** using the worksheets or equivalent documentation, and keep them.
3. **Know or have reason to know** — make reasonable inquiries when information appears incorrect, inconsistent, or incomplete, and **contemporaneously document** the inquiries and the answers.
4. **Keep records** for three years: the 8867, the worksheets, the documents relied on, and a record of how and when they were obtained.

## 15.2 The knowledge requirement

This is the requirement that actually gets preparers penalized. A preparer may not ignore the implications of information already known, and may not accept implausible, inconsistent, or incomplete information without asking.

Examples of information that requires an inquiry and documentation of the answer:

- A Schedule C with round-number receipts, no expenses, and income landing precisely in the EITC plateau.
- A client claiming a child at an address different from the address the client gives for themselves.
- A 22-year-old claiming three children.
- A head of household claim where the taxpayer's income could not plausibly have covered half the cost of the home.
- A dependent whose relationship or residency cannot be explained.
- A cash business with no records at all.

Document the question asked and the answer received, in the file, at the time. A note written after an examination notice arrives is worth nothing.

## 15.3 The other obligations

- **PTIN** — required to prepare any return for compensation, renewed annually.
- **Signature** — the preparer must sign the return and include the PTIN and firm EIN.
- **Copy to the taxpayer** — furnish a complete copy no later than the time the return is presented for signature.
- **Retention** — retain a copy or a list of returns prepared.
- **§6694** — penalties for understatement due to an unreasonable position (no substantial authority) or willful or reckless conduct.
- **Circular 230 §10.34** — a preparer may not sign a return containing a position lacking a reasonable basis, or an unreasonable position, or that is a willful attempt to understate liability.
- **E-file mandate** — a preparer expecting to file 11 or more covered returns in a year must e-file.

## 15.4 Drake — due diligence

| Screen | Where | Detail |
|---|---|---|
| **8867** | **General** | Paid preparer's due diligence checklist, covering the EIC, AOTC, and CTC/ACTC/ODC interview questions. Where a covered credit is present, the applicable questions **must** be completed before the return will e-file. |
| **8867 > Overrides** | Tab | Overrides where the automatic answers are wrong |
| **DD1** | **General** | Due diligence questions and documentation, including the head of household section. Provides entry for **three children**, matching Schedule EIC. |
| **DD2** | **General** | Additional due diligence documentation |
| **2 > Due Diligence** | Tab | Per-dependent due diligence, including the indicator that the taxpayer holds Form 8332 or a substantially similar statement and qualifies for the child tax credit |
| **NOTE** | Selector | Contemporaneous notes attached to the return |
| **ADMN**† | Selector | Reviewer sign-off and workflow tracking |
| **PDF** | Selector | Attach scanned supporting documents to the return file |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Completing Form 8867 at the end as a formality instead of letting it drive the intake questions.
- Answering "yes" to the documentation questions without the documents.
- Treating a correct credit as a defense to a due diligence penalty. It is not.
- Failing to document an inquiry contemporaneously.

### Quiz 15

1. Which four items trigger Form 8867?
2. What is the structure of the §6695(g) penalty, and how many exposures does a return claiming EITC, CTC, AOTC, and HOH carry?
3. List the four due diligence requirements.
4. A client presents a Schedule C with $18,000 of receipts, no expenses, and two qualifying children. What is the concern, what must you do, and what must you record?
5. If the credit turns out to be correct but the documentation is absent, is the penalty avoided?

---

# PART 16 — QUALITY REVIEW, SIGNATURES, AND TRANSMISSION

**Read:** Pub 4491, *Quality Review* · Pub 1345, *Handbook for Authorized IRS e-file Providers* · Form 8879 instructions

## 16.1 Calculate and view first

Nothing is reviewed in data entry. Press **CTRL+V** to calculate and view. Drake produces three categories of message, and they are not equivalent:

| Message type | Meaning |
|---|---|
| **EF Messages** | Blocking. The return cannot be transmitted until each is cleared. Each message names the screen and field. |
| **Return Notes** | Informational. Something the preparer should confirm, often a missed election or an unusual result. Not blocking, and frequently where the real error is. |
| **Fed/State Warnings** | Conditions that will not stop transmission but frequently indicate a data entry error. |

Read all three. Preparers who clear EF messages and ignore return notes transmit wrong returns that the software already flagged.

## 16.2 The review itself

Review against the source documents, not against the data entry screens — comparing data entry to data entry only confirms that you typed what you typed.

A workable sequence:

1. **Document count.** Every document in the file appears on the return; every item on the return has a document. Use the prior-year comparison to find what is missing.
2. **Page 1 identity block.** Names, SSNs, DOBs, address, filing status, dependents, digital asset question.
3. **Income.** Tie each line to a document. Confirm the qualified dividend split, the taxable-vs-gross retirement lines, and the Social Security computation.
4. **AGI reasonableness.** Compare to prior year. Explain any large swing.
5. **Deduction.** Confirm the standard-vs-itemized decision and, in TY2025, whether the higher SALT cap changed it.
6. **Credits.** Confirm each credit generated, and for each one that did **not** generate, know why. Setup > Options, "always show reason for no EIC," makes this explicit for EITC.
7. **Other taxes.** SE tax, NIIT, additional Medicare tax, PTC repayment.
8. **Payments.** Every withholding amount traced to a document; estimated payments confirmed against the client's records, not their memory.
9. **Prior-year comparison.** Drake prints a two-year comparison. Any line that moved materially either has an explanation or is an error.
10. **The plausibility test.** Does the refund or balance due make sense given what the client did this year? If it is surprising, find out why before the client does.

## 16.3 Diagnostics worth running

- **Prior-year comparison** — the single best error detector on a returning client.
- **Two-year tax summary** and the **tax computation worksheet**.
- **Flagged fields (F3)** — clear every one.
- **Split return** (MFJ vs. two MFS) when the answer is not obvious.
- **State returns** — confirm the correct states generated and no extras.

## 16.4 Signatures and authorization

- **Form 8879** is the taxpayer's authorization for the ERO to transmit. It must be signed **after** the taxpayer reviews the return and **before** transmission. It is not filed with the IRS; it is retained for three years.
- Both spouses sign on a joint return.
- The **PIN** screen records signature dates and the practitioner PIN. A signature date after the transmission date is a Pub 1345 violation.
- A **deceased taxpayer's** return is signed by the personal representative or surviving spouse, and **Form 1310** may be required to claim the refund.
- A return signed under a **power of attorney** requires the POA attached.
- Furnish the taxpayer a complete copy of the return.

## 16.5 Transmission and acknowledgment

Transmit, then **confirm the acknowledgment**. A transmitted return is not a filed return. Check acks the next business day and resolve rejects immediately — a rejected return that is never corrected was never filed, and the client will not know.

Common rejects and their causes:

| Reject pattern | Cause |
|---|---|
| Name/SSN mismatch | Name does not match the SSA record — often a recent marriage |
| Duplicate SSN | The SSN was already used on a filed return; identity theft or a dependent claimed elsewhere |
| Dependent SSN already claimed | Another return claimed the same dependent first; paper file with documentation |
| Missing IP PIN / wrong IP PIN | 1.2 |
| Missing Form 8962 | Marketplace coverage without reconciliation (12.6) |
| Prior-year AGI mismatch | Self-select PIN validation; use the AGI from the originally filed prior-year return |
| Form 8862 required | Prior disallowance not addressed |

A return rejected on the due date is generally treated as timely if it is corrected and retransmitted within the perfection period, but do not rely on that as a plan.

### Drake — finishing and filing

| Screen / tool | Where | Detail |
|---|---|---|
| **CTRL+V** | Toolbar | Calculate and view; produces EF messages, notes, and warnings |
| **EF** | Selector | Which federal and state returns to transmit, extension and amended selections, and suppression of specific returns |
| **PIN** | Selector | Signature dates, taxpayer/spouse PINs, ERO PIN, Form 8879 |
| **PDF** | Selector | Attachments required by the schema or by an election |
| **1310**† | Selector | Refund claim for a deceased taxpayer |
| **2848** / **8821**† | Selector | Power of attorney and information authorization |
| **EF > Transmit/Receive** | Menu | Transmission and acknowledgment retrieval |
| **EF > Search EF Database** | Menu | Ack status, reject codes, and history for every return |
| **Reports > Return Status** | Menu | Firm-wide view of what has been transmitted and acknowledged |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

**Traps.**

- Transmitting before running View and reading the messages.
- Clearing EF messages while ignoring return notes.
- Obtaining the 8879 signature before the client has seen the return, or dating it after transmission.
- Assuming transmission is filing.
- Not checking acknowledgments the next business day.
- Reviewing the data entry screens instead of the printed return.

### Quiz 16

1. Name the three categories of message Drake produces on calculation. Which are blocking, and which most often contain the real error?
2. Why must review be performed against source documents rather than data entry screens?
3. When must Form 8879 be signed relative to the client's review and to transmission, and where is it filed?
4. What is the difference between a transmitted return and a filed return?
5. A return rejects for "dependent SSN already used." What happened, and what is the path forward?
6. Which Setup option tells you why a credit did not generate, and why does that matter in review?

---

# PART 17 — AFTER THE RETURN

**Read:** Instructions for Form 1040-X · Pub 556, *Examination of Returns, Appeal Rights, and Claims for Refund* · Pub 1, *Your Rights as a Taxpayer*

## 17.1 Amended returns — Form 1040-X

File when income, deductions, credits, filing status, or dependents were wrong. Do **not** file for a math error the IRS will correct itself, and do not file before the original return has been processed.

- **Statute for a refund claim:** three years from the filing date, or two years from the date the tax was paid, whichever is later.
- Form 1040-X can be e-filed for recent years.
- Column A is the original figures, column C is the corrected figures, column B is the difference, and **Part III requires a clear written explanation** — write it as though the reader has none of the context, because they do not.
- A change in filing status from MFJ to MFS is only permitted before the original due date. MFS to MFJ is permitted within the statute.
- Amending the federal return usually requires amending the state return.

## 17.2 Superseding returns

A return filed after the original but before the due date (including extensions) **supersedes** rather than amends it. This is cleaner than a 1040-X and is available more often than preparers realize, including for elections that must be made on a timely filed return.

## 17.3 Notices

Read what the notice actually says before responding. The common ones:

| Notice | Meaning |
|---|---|
| CP2000 | Underreported income matching — a proposed change, not a bill. It is frequently wrong, particularly on securities basis. Respond by the deadline with the correction. |
| CP14 | Balance due |
| CP12 / CP11 | The IRS changed the return and there is a refund adjustment or a balance due |
| Letter 5071C / 4883C | Identity verification required before the return will process |
| CP75 | EITC examination and documentation request |

A CP2000 for unreported securities sales is a routine event when a client omitted a 1099-B — the IRS proposes tax on the full proceeds with zero basis. The response supplies the basis, and the actual liability is usually a fraction of the proposal.

## 17.4 Records

- Advise the client to retain records for **three years** ordinarily, **six years** if income was understated by more than 25%, and **indefinitely** for basis records: home improvements, investment purchases, IRA Form 8606 basis, depreciation schedules, and carryover schedules.
- The preparer retains the return copy or list, the 8879, the due diligence file, and the supporting documents for the applicable periods.

## 17.5 Carryforward hygiene

Before closing the engagement, confirm that the following are recorded so they survive to next year:

capital loss carryover · charitable contribution carryover · passive activity loss carryover (Form 8582) · NOL · §179 carryover · at-risk carryover · depreciation basis and accumulated depreciation · Form 8606 IRA basis · AMT credit (Form 8801) · foreign tax credit carryover · residential clean energy credit carryover · adoption credit carryover · investment interest expense carryover · state overpayment applied · installment sale balances.

This list is the reason a returning client must be carried forward rather than re-created (2.2).

### Drake — after the return

| Screen | Where | Detail |
|---|---|---|
| **X** | Selector | Form 1040-X. Use the **auto-fill** function to pull the original column A figures from the return as originally prepared in Drake, or key them directly. Then **leave the X screen** and make the corrections in normal data entry — that is what produces the amended column. |
| **EF** | Selector | Check the **1040-X** box to e-file the amended return, and select the state amended return from the drop list where the state supports it. Form 1040-X e-files for the current year and two prior years. Calculate and confirm a green check mark on Form 1040-X before transmitting. |
| **PDF** | Selector | Attach supporting documentation |
| **9465** | Selector | Installment agreement following a balance due |
| **2848** / **8821**† | Selector | Representation and information authorization |
| **Tools > Repair Index / Backup** | Menu | File maintenance |
| **Last Year Data > Update** | Menu | Prior-year carryforward into the new year — the mechanism that preserves everything in 17.5 |

Screen help: F1 · https://kb.drakesoftware.com/kb/Drake-Tax/20051.htm

### Quiz 17

1. What is the statute of limitations for a refund claim, stated both ways?
2. What is a superseding return and when is it available?
3. When may filing status be changed from MFJ to MFS, and from MFS to MFJ?
4. A client receives a CP2000 proposing tax on $60,000 of securities proceeds. What is the likely issue and what is the response?
5. Name five records a client should keep indefinitely.
6. Name eight carryovers that must survive into next year.

---

# APPENDIX A — SOURCE DOCUMENT TO DRAKE SCREEN

| Document | Reports | Drake screen | Guide section |
|---|---|---|---|
| W-2 | Wages, withholding, deferrals, HSA, dependent care | **W2** | 5.1 |
| W-2G | Gambling winnings | **W2G** | 5.13 |
| 1099-INT | Interest, tax-exempt interest, early withdrawal penalty | **INT** | 5.3 |
| 1099-OID | Original issue discount | **INT**† | 5.3 |
| 1099-DIV | Ordinary/qualified dividends, capital gain distributions, §199A | **DIV** | 5.4 |
| 1099-B | Securities sales | **8949** / **D** | 5.7 |
| 1099-R | Retirement distributions | **1099** | 5.5 |
| SSA-1099 / RRB-1099 | Social Security, railroad retirement | **SSA** / **RRB**† | 5.6 |
| 1099-G | Unemployment, state refunds | **99G** | 5.12 |
| 1099-NEC | Nonemployee compensation | **NEC** → Schedule **C** | 5.8 |
| 1099-MISC | Rents, royalties, other income, prizes | **99M** | 5.8, 5.9, 5.13 |
| 1099-K | Payment card and third-party network | **99K**† | 5.8 |
| 1099-C | Cancellation of debt | **99C**† / **982** | 5.13 |
| 1099-S | Real estate sale proceeds | **HOME**† / **4797** | 5.7 |
| 1099-SA | HSA/MSA distributions | **8889** / **8853** | 6.4 |
| 1099-Q | Education account distributions | Education worksheet† | 11.4 |
| 1099-LTC | Long-term care benefits | **8853** | 8.2 |
| 1098 | Mortgage interest, points, property tax | **1098**† → **A** | 8.4 |
| 1098-E | Student loan interest | **4** | 6.7 |
| 1098-T | Tuition | **8863** | 11.4 |
| 1098-C | Vehicle donation | **8283** | 8.5 |
| 1095-A | Marketplace health coverage | **95A**† → **8962** | 12.6 |
| 1095-B / 1095-C | Other coverage | Informational; no entry | — |
| K-1 (1065) | Partnership | **K1P** | 5.10 |
| K-1 (1120-S) | S corporation | **K1S** | 5.10 |
| K-1 (1041) | Estate or trust | **K1F** | 5.10 |
| Form 13614-C | Intake | No screen; drives everything | Part 1 |
| Form 8332 | Release of dependency | **8332** + **PDF** | 4.3 |
| Closing disclosure / settlement statement | Home purchase or sale | **HOME**† / **A** | 5.7, 8.4 |
| Brokerage composite | Multiple of the above | **INT**, **DIV**, **8949** | 5.3, 5.4, 5.7 |

Drake also ships a **DOCS**† screen — a source document guide for 1098 and 1099 series forms. Worth opening once.

---

# APPENDIX B — DRAKE SCREEN INDEX

Screens marked **†** are still unconfirmed against a Drake source — verify these against the installed year. Everything unmarked was confirmed via the Drake knowledge base (see Appendix H). Any screen can be reached by typing its code into the selector field; tab assignments are noted where confirmed.

**The spine (General tab)**

| Code | Holds |
|---|---|
| **1** | Taxpayer/spouse data, filing status, DOB, blindness, address, digital assets, designee |
| **2** | Dependents |
| **3** | Additional income — Schedule 1 Part I |
| **4** | Adjustments — Schedule 1 Part II |
| **5** | Additional taxes and credits — Schedules 2 and 3 |
| **1A** | Additional deductions — Schedule 1-A (new TY2025), **General tab** |

**Income**

`W2` · `W2G` · `INT` · `DIV` · `B` · `1099` · `SSA` · `RRB`† · `99G` · `99M` · `NEC` · `99K`† · `99C`† · `8949` · `D` · `D2` · `HOME`† · `C` · `E` · `F` · `4835` · `K1P` · `K1S` · `K1F` · `4797` · `6252` · `8824`† · `6781`† · `8814` · `8815` · `4137` · `8919` · `4852`

**Business support**

`4562` · `6`–`9` (depreciation overrides — avoid) · `AUTO`† · `8829` · `SE` · `SEHI` · `SEP`† · `6198` · `8582` · `461`† · `7203`† · `8995` · `8995A` · `K199` (Adjustments tab)

**Adjustments**

`4` · `8889` · `HSA`† · `8853` · `SEHI` · `LTC`† · `SEP`† · `8606` · `ROTH` · `2106` · `3903`†

**Deductions**

`A` · `STAX` · `1098` · `8283` · `4952` · `4684`†

**Credits**

`8812` · `2441` · `8863` · `8880` · `1116` · `5695` · `8936` · `8839` · `8396`† · `R`† · `8801` · `8862`

**Health care tab**

`95A` · `8962`

**Other taxes**

`6251` · `5329` · `8959` · `8960` · `H`† · `5405` · `4137` · `8919`

**Payments and filing**

`ES` · `DD` · `8888` · `PMT` · `2210` · `9465` · `4868`† · `PIN` · `EF` · `X`

**Due diligence and administration**

`8867` · `DD1` · `DD2` · `IDS`† · `USE` · `CONS` · `DISC` · `MISC` · `NOTE` · `PDF` · `PRNT` · `ADMN`† · `PREP`† · `1310`† · `2848`† · `8821`† · `8958`† · `2120`† · `8332` · `8938` · `FBAR/114`†

---

# APPENDIX C — TY2025 FIGURES

**Verify every figure in this table against the IRS instructions or Rev. Proc. before it goes in front of a client.** This is the only place in the guide where amounts live, so this is the only table that has to be updated when they change.

The 2025 inflation-adjusted amounts come from **Rev. Proc. 2024-40**; the 2026 amounts, when you need them, are in **Rev. Proc. 2025-32**.

Rows marked ✓ have been checked against a published source. Unmarked rows are still to be confirmed.

**Standard deduction** ✓

| Status | Amount |
|---|---|
| Single / MFS | $15,750 ✓ |
| MFJ / Qualifying surviving spouse | $31,500 ✓ |
| Head of household | $23,625 ✓ |
| Additional, age 65 or blind — unmarried | $2,000 per condition ✓ |
| Additional, age 65 or blind — married/QSS | $1,600 per condition, per person ✓ |
| Combined, both 65 **and** blind | $4,000 unmarried / $3,200 per qualifying married individual ✓ |
| Dependent of another | Greater of $1,350 or earned income + $450, capped at the regular amount |

**Schedule 1-A (TY2025–TY2028)** ✓

| Deduction | Cap | MAGI phaseout begins |
|---|---|---|
| Qualified tips | $25,000 ✓ | $150,000 / $300,000 MFJ ✓ |
| Qualified overtime (FLSA premium only) | $12,500 / $25,000 MFJ ✓ | $150,000 / $300,000 MFJ ✓ |
| Car loan interest (new, US-assembled, VIN required) | $10,000 ✓ | $100,000 / $200,000 MFJ ✓ |
| Senior deduction (per person 65+) | $6,000 ✓ | $75,000 / $150,000 MFJ ✓ |

**Senior deduction age test.** For TY2025 the test is stated as **born before January 2, 1961**, and a valid SSN is required. Use the date test rather than "turns 65 during the year" — they agree, but the date is what the form asks.

**Itemized deductions**

| Item | Figure |
|---|---|
| Medical floor | 7.5% of AGI |
| SALT cap | $40,000 ($20,000 MFS), phasing down above $500,000 MAGI, not below $10,000 |
| Mortgage acquisition debt limit | $750,000 ($375,000 MFS); $1,000,000 if incurred before 12/16/2017 |
| Charitable — cash to public charities | 60% of AGI |
| Charitable — appreciated capital gain property | 30% of AGI |
| Charitable carryforward | 5 years |
| Written acknowledgment required at | $250 |
| Form 8283 Section A / Section B + appraisal | Over $500 / over $5,000 |

**Credits**

| Credit | Figure |
|---|---|
| Child tax credit | $2,200 per qualifying child under 17 with a work-eligible SSN |
| Additional child tax credit (refundable) | Up to $1,700 per child; 15% of earned income above the floor |
| CTC phaseout | $400,000 MFJ / $200,000 all others |
| Credit for other dependents | $500 |
| Dependent care expense cap | $3,000 one qualifying person / $6,000 two or more; credit rate up to 35% |
| American opportunity credit | $2,500 per student; 40% refundable up to $1,000; phaseout $80,000–$90,000 / $160,000–$180,000 |
| Lifetime learning credit | $2,000 per return; same phaseout range |
| Saver's credit | 50/20/10% of up to $2,000 ($4,000 MFJ), tiered by AGI |
| Foreign tax credit without Form 1116 | $300 / $600 MFJ, passive income only |
| Adoption credit | $17,280, with a refundable portion new for TY2025; phaseout begins around $259,190 MAGI |
| EITC maximum | Roughly $649 (no children) / $4,328 (1) / $7,152 (2) / $8,046 (3+) |
| EITC investment income limit | $11,950 — a cliff, not a phaseout |

**Retirement and health**

| Item | Figure |
|---|---|
| IRA contribution limit | $7,000, plus $1,000 catch-up at 50 |
| IRA deduction phaseout — covered by a plan | $79,000–$89,000 single/HOH; $126,000–$146,000 MFJ |
| IRA deduction phaseout — not covered, spouse covered | $236,000–$246,000 |
| IRA deduction phaseout — MFS | $0–$10,000 |
| Roth contribution phaseout | $150,000–$165,000 single; $236,000–$246,000 MFJ; $0–$10,000 MFS |
| HSA contribution limit | $4,300 self-only / $8,550 family, plus $1,000 catch-up at 55 |
| HDHP minimum deductible | $1,650 self-only / $3,300 family |
| HDHP out-of-pocket maximum | $8,300 self-only / $16,600 family |
| Educator expense | $300 per educator ($600 MFJ if both qualify) |
| Student loan interest | $2,500 cap; phaseout $85,000–$100,000 single / $170,000–$200,000 MFJ; MFS disallowed |

**Rates and thresholds**

| Item | Figure |
|---|---|
| Social Security wage base | $176,100 |
| SE tax | 15.3% on 92.35% of net earnings; $400 filing threshold |
| Additional Medicare tax | 0.9% above $200,000 single/HOH, $250,000 MFJ, $125,000 MFS |
| Net investment income tax | 3.8% at the same thresholds |
| Long-term capital gain 0% bracket ends | $48,350 single / $96,700 MFJ |
| Long-term capital gain 20% bracket begins | $533,400 single / $600,050 MFJ |
| Capital loss deduction | $3,000 ($1,500 MFS), indefinite carryforward |
| Kiddie tax threshold | Unearned income over $2,700 |
| AMT exemption | $88,100 single / $137,000 MFJ; phaseout begins $626,350 / $1,252,700 |
| QBI taxable income threshold | $197,300 single / $394,600 MFJ; phase-in range $50,000 / $100,000 above |
| Standard mileage — business | 70¢ |
| Standard mileage — medical/moving | 21¢ |
| Standard mileage — charitable | 14¢ |
| §179 expensing limit | $2,500,000, phasing out above $4,000,000 of property placed in service |
| Bonus depreciation | 100% for qualifying property acquired after 1/19/2025 |
| Qualifying relative gross income limit | $5,200 ✓ (up from $5,050 in 2024) |
| Rental active participation allowance | $25,000, phasing out $100,000–$150,000 MAGI |
| Estimated tax safe harbor | 90% current year, or 100% of prior year (110% if prior AGI over $150,000) |
| Foreign earned income exclusion | $130,000 |
| FBAR threshold | $10,000 aggregate at any time |
| 1099-K reporting threshold | Over $20,000 **and** over 200 transactions |
| §121 home sale exclusion | $250,000 / $500,000 MFJ |
| Failure-to-file / failure-to-pay penalties | 5% per month / 0.5% per month |

**Social Security taxability base amounts**

| Status | 50% tier begins | 85% tier begins |
|---|---|---|
| Single / HOH / QSS | $25,000 | $34,000 |
| MFJ | $32,000 | $44,000 |
| MFS, lived together at any time | $0 | $0 |

---

# APPENDIX D — FORM 1040 LINE MAP (TY2025)

Page 1 numbering below reflects the TY2025 form, which inserted Schedule 1-A at line 13b. **Confirm against the final form and instructions on first use.**

| Line | Contents | Guide section |
|---|---|---|
| 1a | Wages from Form W-2 Box 1 | 5.1 |
| 1b–1h | Household employee wages, tips not reported, Medicaid waiver, dependent care benefits, adoption benefits, Form 8919 wages, other earned income | 5.1, 5.2 |
| 1i | Nontaxable combat pay election | 13.4 |
| 1z | Total of line 1 | — |
| 2a / 2b | Tax-exempt interest / taxable interest | 5.3 |
| 3a / 3b | Qualified dividends / ordinary dividends | 5.4 |
| 4a / 4b | IRA distributions gross / taxable | 5.5 |
| 5a / 5b | Pensions and annuities gross / taxable | 5.5 |
| 6a / 6b / 6c | Social Security gross / taxable / lump-sum election | 5.6 |
| 7 | Capital gain or loss (Schedule D) | 5.7 |
| 8 | Additional income (Schedule 1 line 10) | 5.8–5.13 |
| 9 | Total income | — |
| 10 | Adjustments (Schedule 1 line 26) | Part 6 |
| **11** | **Adjusted gross income** | — |
| 12 | Standard deduction or itemized deductions | Part 8 |
| 13a | Qualified business income deduction | Part 9 |
| 13b | Additional deductions (Schedule 1-A line 38) | Part 7 |
| 13c | Total of 13a and 13b | — |
| 14 | Lines 12 and 13c combined | — |
| **15** | **Taxable income** | — |
| 16 | Tax | Part 10 |
| 17 | Additional taxes from Schedule 2 Part I | Part 12 |
| 19 | Child tax credit and credit for other dependents | 11.2 |
| 20 | Other nonrefundable credits (Schedule 3 Part I) | Part 11 |
| 23 | Other taxes (Schedule 2 Part II) | Part 12 |
| **24** | **Total tax** | — |
| 25a–d | Federal income tax withheld — W-2, 1099, other, total | 13.1 |
| 26 | Estimated payments and prior-year overpayment applied | 13.2 |
| 27 | Earned income credit | 13.4 |
| 28 | Additional child tax credit | 11.2 |
| 29 | American opportunity credit, refundable portion | 11.4 |
| 31 | Other payments and refundable credits (Schedule 3 Part II) | 13.3 |
| **33** | **Total payments** | — |
| 34 | Amount overpaid | 14.1 |
| 35a | Refunded to the taxpayer | 14.2 |
| 36 | Applied to next year's estimated tax | 14.2 |
| 37 | Amount owed | 14.3 |
| 38 | Estimated tax penalty | 14.4 |

**Attached schedules**

| Schedule | Purpose | Reaches 1040 at |
|---|---|---|
| Schedule 1 Part I | Additional income | Line 8 |
| Schedule 1 Part II | Adjustments to income | Line 10 |
| **Schedule 1-A** | Tips, overtime, car loan interest, senior deduction | Line 13b |
| Schedule 2 Part I | AMT, excess advance PTC | Line 17 |
| Schedule 2 Part II | SE tax, other taxes | Line 23 |
| Schedule 3 Part I | Nonrefundable credits | Line 20 |
| Schedule 3 Part II | Other payments and refundable credits | Line 31 |
| Schedule A | Itemized deductions | Line 12 |
| Schedule B | Interest and dividends | Lines 2b, 3b |
| Schedule C | Business profit or loss | Schedule 1 Part I |
| Schedule D | Capital gains and losses | Line 7 |
| Schedule E | Rents, royalties, pass-throughs | Schedule 1 Part I |
| Schedule F | Farm | Schedule 1 Part I |
| Schedule SE | Self-employment tax | Schedule 2, and Schedule 1 for half |
| Schedule EIC | Qualifying children for EITC | Line 27 |
| Schedule 8812 | Child tax credit and ACTC | Lines 19, 28 |
| Schedule H | Household employment taxes | Schedule 2 |
| Schedule R | Elderly or disabled credit | Schedule 3 |

---

# APPENDIX E — PUBLICATION CROSSWALK

| Guide section | Primary publication | Secondary |
|---|---|---|
| Part 1, intake and consent | Pub 4491 *Screening and Interviewing* | Circular 230 §10.22, §10.34 |
| Part 2, taxpayer data | Pub 501 | Form 1040 instructions |
| Part 3, filing status | Pub 501; Pub 4012 Tab B | Pub 555 (community property) |
| Part 4, dependents | Pub 501; Pub 4012 Tab C | Pub 504 (divorced or separated) |
| 5.1–5.2, wages and tips | Pub 4012 Tab D; Pub 531 | Pub 15-A |
| 5.3–5.4, interest and dividends | Pub 550 | Pub 1212 (OID) |
| 5.5, retirement | Pub 590-B; Pub 575 | Pub 939 |
| 5.6, Social Security | Pub 915 | — |
| 5.7, capital gains and basis | Pub 550; Pub 551 | Pub 523 (home sale) |
| 5.8, self-employment | Pub 334 | Pub 463, 535, 587, 946 |
| 5.9, rental | Pub 527 | Pub 925, 946 |
| 5.10, K-1s | Pub 541 | Form 7203 instructions |
| 5.11, farm | Pub 225 | — |
| 5.13, other income | Pub 525 | Pub 4681 (canceled debt) |
| Part 6, adjustments | Pub 4012 Tab E; Pub 590-A | Pub 969 (HSA), Pub 970 |
| Part 7, Schedule 1-A | Schedule 1-A instructions | IRS newsroom guidance |
| Part 8, deductions | Pub 501; Pub 4012 Tab F | Pub 502, 526, 936, 529 |
| Part 9, QBI | Form 8995/8995-A instructions | — |
| Part 10, tax computation | Form 1040 instructions | Form 6251, 8615 instructions |
| Part 11, credits | Pub 4012 Tabs G, H | Pub 503, 970, 974 |
| Part 12, other taxes | Schedule 2 instructions | Pub 517 (clergy), 926 (household) |
| Part 13, payments and EITC | Pub 596 | Pub 505 |
| Part 14, refund and estimates | Pub 505 | Form 2210 instructions |
| Part 15, due diligence | Form 8867 instructions | Circular 230 |
| Part 16, e-file | Pub 1345 | Pub 4491 *Quality Review* |
| Part 17, after the return | Pub 556; Pub 1 | Form 1040-X instructions |

---

# APPENDIX F — PRE-USE VERIFICATION CHECKLIST

Complete before this guide is relied on for a live return, and once each filing season thereafter.

1. **Confirm every figure in Appendix C** against the IRS instructions or the annual revenue procedure. Correct in Appendix C only.
2. **Confirm the Form 1040 line map in Appendix D** against the final TY2025 form, particularly lines 12 through 15 where Schedule 1-A was inserted.
3. **Confirm the remaining Drake screen codes marked †** against the installed year using F1 or the Federal 1040 Screen List (KB 20051). Remove the dagger once confirmed. The unmarked codes were verified against the Drake knowledge base; the daggered remainder is the short list still outstanding — chiefly `RRB`, `99K`, `99C`, `HOME`, `AUTO`, `SEP`, `HSA`, `LTC`, `IDS`, `ADMN`, `PREP`, and the administrative forms.
4. **Confirm Schedule 1-A behavior in the installed software.** Screen **1A** on the General tab is confirmed, as is the carry to Form 1040 line 13b. Still verify in your installed year: that the four deductions compute, that the MAGI phaseouts apply, that line 14b captures overtime reported on Form 1099-NEC or 1099-MISC rather than only W-2 overtime on 14a, that all four vehicle entries accept a VIN and a post-12/31/2024 origination date, and that the senior deduction **stacks with** the age-65 additional standard deduction rather than replacing it.
5. **Confirm Pub 4012 tab letters** against the printed edition.
6. **Confirm the TY2025 energy and vehicle credit termination dates** (11.7) against current guidance, since these changed during the year.
7. **Confirm the qualifying relative gross income limit** and the EITC maximum credit amounts, which are the two figures in Appendix C carrying the most uncertainty.
8. **Confirm the tips occupation list** published by Treasury for the Schedule 1-A tips deduction.
9. **Set the Setup options in 0.1** on every workstation.
10. **Run one practice return end to end** against this guide and note anything the guide does not cover.

---

# APPENDIX G — QUIZ ANSWER KEY

### Quiz 0
1. W-2 wage and withholding verification (catches transposition in Boxes 1, 2, 16, 17 at the point of entry) and "always show tax computation worksheet" (shows which method produced the tax instead of a bare number).
2. An override replaces the calculated number outright. An adjustment modifies it — positive increases, negative decreases. Both are admissions you could not find the entry causing the wrong result; find the entry instead.
3. It assigns an item to Taxpayer, Spouse, or Joint. It is invisible until the return is split or a per-person limit is hit — the Social Security wage base, the IRA coverage test, the excess Social Security tax credit, HSA limits.
4. A detail worksheet exists behind the field. CTRL+W.
5. Nearly every phaseout on the return measures against AGI or a MAGI derived from it, so any change to income or adjustments changes results downstream, and credits must be re-checked.

### Quiz 1
1. §7216 governs the use and disclosure of taxpayer return information by a preparer; violation is criminal, with a companion civil penalty under §6713. A consent to **use** covers using the information for anything beyond preparing the return; a consent to **disclose** covers giving it to anyone outside the firm.
2. Any four of: marital status and date of change; new household members; self-employment or gig income; Marketplace coverage; foreign accounts or income; digital asset activity; retirement distributions or rollovers; a move, home sale, or rental; tuition or student loan payments; estimated payments made; prior disallowed credits.
3. Both reject. A missing required IP PIN rejects, and a prior-year IP PIN rejects because it changes annually.
4. **NOTE**, which can be set to block the return from being marked complete.
5. The child tax credit now requires a valid SSN for the taxpayer (at least one spouse on a joint return). The Schedule 1-A deductions also require a taxpayer SSN.

### Quiz 2
1. Any four of: the additional standard deduction at 65; the Schedule 1-A senior deduction; EITC age tests; IRA and retirement contribution and distribution rules; kiddie tax applicability; the credit for the elderly.
2. The "dependent of another" box. It caps the standard deduction at the greater of the floor amount or earned income plus a small increment, and blocks several credits including the education credits and the saver's credit.
3. Net self-employment earnings of $400 or more. Also: advance premium tax credit received, certain other taxes owed, or the desire to claim refundable credits or a withholding refund.
4. Any five of: capital loss carryover; charitable carryover; passive activity loss carryover; NOL; §179 carryover; depreciation basis and accumulated depreciation; Form 8606 IRA basis; AMT credit; foreign tax credit carryover; state overpayment applied; installment sale balances.
5. On page 1 of Form 1040, entered on Drake screen **1**. It is required on every return.

### Quiz 3
1. A qualifying person lived in the home more than half the year, **and** the taxpayer paid more than half the cost of keeping up the home. The cost test is the one skipped.
2. Any five of: EITC; education credits; student loan interest; dependent care credit; the collapsed IRA and Roth phaseout ranges; the premium tax credit; the zero Social Security base amount when the spouses lived together; the halved SALT cap and capital loss limit; the requirement that both spouses itemize if either does.
3. TY2025 is MFJ — the year of death still permits a joint return. TY2026 would be qualifying surviving spouse if there is a dependent child, the taxpayer has not remarried, and they pay more than half the cost of the home.
4. The spouse did not live in the home during the last six months of the year; the taxpayer paid more than half the cost of keeping up the home; a qualifying child lived with the taxpayer more than half the year.
5. The **Return > Split** function compares MFJ against two MFS returns. **Form 8958** is required for MFS in a community property state.

### Quiz 4
1. Relationship, age, residency, support, and joint return.
2. Qualifying child: the **child** must not have provided more than half of their **own** support. Qualifying relative: the **taxpayer** must have provided more than half of the **person's** support. The direction reverses.
3. The parent with the higher AGI, under the tiebreaker rules. The taxpayers do not choose, and filing first does not decide it.
4. Transfers: the dependency claim, the child tax credit, and the credit for other dependents. Does **not** transfer: head of household, EITC, the dependent care credit, and the exclusion for dependent care benefits.
5. **Months lived in the home** on screen 2. Residency is what decides contested claims, and Drake will compute credits from a defaulted value without complaint.
6. When a credit (EITC, CTC/ACTC/ODC, or AOTC) was previously disallowed for reasons other than a math error. Omitting it produces a reject or a denial of the credit.

### Quiz 5.1
1. Box 1 goes to the income block (line 1a); Box 2 goes to the payments block (line 25a). They are conflated constantly, and treating withholding as income or vice versa breaks both the tax and the refund.
2. Employer and employee HSA contributions made through a cafeteria plan. It triggers Form 8889, and it belongs on **line 9** (employer contributions), not line 2.
3. It indicates coverage by a workplace retirement plan, which is one of the two facts that decides whether a traditional IRA contribution is deductible (6.6).
4. Excess Social Security tax was withheld. It is a refundable credit in the payments block — but only when the excess arises for **one person** across multiple employers.
5. Allocated tips are not included in Box 1 and must be reported. Form **4137** computes the employee's share of Social Security and Medicare on them.

### Quiz 5.2
1. Reported tips are already in Box 1. Allocated tips (Box 8) are not in Box 1 and must be added. Unreported tips were never given to the employer and require Form 4137.
2. Form **4137**; the tax lands on Schedule 2 as an other tax.
3. It reduces **taxable income** only. It is taken after AGI on Schedule 1-A, so it does not loosen AGI-based phaseouts, and the tips remain fully subject to Social Security and Medicare tax.

### Quiz 5.3
1. Taxable interest or ordinary dividends over $1,500; a foreign account or foreign trust interest; or the other conditions in the Schedule B instructions (nominee distributions, seller-financed mortgage interest, bond premium).
2. Because it affects other calculations even though it is not taxed — the provisional income computation for Social Security, and MAGI for the premium tax credit, IRA deductibility, and other phaseouts.
3. Aggregate foreign account value over $10,000 at any point in the year. FinCEN Form 114 is filed with FinCEN, separately from the return. Form 8938 has higher, status-dependent thresholds and is filed **with** the return. Either, both, or neither can apply.
4. Screen **B**, Schedule B **Part III**.
5. Form **8815**. It is disqualified by MFS status, by MAGI above the phaseout, and by bonds not issued in the taxpayer's name (or spouse's) after 1989 with the taxpayer at least 24 at issuance.

### Quiz 5.4
1. Line 3a (qualified dividends) is a **subset** of line 3b (ordinary dividends), taxed at capital gain rates rather than ordinary rates.
2. More than 60 days held within the 121-day window surrounding the ex-dividend date. A client who sold soon after a dividend may fail the holding period even though the payer reported the dividend as qualified.
3. A return of capital. It is not income; it reduces basis. Once basis reaches zero, further distributions are capital gain.
4. Box 5, §199A dividends, feeding Form 8995 and the QBI deduction.

### Quiz 5.5
1. Line 4a is the gross distribution; line 4b is the taxable amount. On a direct rollover, line 4b is zero and **ROLLOVER** prints beside the line.
2. G is a direct rollover (not taxable). 1 is an early distribution with no known exception (10% additional tax unless an exception is claimed on Form 5329). S is an early SIMPLE distribution within the first two years, carrying **25%**.
3. Compute the taxable portion yourself using the pro rata rule across all traditional IRAs. **Form 8606** holds the basis and performs the computation.
4. A qualified charitable distribution: age 70½ or older, paid directly from the IRA to a qualified charity. It is better than a deduction because it is excluded from income entirely, reducing AGI and therefore every AGI-driven phaseout — and it helps even a client taking the standard deduction.
5. Any four of: first-time home purchase (IRA only), qualified higher education (IRA only), medical expenses above the AGI floor, disability, death, separation from service at 55 or later (plan only), substantially equal periodic payments, IRS levy, qualified birth or adoption, certain disasters. Reported on **Form 5329**.

### Quiz 5.6
1. AGI excluding Social Security, plus tax-exempt interest, plus certain exclusions, plus one-half of the Social Security benefit. Tax-exempt interest is the surprise — it increases the tax on benefits despite not being taxed itself.
2. 50% and 85%.
3. The base amount is **zero**, so up to 85% of benefits are taxable immediately.
4. The **gross** benefit. The Medicare premiums go to Schedule A as a medical expense.
5. An election to compute the taxable portion of a prior-year benefit paid in the current year using the prior year's income. Reported on line **6c**.

### Quiz 5.7
1. Proceeds, basis, and holding period. **Basis** is most often wrong.
2. Inherited: fair market value at date of death, with an automatic long-term holding period. Gift with a gain: the donor's carryover basis. Gift with a loss: FMV at the date of the gift — the dual-basis rule.
3. $3,000 per year ($1,500 MFS); the excess carries forward indefinitely retaining its short- or long-term character. It is lost when a returning client is set up as a new return instead of being carried forward.
4. The compensation element already taxed in W-2 Box 1 **is** basis, and the broker omitted it. Correct the basis on Form 8949 with an adjustment code, using the vesting-date value from the employer's supplemental statement.
5. Owned and used as a principal residence for two of the last five years, and no §121 exclusion used in the prior two years. $250,000 of gain, or $500,000 MFJ.
6. A loss on a security sold and repurchased within 30 days before or after the sale. The loss is disallowed and added to the basis of the replacement shares, deferring it. If the replacement is bought inside an IRA, the loss is **permanently** lost — there is no basis to add it to.

### Quiz 5.8
1. Whenever there is a trade or business carried on with continuity and a profit motive, regardless of amount. No — the absence of a 1099-NEC changes nothing; cash income is income.
2. Standard mileage and actual expenses. A vehicle placed in service using actual expenses with MACRS depreciation can never switch to standard mileage.
3. **Exclusive** and **regular** use as the principal place of business. The deduction cannot create or increase a loss; the disallowed portion carries forward.
4. §179 is elected, applies to specified property, and is limited by business income (the excess carries forward). Bonus depreciation is automatic unless elected out, is not limited by business income, and can create a loss. TY2025 restores 100% bonus for qualifying property acquired after 1/19/2025.
5. It is hobby income, reported as other income on Schedule 1. The expenses are **not deductible** at all, because the miscellaneous itemized deduction that used to absorb them is suspended.
6. The code that links a 4562 asset, an AUTO entry, or a 1099 to a specific activity. Left blank on a multi-business return, everything attaches to the first activity.

### Quiz 5.9
1. A repair keeps the property in operating condition and is deducted currently; an improvement betters, restores, or adapts it and must be capitalized and depreciated. Getting it wrong either overstates the current deduction or defers a deduction the client was entitled to now.
2. Gain on sale is computed as though depreciation had been taken whether or not it was. Skipping it forfeits the deduction while keeping the recapture — the worst of both.
3. Up to $25,000 of rental loss deductible against other income for a taxpayer who **actively participates**. It phases out between $100,000 and $150,000 of modified AGI.
4. It is not reported at all. Fewer than 15 rental days means no rental income and no rental expenses.
5. **Form 8582**. A fully taxable disposition of the entire interest releases the suspended losses.

### Quiz 5.10
1. Basis, then at-risk, then passive. A loss must clear all three.
2. **Form 7203**, required when the shareholder claims a loss, receives a distribution, disposes of stock, or receives a loan repayment.
3. A partnership guaranteed payment **is** subject to SE tax. S corporation ordinary income is **not** — but the shareholder-employee must take reasonable compensation on a W-2, and an S corporation K-1 with substantial income and no owner wages is an examination flag.
4. The capital account is a book or §704(b) measure reported by the entity; tax basis includes the partner's share of liabilities and reflects the partner's own transactions. They routinely differ.
5. Any three of: §179 deduction; charitable contributions; §199A information; foreign taxes; interest, dividend, and capital gain items; investment interest expense; tax-exempt income.

### Quiz 5.11
1. Schedule F is for a farmer who materially participates and carries SE tax. Form 4835 is farm rental income where the landlord does **not** materially participate, and is not subject to SE tax.
2. Farm income averaging — it spreads farm income back over the three prior years' brackets.
3. A qualifying farmer (two-thirds of gross income from farming) may make a single estimated installment due January 15, or skip estimates entirely by filing the return and paying the full tax by March 1.

### Quiz 5.12
1. Fully taxable, and withholding is optional — most recipients decline it, which is why unemployment years produce balances due.
2. When the client took the **standard deduction** in the year the tax was paid, so the state tax produced no benefit. The tax benefit rule then makes the refund entirely nontaxable.
3. The prior-year itemized deduction total, the prior-year standard deduction for that status, the state and local tax actually deducted, and whether the SALT cap limited it.

### Quiz 5.13
1. The full $8,000 of winnings is taxable, and the $8,000 of losses is deductible only as an itemized deduction. A client taking the standard deduction pays tax on the full $8,000 despite having broken even.
2. Bankruptcy, insolvency, qualified principal residence indebtedness, qualified farm indebtedness, and qualified real property business indebtedness. Claimed on **Form 982**.
3. The date of the divorce or separation instrument. Alimony is taxable to the recipient and deductible by the payer only under instruments executed on or before 12/31/2018 and not modified to adopt the current rules.
4. Yes — a token-for-token trade is a taxable disposition; like-kind exchange treatment is unavailable. Moving coins between the taxpayer's own wallets is not a disposition.
5. Page 1 of Form 1040, entered on Drake screen **1**. It must be answered on every return.

### Quiz 5.14
1. The $40,000 inheritance is not reported. The $1,200 of interest earned after death **is** reported as interest income.
2. Not reported: child support; workers' compensation. Reported: alimony under a 2015 decree; punitive damages.
3. Because it enters the provisional income computation for Social Security and several MAGI tests, so it must be visible on line 2a even though it is not taxed.

### Quiz 6
1. An adjustment reduces AGI itself, so it lowers tax directly **and** loosens every phaseout that AGI governs. It also helps every taxpayer, while an itemized deduction only helps those whose itemized total exceeds the standard deduction.
2. Whether the taxpayer or spouse is covered by a workplace retirement plan, and MAGI against the applicable phaseout range. The first comes from **W-2 Box 13**.
3. Line 2 is the taxpayer's own after-tax contributions, which produce the deduction. Line 9 is employer contributions including cafeteria-plan amounts in Box 12 code W, already excluded from Box 1. Entering a code W amount on line 2 double-counts it and generates a phantom excess contribution and a 6% excise tax.
4. Limited to the net profit of the business the plan is established under; disallowed for any month the taxpayer was eligible for an employer-subsidized plan through their own or a spouse's employer; and the same premiums cannot also be deducted on Schedule A.
5. 7% of the conversion is nontaxable and 93% is taxable — $7,000 of basis against $100,000 of total traditional IRA value. The **pro rata rule** produces this; the conversion cannot be matched only against the new contribution.
6. The basis is lost, and the client is taxed a second time on the same dollars when the money is eventually distributed. The fix is a chain of amended returns, if the records still exist.
7. Only members of the Armed Forces on active duty moving under a permanent change of station order.
8. The **child** may deduct it, provided the child is not claimed as a dependent — the parent's payment is treated as a gift to the child, who is treated as making the payment. The parent deducts nothing because they are not legally obligated. **MFS** disqualifies the deduction entirely.
9. The recipient's **SSN** and the **date of the original divorce or separation instrument**. The instrument qualifies only if it was executed on or before 12/31/2018 and has not been modified to adopt the post-TCJA rules.

### Quiz 7
1. Form 1040 line **13b**. It is subtracted **after** AGI.
2. Yes. These are below-the-line deductions but are not itemized deductions, so a standard-deduction taxpayer gets them in addition to the standard deduction.
3. Only the FLSA **premium** portion qualifies — the extra half in time-and-a-half — so roughly $6,000 of an $18,000 overtime figure, subject to the $12,500/$25,000 cap and the MAGI phaseout.
4. Any four of: a **new** vehicle; personal use; the loan secured by a first lien on the vehicle; final assembly in the United States; loan originated after 12/31/2024; **VIN reported** on Schedule 1-A; MAGI below the phaseout.
5. The age-65 additional standard deduction ($2,000 for an unmarried taxpayer) **and** the $6,000 Schedule 1-A senior deduction. They are cumulative, not alternatives.
6. Because it is a deduction from taxable income, not an exclusion from wages. The tips remain wages for FICA purposes and remain in AGI.
7. Married filing separately.

### Quiz 8
1. Filing status, date of birth (age 65), and the blindness checkboxes — plus the dependent-of-another indicator, which is the one missed on a student's return.
2. In addition to it. Both apply.
3. 7.5% of AGI. Commonly missed: Medicare premiums withheld from Social Security benefits, and long-term care insurance premiums within the age-based limits. (Also medical mileage and after-tax retiree health premiums.)
4. The cap rose to $40,000 ($20,000 MFS) with a phase-down above $500,000 MAGI, floored at $10,000. Re-test every client with meaningful state income tax and property tax, including those who have taken the standard deduction since 2018.
5. Only the interest on the $40,000 used to substantially improve the home is deductible — two-thirds of the interest. The 1098 reports the interest paid and the outstanding balance; it does not report what the proceeds were used for. Only the client can answer that.
6. $250. No — the acknowledgment must be contemporaneous, obtained by the earlier of the filing date or the due date, and it cannot be cured afterward.
7. Noncash gifts over $500 require Form 8283 Section A; over $5,000 requires Section B **and** a qualified appraisal.
8. Zero. The value of donated services and time is never deductible. Unreimbursed out-of-pocket costs incurred while volunteering are.

### Quiz 9
1. No, it does not reduce self-employment tax. No, it does not reduce AGI — it comes after AGI. It appears on Form 1040 line 13a.
2. The W-2 wage and qualified property limitation (the greater of 50% of W-2 wages, or 25% of wages plus 2.5% of unadjusted basis), and the specified service trade or business restriction, which applies only to SSTBs.
3. Any four of: capital gains and losses; dividends; interest not allocable to the business; reasonable compensation paid to an S corporation shareholder; guaranteed payments to a partner; foreign-source income.
4. The deductible half of self-employment tax, the self-employed health insurance deduction, and self-employed retirement plan contributions attributable to the business.
5. Box 5, §199A dividends.
6. 250 hours of rental services per year, separate books and records for the enterprise, and contemporaneous records including time logs.

### Quiz 10
1. The marginal rate is the rate on the next dollar of income; the effective rate is total tax divided by taxable income. The effective rate is always lower because income in the lower brackets is taxed at those lower rates.
2. Any three of: the Social Security provisional income phase-in; the EITC phase-out; the premium tax credit phase-out; education credit phaseouts; the QBI phase-in range; the Schedule 1-A phaseouts; the IRA deduction phaseout.
3. The **Qualified Dividends and Capital Gain Tax Worksheet**. The tax table applies ordinary rates to all taxable income and would overstate the tax on the preferential income.
4. A child with unearned income above the threshold who is under 18, or 18 and did not provide more than half their support from earned income, or a full-time student aged 19–23 in the same situation. The excess is taxed at the **parent's** marginal rate.
5. Incentive stock option exercises, large state and local tax deductions in high-tax states, and substantial private activity bond interest.
6. No regular tax event. The bargain element is an AMT preference, potentially producing a large AMT liability with no cash from a sale to pay it. The AMT paid becomes a Form 8801 minimum tax credit recoverable in later years.

### Quiz 11
1. A nonrefundable credit reduces tax to zero and stops; it sits in the credits block. A refundable credit can produce a refund exceeding what was paid in; it sits in the payments block.
2. $2,200 per qualifying child under 17 with a work-eligible SSN; up to $1,700 refundable as the ACTC. New for TY2025, the **taxpayer** must also have a valid SSN (at least one spouse on a joint return).
3. Yes. A spouse who is a full-time student or is disabled is treated as having deemed monthly earned income, which satisfies the both-spouses-must-have-earned-income requirement.
4. AOTC: $2,500 maximum, **per student**, 40% refundable up to $1,000, available for four years. LLC: $2,000 maximum, **per return**, not refundable, available for unlimited years.
5. Box 1 reports amounts paid to the institution, which can straddle academic years, exclude course materials bought elsewhere, and disagree with what the taxpayer actually paid. Use the bursar's account statement plus receipts for books and required materials.
6. Two years before the tax year through the filing date of the return. Distributions from retirement accounts during that window reduce the eligible contribution and can eliminate the credit entirely.
7. When all foreign tax is from passive income reported on 1099-DIV or 1099-INT and the total does not exceed $300 ($600 MFJ). Then it can be claimed directly on Schedule 3.
8. No. The new clean vehicle credit terminated for vehicles **acquired after 9/30/2025**. The acquisition date controls — not delivery, and not the contract date.

### Quiz 12
1. 92.35%. The remaining 7.65% approximates the employer-share deduction an employee would effectively receive, keeping a self-employed person roughly parallel to an employee.
2. The Social Security portion applies only to the wage base remaining after the $170,000 of W-2 wages — roughly $6,100 of the $176,100 base. The Medicare portion (2.9%) applies to all of the net SE earnings, because it has no ceiling.
3. No, neither employer withholds — the 0.9% withholding trigger is $200,000 of wages **per employer**, and each earns $160,000. Yes, they owe it: their combined $320,000 exceeds the $250,000 MFJ threshold, producing tax on $70,000. This is the classic unexpected balance due.
4. Included: interest, dividends, capital gains, rents, royalties, annuities, and passive business income. Excluded: wages, self-employment income, active business income, tax-exempt interest, and distributions from qualified retirement plans.
5. It is rejected or held, because Form 8962 is required to reconcile the advance premium tax credit. This is a leading cause of delayed refunds.
6. The qualified higher education expense exception applies to IRA distributions, so the 10% additional tax does not apply — but the distribution is still ordinary income. Claimed on **Form 5329** with the exception code.
7. When the taxpayer paid a household employee cash wages above the annual threshold, or paid $1,000 or more in any calendar quarter (triggering FUTA).

### Quiz 13
1. Because it behaves like money already paid — it can produce a refund beyond the tax and beyond what was withheld. That is precisely what the payments block represents.
2. Treated as paid evenly throughout the year regardless of when it was actually withheld. That makes a late-year withholding increase able to cure an earlier underpayment, which a fourth-quarter estimated payment cannot do.
3. Any four of: unemployment compensation; pension and IRA distributions; Social Security; interest, dividends, and capital gains; alimony; workers' compensation; income earned while an inmate.
4. $11,950 for TY2025. One dollar over eliminates the **entire** credit — a cliff, not a graduated reduction.
5. The **support test** does not apply to an EITC qualifying child. A child can therefore be an EITC qualifying child without being the taxpayer's dependent.
6. No. Neither person exceeded the wage base individually, and the excess Social Security tax credit is computed **per person**. Combining spouses' wages to manufacture an excess is a common and incorrect adjustment.
7. The IRS may not issue a refund on a return claiming EITC or ACTC before mid-February. Set the client's expectation at filing.

### Quiz 14
1. Tax due after withholding and credits under $1,000; or payments of at least 90% of the current year's tax; or payments of at least 100% of the prior year's tax — **110%** if prior-year AGI exceeded $150,000 ($75,000 MFS).
2. It extends the time to **file**. It does not extend the time to **pay**; interest and failure-to-pay penalties run from the original due date.
3. Failure to file is 5% per month; failure to pay is 0.5% per month — ten times the cost. Always file on time, even when the client cannot pay.
4. The **annualized income installment method** on Form 2210. It matches required installments to when the income was actually earned, so a fourth-quarter gain does not create a penalty for the first three quarters.
5. Withholding is deemed paid ratably across the year, so it can cure a first-quarter shortfall. An estimated payment is credited on the date paid and does not fix earlier underpayments.
6. Both accounts must be in the taxpayer's name; a preparer's account is prohibited. Form **8888** splits a refund across up to three accounts. The IRS also limits deposits to three per account before converting to a paper check.

### Quiz 15
1. Earned income credit; child tax credit / additional child tax credit / credit for other dependents; American opportunity credit; head of household filing status.
2. The §6695(g) penalty applies **per credit, per return**. Such a return carries four separate exposures.
3. Complete and submit Form 8867; compute the credit using the worksheets or equivalent and keep them; satisfy the knowledge requirement by making reasonable inquiries into incorrect, inconsistent, or incomplete information and contemporaneously documenting them; keep the records for three years.
4. Receipts with no expenses is implausible for almost any real business, and the income sits where the EITC is maximized. You must inquire into the nature of the business, its actual expenses, and the records supporting the receipts, and you must record the questions asked and the answers given, in the file, at the time.
5. No. The obligation runs to the process as well as the result; the penalty applies for failing to meet the requirements even when the credit is ultimately correct.

### Quiz 16
1. EF Messages (blocking), Return Notes (informational), and Fed/State Warnings. EF messages are blocking; **return notes** are where the real error most often is, because nothing forces you to read them.
2. Comparing data entry to data entry only confirms that you typed what you typed. Only the source documents can show what should have been entered.
3. After the taxpayer has reviewed the return and **before** transmission. It is not filed with the IRS; it is retained by the ERO for three years.
4. A transmitted return has been sent but not necessarily accepted. It is filed only when the IRS acknowledgment shows acceptance. A rejected return that is never corrected was never filed.
5. Another return claimed the same dependent first — a former spouse, another relative, or identity theft. Confirm the client's entitlement, then paper file with documentation of relationship, residency, and support; the IRS resolves the conflict afterward.
6. Setup > Options, **"always show reason for no EIC."** In review you must know why each credit did **not** generate, not only that it did not.

### Quiz 17
1. Three years from the date the return was filed, or two years from the date the tax was paid, whichever is **later**.
2. A return filed after the original but before the due date including extensions. It replaces the original rather than amending it, and is available more often than preparers use it — including for elections requiring a timely filed return.
3. MFJ to MFS only before the original due date. MFS to MFJ any time within the statute.
4. The client omitted a 1099-B, and the IRS proposed tax on the full proceeds assuming zero basis. Respond by the deadline with the basis documentation and a corrected Schedule D / Form 8949; the real liability is usually a small fraction of the proposal.
5. Any five of: home improvement records; investment purchase records; Form 8606 IRA basis; depreciation schedules; carryover schedules; partnership and S corporation basis records; prior returns supporting a carryover or an election.
6. Any eight of: capital loss carryover; charitable contribution carryover; passive activity loss carryover; NOL; §179 carryover; at-risk carryover; depreciation basis and accumulated depreciation; Form 8606 IRA basis; AMT credit; foreign tax credit carryover; residential clean energy credit carryover; adoption credit carryover; investment interest expense carryover; state overpayment applied; installment sale balances.

---

# APPENDIX H — DRAKE KB ARTICLE INDEX BY SECTION

Every article below was confirmed to exist. Article numbers are stable across years; the **content** is updated per year, so an article still needs to be read against the installed version. F1 inside the screen remains the authority for the installed year's field layout.

URL pattern: `https://kb.drakesoftware.com/kb/Drake-Tax/<number>.htm`

**Orientation and navigation**

| Article | Title |
|---|---|
| 20051 | Federal 1040: Screen List |
| 13109 | Data Entry Basics |
| 10221 | Creating a New Return |
| 14287 | Data Entry Toolbar |
| 18202 | Setup Options Overview |
| 20072 | Viewing and Printing a Return |
| 12615 | Right-Click Menus in Drake Software |
| 10855 | Comparison Sheet FAQs (prior-year comparison) |
| 12496 | Practice Management Tools |
| — | Drake 101 – Data Entry (PDF): `kb.drakesoftware.com/kb/Resources/PDFs-Finished/Drake_101_Data_Entry.pdf` |

**TY2025 / OBBBA — read these first**

| Article | Title | Guide section |
|---|---|---|
| 18910 | 2025 Changes for Form 1040 and Related Schedules and Forms | Front matter |
| 18889 | New Tax Bill | Front matter |
| 18890 | Schedule 1-A: Additional Deductions | Part 7 |
| 18874 | Qualified Overtime Compensation Deduction ("No Tax on Overtime") | 7.3 |
| 18926 | Qualified Passenger Vehicle Loan Interest Deduction ("No Tax on Car Loan Interest") | 7.4 |
| 18837 | Drake Tax Planner Updates for New Tax Bill | Part 14 |
| 18950 | SC – New Tax Bill Non-Conformity (2025) — a template for checking state conformity | Part 8 |

**Part 1 — Intake, identity, consent**

| Article | Title |
|---|---|
| 10866 | Consent Forms for Use and Disclosure of Tax Return Information (§7216) |
| 13355 | Drake E-Sign (in-person or online) |
| 11688 | Setting Up Alternative Electronic Signatures |

**Parts 3–4 — Filing status and dependents**

| Article | Title |
|---|---|
| 10558 | 8332: Release / Revoke of Claim of Dependent |
| 14867 | Not a Dependent: HOH Qualifier |
| 14573 | Child Tax Credit – Fewer Than 7 Months in Home |
| 18340 | 8812: CTC, ACTC, and ODC |

**5.1 — Wages**

| Article | Title |
|---|---|
| 10932 | 1040: Wage or Distribution and Withholding Verification Fields |
| 10378 | W-2: Additional Entries for Boxes 12, 14, and States |
| 10796 | W2 Import Feature |
| 10623 | Forms W-2 and 1099 in View and Sets |

**5.3–5.4 — Interest and dividends**

| Article | Title |
|---|---|
| 11742 | Guide to 1098 and 1099 Informational Returns — the master source-document index |

**5.5 — Retirement distributions**

| Article | Title |
|---|---|
| 10437 | 1099-R: Taxable Amount FAQs |
| 10177 | 1040: 1099-R ROLLOVER Checkbox or Literal |
| 11185 | 1099-R – Roth Distributions and Rollovers |
| 17107 | 1099-R – Additional Information Check Boxes |
| 16070 | 1099-R – Box 7 Code J |
| 13788 | 5329 – Common Scenarios and Questions |
| 15519 | Forms 8915-A through 8915-E (disaster distributions) |

**5.7 — Capital gains and basis**

| Article | Title |
|---|---|
| 10542 | 1099-B – Broker and Barter Transactions |
| 12530 | Schedule D: Lines 1a and 8a (summary reporting without Form 8949) |
| 13157 | 8949: Code on Part I or II (adjustment codes) |
| 10139 | Schedule D / Form 8949 Import |
| 11978 | 8949 – Import Transactions, PDI Indicator or PDF Attachment |
| 13244 | 1040: Importing Multiple Schedule D Transaction Spreadsheets |
| 11409 | 8949: EF Message 5310 |
| 14125 | Sale of Asset Used for Personal and Business Use |

**5.8 — Self-employment and depreciation**

| Article | Title |
|---|---|
| 11794 | 4562 Screen and Screens 6-9 (use the detail screen, not the overrides) |
| 11881 | 4562: Common Issues, Limits, Section 179 Data Entry, EF Message 2408 |
| 10108 | Depreciation Calculation |
| 14188 | 4562: Description Keywords — **do not begin a description with LAND** or depreciation will not calculate |
| 11419 | 4562: Printing Issues |
| 11565 | 1040: Recapturing Depreciation |
| 10893 | 1040: Auto expenses |
| 10520 | 1099-K: Data Entry |
| 10519 | Self-Employment Health Insurance Deduction |

**5.9 — Rental and passive losses**

| Article | Title |
|---|---|
| 10284 | 1040: Form 8582 |
| 10311 | 1040: Prior Unallowed Passive Operating Losses |
| 10128 | 1040: Losses Not on Schedule E, page 2 |
| 18104 | Schedule E: Activity Type, Section 179, Note 120 |
| 14249 | Schedule E: Disposition of Rental Property |
| 10113 | Self-Rental and Land, Note 357 |
| 10210 | 4835: Farm Rental Income and Expenses |
| 11138 | 4797: Passive Activity Adjustment |

**5.10 — K-1s**

| Article | Title |
|---|---|
| 11124 | K1P: Income from PTP Considered Nonpassive |
| 16617 | 1065/1120-S – Wks QBI Calculation and Override |

**Part 6 — Adjustments**

| Article | Title |
|---|---|
| 11734 | 8889 – Frequently Asked Questions (HSA) |
| 15856 | 1040 – Death of HSA Account Beneficiary |
| 10286 | 8606: Lines 4 or 8 are Blank |
| 10365 | IRA: Recharacterization |
| 14711 | 1040: IRA Deduction Not Showing on Return |
| 10439 | 1098-E: Student Loan Interest Deduction |
| 10519 | Self-Employment Health Insurance Deduction |

**Part 8 — Schedule A**

| Article | Title |
|---|---|
| 16988 | Schedule A – Force Itemized or Standard Deduction |
| 15833 | Schedule A – State and Local Income Tax Deduction Limitation (Wks SALT) |
| 10641 | 1098: Mortgage Interest Deduction Limitation |
| 13229 | 1098: Splitting Mortgage Interest |
| 11513 | 1098 – Mortgage Insurance Premiums |
| 10584 | 1098-MA |
| 11171 | 1098-C: Data Entry (vehicle donation) |

**Part 9 — QBI**

| Article | Title |
|---|---|
| 15919 | QBI Deduction: Frequently Asked Questions |
| 16072 | QBI Deduction – Specified Service Trade or Business (SSTB) |
| 16071 | QBI Deduction: Business Aggregation |
| 16013 | QBI: Unadjusted Basis Immediately After Acquisition (UBIA) |
| 16616 | QBI – Form 8995-A – Schedule C Loss Netting and Carryforward |
| 16054 | QBI Deduction – W2 Wage Allocation 1120-S |
| 16431 | QBI Deduction – 1120-S/1065 Message Amount Unallocated |

**Part 11 — Credits**

| Article | Title |
|---|---|
| 18340 | 8812: CTC, ACTC, and ODC |
| 12153 | 8863: Education Benefits |
| 10991 | 1098-T: Data Entry |
| 10886 | EIC: Frequently Asked Questions |

**Part 12 — Other taxes and ACA**

| Article | Title |
|---|---|
| 13091 | ACA Reporting Forms 1095-A, 1095-B, 1094-C, 1095-C |
| 14067 | 8962: Shared Policy Allocation (ACA) |
| 17542 | Reject "F8962-070" – Forms 1095-A and 8962 Missing |

**Parts 13–14 — Payments, refund, balance due**

| Article | Title |
|---|---|
| 11656 | Form 8888: Direct Deposit |
| 10136 | Federal and State Payments – Electronic Funds Withdrawal Setup |
| 11567 | Wrong Direct Deposit or Direct Debit Bank Information on an e-Filed Return |
| 13370 | State Returns: Estimated Tax Vouchers Direct Debit |

**Part 15 — Due diligence**

| Article | Title |
|---|---|
| 14291 | 1040: Due Diligence FAQs |
| 14268 | Facts About Refundable Credits Due Diligence |

**Part 16 — Review, e-file, transmission**

| Article | Title |
|---|---|
| 10117 | Clearing EF Messages |
| 10398 | EF Return Selector – Messages and Troubleshooting |
| 19003 | Allow EF Selection from the Calculation Results Window (admin only) |
| 18896 | EF Messages 5330, 5350, 0672, 5084, 5090, 5091, 5092 |
| 10853 | 1040: EF Message 5331 |
| 20076 | EF Message 6219 |
| 14183 | 1040: EF Message 5429 |
| 20072 | Viewing and Printing a Return |

**Part 17 — After the return**

| Article | Title |
|---|---|
| 16841 | 1040: Generating an Amended Return |
| 10979 | 1040-X: FAQs and Troubleshooting |
| 17897 | Superseded Returns |
| 16938 | States Generally – Generating and e-Filing Amended Individual Returns |

**Other entity screen lists**, for when a K-1 traces back to its source: 1065 — 20054 · 1120-S — 20056 · 1120 — 20055 · 1041 — 20053.

---

## SCOPE NOTE

This guide covers **individual income tax returns (Form 1040)** only. Entity returns — Form 1065, Form 1120-S, Form 1120, Form 1041, and Form 709 — are out of scope here, and appear only where they feed the individual return through a Schedule K-1 (5.10).

The individual-return topics deliberately treated at overview depth rather than in full, because they are uncommon and each deserves its own research pass when they appear: nonresident and dual-status returns (Form 1040-NR), expatriation, foreign trusts and PFICs (Forms 3520, 8621), net operating loss computation and carryback elections, casualty loss computation for federally declared disasters, and clergy returns beyond the SE tax treatment noted in 12.2.
