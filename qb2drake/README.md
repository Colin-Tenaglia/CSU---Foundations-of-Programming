# qb2drake — QuickBooks → Drake Accounting converter

Reads a QuickBooks export and writes the two CSV files Drake Accounting
imports: a **chart of accounts** and a **transaction (journal entry) file**.

It handles the awkward parts of the job:

* QuickBooks report CSVs are laid out for a human — title rows above the real
  header, a leading blank column, subtotals mixed into the detail, and (in a
  General Ledger) the account printed once as a section heading instead of on
  every row.
* A General Ledger prints each side of an entry under a different account, so
  the entries have to be reassembled before Drake will accept them.
* QuickBooks does not require account numbers; Drake does. Unnumbered accounts
  are assigned numbers deterministically from type-based ranges.
* Sub-accounts (`Utilities:Electric`) become Drake levels, and any missing
  parent account is created.
* Everything is checked for balance *before* it reaches Drake, which reports
  import failures without saying which row caused them.

## Install

No dependencies for CSV/IIF input:

```bash
python -m qb2drake --help          # run straight from the repo
pip install -e .                   # or install the `qb2drake` command
pip install -e ".[excel]"          # add openpyxl for .xlsx input
```

## Quick start

```bash
# Best results: give it the account listing *and* the transaction report
qb2drake convert account_listing.csv general_ledger.csv -o drake_import/

# A single IIF export carries both
qb2drake convert quickbooks_export.iif -o drake_import/

# Parse and check without writing anything
qb2drake inspect journal.csv
```

Output lands in `drake_import/`:

```
drake_chart_of_accounts.csv
drake_transactions.csv
```

## ⚠️ Check the column layout against your copy of Drake

Drake Accounting's import templates vary between program years, and the import
wizard lets a firm re-order columns. **Compare the generated header row against
the template your Drake Accounting expects before importing.** The layout is
data, not code:

```bash
qb2drake dump-profile my_drake.json     # writes the default layout
$EDITOR my_drake.json                   # re-order / rename / drop columns
qb2drake convert export.iif --profile my_drake.json -o drake_import/
```

Each column is `{"header": "...", "field": "..."}`, or
`{"header": "...", "constant": "..."}` for a fixed value such as a client code.

| Chart fields | Transaction fields |
|---|---|
| `level`, `number`, `description`, `type`, `normal_balance`, `division`, `parent_number`, `source_name`, `opening_balance` | `entry_no`, `date`, `journal`, `reference`, `account_number`, `account_name`, `description`, `memo`, `name`, `debit`, `credit`, `amount`, `division` |

`date_format` and `zero_as_blank` (blank vs. `0.00` in the unused amount column)
are also set in the profile.

## Supported inputs

Format is detected from the file contents, so the extension does not matter.

| Input | What it gives you |
|---|---|
| `.IIF` (QB Desktop) | Chart of accounts **and** transactions — the best single source |
| Journal / Transaction Detail report | Transactions, grouped exactly by `Trans #` |
| General Ledger report | Transactions, reassembled from the per-account sections |
| Trial Balance report | Chart of accounts plus a balanced opening entry |
| Account Listing / Chart of Accounts | Account names, types, numbers, descriptions |
| QuickBooks Online CSV exports | Same reports; the alternate column wording is recognised |

### What it cannot read: .QBB and other company files

`.QBB` (backup), `.QBW` (company file), `.QBM` (portable), and the Accountant's
Copy formats `.QBX` / `.QBA` / `.QBY` are proprietary binary containers with no
published specification. Nothing outside QuickBooks can open one, so the
converter refuses them and prints the restore-and-export steps instead of
failing with a parse error.

The route is always the same: restore or open the file in QuickBooks Desktop,
then export an IIF file or a General Ledger / Account Listing report to CSV and
convert that. If you have no copy of QuickBooks, the file has to go back to
whoever produced it — ask them for those two reports as CSV.

`.QBO` (Web Connect) is refused for a different reason: it is a bank statement
download, so it carries one side of each transaction and no chart of accounts.
Import it into QuickBooks, categorise it, then export a report.

CSV, TSV, and `.xlsx` are all read. Pass several files at once and they are
merged — pairing an **Account Listing** with a **General Ledger** is the
recommended combination, because the listing supplies the account types the
ledger leaves out.

### Exporting from QuickBooks

* **Desktop** — Reports → *Accountant & Taxes* → *General Ledger* (or *Journal*,
  *Trial Balance*, *Account Listing*) → **Excel → Create New Worksheet → Export
  to a comma separated values (.csv) file**. For IIF: File → Utilities → Export
  → *Lists to IIF Files*.
* **Online** — Reports → search for *Journal* (or *General Ledger*, *Trial
  Balance*, *Account List*) → set the date range → **Export → Export to Excel**
  (or CSV).

Set the report period to the range you want converted; the converter takes what
the report contains.

## Reviewing the mapping before you convert

Auto-assigned account numbers and inferred types are a starting point, not a
decision. Dump them, edit them, feed them back:

```bash
qb2drake init-map export.iif -o account_map.csv
$EDITOR account_map.csv
qb2drake convert export.iif --account-map account_map.csv -o drake_import/
```

`account_map.csv` has one row per account:

```
quickbooks_account,quickbooks_type,drake_account_number,drake_account_type,drake_description,division
Utilities:Electric,EXP,6210,Expense,Electric service,
```

Anything you fill in wins over the automatic mapping. Blank cells keep it.

## How the mapping works

**Account types.** IIF codes (`BANK`, `AR`, `COGS`, `EXINC`, …) and report
labels (`Other Current Liability`, `Accounts Receivable (A/R)`, …) map to Drake's
classifications: Asset, Liability, Equity, Income, Cost of Sales, Expense,
Other Income, Other Expense. When a type is missing, the account inherits its
parent's; failing that it is guessed from the account name; failing that it
falls to `--default-type` (Expense) and is flagged in the report.

**Account numbers.** A QuickBooks number is kept as-is. Otherwise a number is
assigned from the range for its type — Asset 1000, Liability 2000, Equity 3000,
Income 4000, Cost of Sales 5000, Expense 6000, Other Income 7000, Other Expense
8000, stepping by 10. Change a range with `--range Expense=6000:5`, or ignore
QuickBooks' numbering entirely with `--renumber`.

**Journals.** The QuickBooks transaction type picks the Drake journal code:
Check / Bill Payment / Credit Card Charge → `CD`, Deposit / Payment / Sales
Receipt → `CR`, Invoice / Credit Memo → `SJ`, Bill / Vendor Credit → `PJ`,
Paycheck / Liability Check → `PR`, everything else → `GJ` (`--default-journal`).

**Levels.** `Utilities:Electric:Summer` becomes level 3. Drake supports four
levels, so anything deeper is flattened to level 4 and reported.

## The conversion report

Every run prints (and `--report FILE` saves) a summary:

```
  accounts written.................. 10
  transactions written.............. 5
  total debits...................... 7,058.24
  total credits..................... 7,058.24
  difference........................ 0.00
```

followed by errors and warnings. **Errors** are things Drake will reject —
entries that do not balance, missing dates, duplicate account numbers,
transactions referencing an account that is not in the chart. The files are
still written so you can look at them; `--strict` exits non-zero instead.
**Warnings** are judgement calls the converter made for you: inferred account
types, created parent accounts, flattened levels.

## Options

```
--account-map FILE      account overrides from `init-map`
--profile FILE          output column layout from `dump-profile`
--default-type TYPE     classification for accounts that cannot be typed
--renumber              ignore QuickBooks numbers, assign from the ranges
--range TYPE=START:STEP override one auto-numbering range (repeatable)
--division CODE         stamp a Drake division on every row
--default-journal CODE  journal for transaction types with no mapping
--group-by MODE         auto | trans-no | none — how report rows fold into entries
--no-opening-entry      Trial Balance input: chart only, no opening entry
--no-sort               keep source row order instead of sorting by date
--report FILE           also write the report to a file
--strict                exit non-zero when there are errors
```

`--group-by` is worth knowing about. `auto` uses `Trans #` when the report has
one (exact), and otherwise rebuilds General Ledger entries by matching date,
transaction type, reference number, and name. That last case is a heuristic: two
entries on the same day, of the same type, with no reference number and the same
payee will be merged into one. They still balance, and the totals are unchanged,
but if you need the entries kept apart, use `--group-by none` and split them by
hand — or convert from a Journal report or IIF file instead, where the grouping
is exact.

## What is not converted

Accounting data only — the chart of accounts and journal entries. It does not
bring across customers, vendors, 1099 data, employees, payroll, inventory items,
open A/R or A/P invoice detail, budgets, or attachments. A/R and A/P come across
as account balances, not as open documents.

## Using it as a library

```python
from qb2drake import convert

result = convert(["general_ledger.csv", "account_listing.csv"], "drake_import/")
print(result.report.render())
if not result.report.ok:
    raise SystemExit("fix the source data first")
```

## Tests

```bash
python -m unittest discover -s tests -v
```

51 tests covering each input format, the mapping rules, validation, and the
generated files. `samples/` holds a small example of every supported export.
