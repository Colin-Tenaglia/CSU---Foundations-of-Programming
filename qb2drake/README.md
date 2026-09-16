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

## The app

```bash
python qb2drake_gui.pyw        # from a checkout
qb2drake gui                   # if installed
```

On Windows, `qb2drake_gui.pyw` is double-clickable and opens without a console
window. The app follows the order the work happens in:

1. **QuickBooks export files** — add one `.IIF`, or add both a General Ledger
   and an Account Listing CSV.
2. **Drake blank templates** — point at the blank templates from
   *Tools > Spreadsheets > Export tab* so the output matches your program
   year's columns exactly.
3. **Save the converted files to** — an output folder.
4. **Options** — write an `.IIF` as well, renumber accounts, set a division.

Press **Convert** and the result panel shows the full report: totals, anything
Drake would reject in red, warnings in amber, the files written, and the import
steps. The status bar says plainly whether it is ready to import. *Help* has
the export and import instructions, including what the Client Code is.

Everything below is the same converter from the command line.

## Building a standalone .exe

So it can be handed to someone without Python installed. Must be run on
Windows — PyInstaller does not cross-compile.

```bat
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed ^
            --name "QuickBooks to Drake" qb2drake_gui.pyw
```

The result is `dist\QuickBooks to Drake.exe`, a single file to copy anywhere.

## Install


No dependencies for CSV/IIF input:

```bash
python -m qb2drake --help          # run straight from the repo
pip install -e .                   # or install `qb2drake` and `qb2drake-gui`
pip install -e ".[excel]"          # add openpyxl for .xlsx input
```

The app needs tkinter, which ships with Python on Windows and macOS. On
Debian/Ubuntu it is a separate package: `sudo apt install python3-tk`.

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
drake_chart_of_accounts.csv     # Tools > Spreadsheets > Import
drake_transactions.csv          # Tools > Spreadsheets > Import
drake_chart_of_accounts.IIF     # with --iif: File > Import > Import QuickBooks
```

## Getting the files into Drake Accounting

Drake has **two separate import doors**, and this trips people up: the
QuickBooks wizard does not import transactions.

| | `File > Import > Import QuickBooks` | `Tools > Spreadsheets > Import` |
|---|---|---|
| Takes | one `.IIF` file | CSV matching Drake's blank template |
| Imports | Employees, Customers, **Chart of Accounts**, Vendors | **Journal Entries**, Chart of Accounts, and more |
| Needs | a **Client Code** | a client already selected |

So the chart of accounts can go either way; **journal entries only go through
the spreadsheet import**. There is no transactions checkbox on the QuickBooks
wizard — if you were looking for one, that is why you could not find it.

### The Client Code

It is **not** in your QuickBooks data, and it is not something to look up. It
is Drake Accounting's own identifier for the client, and **you choose it**:

* up to **8 characters** — letters, digits, and underscores
* type a code that **does not exist yet** and Drake **creates a new client**
  with it
* type an **existing** client's code and Drake imports only the pieces that
  client does not already have

So for a new client, invent something like `ACME01` and press Import. That is
the whole story.

One caveat from Drake's own instructions: each selection imports **once**. Once
the Chart of Accounts has come in under a client code, that checkbox is greyed
out for that client. Get the chart right before importing rather than expecting
to re-import over the top.

### Matching Drake's exact column layout

Do not guess at it, and do not trust the defaults in this tool — Drake's
templates differ between program years. Get the real template out of your own
installation and build the layout from it:

1. In Drake Accounting: **Tools > Spreadsheets > Export tab** → save the blank
   templates (`Blank_JournalEntries_Template.csv`,
   `Blank_ChartOfAccounts_Template.csv`).
2. Build the profile from them:

```bash
qb2drake profile-from-template \
    Blank_JournalEntries_Template.csv \
    Blank_ChartOfAccounts_Template.csv \
    -o drake_profile.json

qb2drake convert export.iif --profile drake_profile.json -o drake_import/
```

The generated files then carry Drake's own header row, in Drake's own order.
Columns the matcher cannot place are **kept in position and left blank**, and
listed for you:

```
  Blank_JournalEntries_Template.csv: could not place 1 column(s):
    - 'Batch ID'
```

Fill one in by editing its entry in the JSON — set a `"field"` to pull a value,
or a `"constant"` for a fixed one. `dump-profile` still writes the built-in
default layout if you have no template to hand.

| Chart fields | Transaction fields |
|---|---|
| `level`, `number`, `description`, `type`, `normal_balance`, `division`, `parent_number`, `source_name`, `opening_balance` | `entry_no`, `date`, `journal`, `reference`, `account_number`, `account_name`, `description`, `memo`, `name`, `debit`, `credit`, `amount`, `division` |

### Writing an .IIF for the QuickBooks wizard

`--iif` writes the chart of accounts as `drake_chart_of_accounts.IIF`:

```bash
qb2drake convert qbo_report.csv --iif -o drake_import/
```

Worth doing in two situations:

* **QuickBooks Online has no IIF export at all**, so an Online client cannot
  use Drake's QuickBooks wizard. Converting an Online report into IIF opens
  that door.
* **QuickBooks files exported without account numbers.** Drake's instructions
  tell you to switch on *Use Account Numbers* in QuickBooks first, because the
  import needs numbered accounts — miss that and the chart arrives unusable.
  Every account written here has a number, assigned if QuickBooks had none.

Account type detail is preserved on the way through, so a Bank account stays
`BANK` rather than flattening to a generic asset. Opening balances are written
as zero deliberately: balances belong in the journal entry import, and carrying
them on the accounts as well would post them twice.

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
--iif                   also write the chart as .IIF for the QuickBooks wizard
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
python -m unittest discover -s tests -v     # 87 tests
xvfb-run -a python -m unittest discover -s tests   # include the app tests headlessly
```

87 tests covering each input format, the mapping rules, validation, the
generated files, the conversion job, and the app itself — including that
closing the window mid-conversion shuts down cleanly. The app tests skip
automatically when there is no tkinter or no display. `samples/` holds a small
example of every supported export.
