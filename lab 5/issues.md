# Lab 5 — Static Code Analysis: Issues Identified and Fixed

**Name:** S.R Lokesh Adithya
**SRN:** PES1UG24CS392
**Section:** G
**Assigned repository:** `SETAPESU26/L5_28_blood_donation` (row 28 of the Lab 5 repo assignment)
**File analysed:** `blood_donation.py`

---

## 1. Environment and commands used

```bash
python3 -m venv venv
source venv/bin/activate
pip install pylint bandit flake8

python blood_donation.py                                # baseline behaviour

pylint blood_donation.py > pylint_report.txt
bandit -r blood_donation.py > bandit_report.txt
flake8 blood_donation.py > flake8_report.txt
```

Tool versions: Pylint 4.1.3, Bandit 1.9.4, Flake8 7.5.0 (CPython 3.13).

---

## 2. Result summary

| Tool | Before | After |
|------|--------|-------|
| **Pylint** | **4.81 / 10** — 28 messages | **10.00 / 10** — 0 messages |
| **Bandit** | **4 issues** — 1 High, 1 Medium, 2 Low | **0 issues** |
| **Flake8** | **4 issues** — E501, E303, E261, E225 | **0 issues** |

Reports are in `reports/before/` and `reports/after/`.

The program's demonstration output is **byte-for-byte identical** before and
after every change:

```
Stock: {'A+': 0, 'A-': 0, 'B+': 0, 'B-': 0, 'O+': 2, 'O-': 1, 'AB+': 0, 'AB-': 0}
Units for an A+ patient: 3
Units for a Z+ patient: 0
Is O- universal? True
Low stock groups: ['A+', 'A-', 'B+', 'B-', 'O-', 'AB+', 'AB-']
Donors eligible today: []
```

---

## 3. Issue table

Ordered by severity, highest first. Line numbers refer to the original file.

### 3.1 Security issues — Bandit

| # | Issue | Type | Tool / Code | Severity | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|----------|---------|-------------|--------------|
| 1 | Shell command built by string concatenation | Security — OS command injection | Bandit `B605` start_process_with_a_shell, CWE-78 | **High** | 65 | `notifyDonors` called `os.system("send-sms " + " ".join(phoneList))`. The phone numbers come from the caller and are pasted straight into a shell command line, so a value such as `0; rm -rf ~` would be executed by the shell as a second command. | Removed the shell entirely rather than just quoting it. `notify_donors` now validates each number against `^\+?[0-9]{10,15}$` and returns the queue of accepted numbers, so no external process is spawned and there is no injection surface left. |
| 2 | Insecure temporary file creation | Security — race condition | Bandit `B306` blacklist (mktemp), CWE-377 | **Medium** | 60 | `tempfile.mktemp()` only returns a name that was unused *at the moment it was called*. Between that check and the program opening the file, another process can create a file or symlink at the same path (a time-of-check/time-of-use race), letting an attacker redirect or read the donor sheet. | Switched to `tempfile.mkstemp()`, which creates the file atomically with `O_EXCL` and returns an already-open descriptor. The descriptor is closed and the path returned, preserving the original signature. |
| 3 | Hardcoded password in source | Security — credential exposure | Bandit `B105` hardcoded_password_string, CWE-259 | Low | 5 | `OFFICER_PASSWORD = "bloodbank-demo"` puts a credential in the source file, so it is in the Git history, in every clone and visible to anyone with read access to the repository. It also cannot be rotated without a code change. | Read from the environment instead: `os.environ.get("BLOODBANK_OFFICER_PASSWORD", "")`. The value is supplied at deployment time and never committed. |
| 4 | `assert` used for input validation | Security / Robustness | Bandit `B101` assert_used, CWE-703 | Low | 18 | `assert bloodGroup in stock` is removed by the interpreter when Python runs with `-O`, so in an optimised deployment the blood-group check silently disappears and an unknown group would reach `donors` and corrupt the stock dictionary. `assert` is a development aid, not a validation mechanism. | Replaced with an explicit check that raises: `if blood_group not in stock: raise ValueError(...)`. This runs under every optimisation level. |

### 3.2 Code quality issues — Pylint

| # | Issue | Type | Tool / Code | Severity | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|----------|---------|-------------|--------------|
| 5 | Mutable default argument | **Bug** | Pylint `W0102` dangerous-default-value | **High (warning)** | 17 | `def registerDonor(..., notes=[])`. The default list is created **once**, when the function is defined, and is then shared by every call that omits the argument. Rejection messages therefore accumulate across unrelated calls, so the second caller sees the first caller's notes. A classic Python trap. | Default is now `notes=None`, with `if notes is None: notes = []` inside the function, so each call that omits the argument gets a fresh list. |
| 6 | Overly broad exception handler | **Bug** | Pylint `W0718` broad-exception-caught | **High (warning)** | 45 | `unitsFor` wrapped its lookup in `except Exception: return 0`. That catches everything — `KeyError`, but equally `TypeError`, a typo-induced `NameError`, even a bug in `sum()` — and reports all of them as "0 units available". For a blood bank that means a lookup failure is indistinguishable from genuinely empty stock. It is also what hid issue #8 below. | Narrowed to `except KeyError`, the only exception the dictionary lookup can legitimately raise. Any other failure now propagates and is visible. |
| 7 | Chained equality comparisons | Readability | Pylint `R1714` consider-using-in | Low (refactor) | 50 | `bloodGroup == "O-" or bloodGroup == "AB+"` repeats the operand and grows awkwardly with each extra group. | Rewritten as `blood_group in UNIVERSAL_GROUPS`, with the tuple declared as a named module constant. |
| 8 | camelCase names throughout | Style — PEP 8 | Pylint `C0103` invalid-name (13 occurrences) | Low (convention) | 17, 27, 33, 42, 49, 53, 58, 63 | Every function and several arguments used Java-style `camelCase` (`registerDonor`, `bloodGroup`, `lastDonation`, `phoneList`, …). PEP 8 reserves `camelCase` for class names; functions and variables are `snake_case`. Mixed conventions in one codebase slow every future reader down. | Renamed all 13 identifiers to `snake_case` (`register_donor`, `blood_group`, `last_donation`, `phone_list`, …) and updated every call site. |
| 9 | Missing docstrings | Maintainability | Pylint `C0114` missing-module-docstring, `C0116` missing-function-docstring (9 occurrences) | Low (convention) | 1, 17, 27, 33, 42, 49, 53, 58, 63, 68 | Neither the module nor any of the nine functions documented its purpose, so a reader had to infer the 90-day donation rule and the 18–65 age rule from the code body. | Added a module docstring describing the register, and a docstring to every function stating what it returns and what it raises. |

### 3.3 Logic defects found while reading the reports

These were **not reported by any of the three tools**. They were found by
following up the warnings above — which is the point of reading a report
rather than just clearing it.

| # | Issue | Type | Tool / Code | Severity | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|----------|---------|-------------|--------------|
| 10 | Incomplete blood-group compatibility table | **Bug** — silent wrong answer | None (found by investigating `W0718`) | **High** | 8–14 | `COMPATIBLE` only had entries for `A+`, `B+`, `O+`, `O-` and `AB+`. For an `A-`, `B-` or `AB-` patient the lookup raised `KeyError`, which the broad `except Exception` swallowed, so `unitsFor("A-")` reported **0 compatible units available** when stock existed. Three of the eight blood groups silently got a clinically wrong answer, and no tool could see it because the handler made the program look correct. | Added the three missing entries with the correct medical compatibility (`A-` ← A-, O-; `B-` ← B-, O-; `AB-` ← A-, B-, O-, AB-) and replaced `list(stock)` for `AB+` with an explicit list so the table no longer depends on `stock`'s insertion order. |
| 11 | `main()` executed at import time | Design | None | Medium | 85 | The file ended with a bare `main()` call, so merely importing the module — to unit-test `can_donate`, or to reuse `units_for` elsewhere — ran the whole demonstration and mutated the global `stock`. | Guarded with `if __name__ == "__main__": main()`, so the demo runs only when the file is executed directly. |
| 12 | Magic numbers | Maintainability | None | Low | 19, 30, 53 | The age limits `18`/`65` and the `90`-day donation gap were literals buried in expressions, with the rule they encode left implicit. | Extracted as `MIN_DONOR_AGE`, `MAX_DONOR_AGE` and `DONATION_GAP_DAYS`. |

### 3.4 Formatting issues — Flake8

| # | Issue | Type | Tool / Code | Severity | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|----------|---------|-------------|--------------|
| 13 | Line too long (82 > 79) | Style — PEP 8 | Flake8 `E501` | Low | 7 | The `stock` dictionary literal ran to 82 characters, past PEP 8's 79-column limit. | Split the literal across two lines, four blood groups each. |
| 14 | Too many blank lines (3) | Style — PEP 8 | Flake8 `E303` | Low | 58 | Three blank lines before `donorSheetPath`; PEP 8 specifies exactly two between top-level definitions. | Removed the extra blank line. |
| 15 | Missing two spaces before inline comment | Style — PEP 8 | Flake8 `E261` | Low | 80 | `low_stock()) # below 2 units` — PEP 8 requires at least two spaces before an inline `#`. | Added the second space. |
| 16 | Missing whitespace around operator | Style — PEP 8 | Flake8 `E225` | Low | 81 | `eligible=[...]` — no spaces around the assignment operator. | Written as `eligible = [...]`. |

---

## 4. Commit history

The handout asks for three commits, one per tool. Each was verified by
re-running all three tools and re-running the program before committing.

| Commit | Scope | Effect |
|--------|-------|--------|
| `ad97f2f` | `fix(security)` — Bandit findings #1–4 | Bandit 4 issues (1 High, 1 Medium, 2 Low) → **0** |
| `9225a39` | `refactor(quality)` — Pylint findings #5–9, plus logic defects #10–12 | Pylint **4.81/10 → 10.00/10** |
| `64c97f5` | `style(pep8)` — Flake8 findings #13–16 | Flake8 4 issues → **0** |

The commits are deliberately ordered security → quality → style, so the
highest-severity change is the smallest and most reviewable diff, and the
large cosmetic rename does not bury it.
