# Lab 5 — Reflection Questions

**Name:** S.R Lokesh Adithya
**SRN:** PES1UG24CS392
**Section:** G
**File analysed:** `blood_donation.py` (`SETAPESU26/L5_28_blood_donation`)

---

## Q1. What is the purpose and scope of static code analysis, and what can it not do?

Static analysis examines source code **without executing it**. It parses the
code into an abstract syntax tree and reasons about what the code *says*,
rather than observing what it *does* at runtime. That gives it one large
advantage and one hard limit.

The advantage is **coverage**. Running `blood_donation.py` exercised exactly
one path: four registrations, three donation attempts, two stock queries.
Pylint, Bandit and Flake8 read all 85 lines, including `donorSheetPath` and
`notifyDonors`, which the demonstration never calls. The single **High**
severity finding in this lab — the `os.system` command injection — was in one
of those unreachable functions. No amount of running the program would have
found it; testing only reaches code that executes.

The limit is that static analysis knows the shape of the code, not its
**meaning**. The clearest example from this lab is issue #10: `COMPATIBLE` was
missing the `A-`, `B-` and `AB-` entries, so `units_for("A-")` reported zero
compatible units for a patient whose blood was actually in stock. In a blood
bank that is the most dangerous defect in the file, and all three tools gave it
a clean pass — the dictionary was syntactically perfect, the lookup was valid
Python, and the `except Exception` handler made the failure look like a
deliberate design choice. A tool cannot know that there are eight blood groups
and that five entries is therefore wrong.

So the honest scope is: static analysis is a **filter, not a verdict**. It
clears away the mechanical faults — the style noise, the unsafe API calls, the
known Python traps — cheaply and exhaustively, which is precisely what frees
reviewer attention for the domain logic that only a human who understands blood
compatibility can check. It is complementary to testing and review, not a
substitute for either.

---

## Q2. Which of the three tools was most useful, and how do their roles differ?

They are not interchangeable, and the file showed why — each tool found a class
of problem that the other two were blind to.

**Bandit was the most valuable per finding.** It produced only four results,
but one was the `os.system` injection: the only defect in the file that an
attacker could exploit from outside, in a function no test would ever reach.
Four findings, one of them genuinely serious, is a far better signal-to-noise
ratio than twenty-eight style messages. Bandit also flagged two subtleties I
would not have thought to look for: that `tempfile.mktemp()` carries a
time-of-check/time-of-use race, and that `assert` is **deleted** when Python
runs with `-O`, which quietly removes the blood-group validation in a
production deployment. Both are the kind of thing you only know if you have
been told, which is exactly what a tool encoding institutional knowledge is
for.

**Pylint was the most useful overall**, because it was the only tool that found
actual bugs rather than violations. Two of its warnings were real defects:
`W0102` caught the mutable default `notes=[]`, where the list is created once
at definition time and silently shared across every call — a trap that produces
wrong behaviour that is maddening to debug by hand. `W0718` caught the
`except Exception`, and following that warning up is what led me to the
compatibility-table bug. That is the pattern worth remembering: the broad
handler was not just untidy, it was **load-bearing concealment**. Narrowing it
to `except KeyError` was what made the hidden defect visible.

**Flake8 was the least interesting but the cheapest to satisfy** — four
formatting issues, all fixed in under a minute. Its value is not in any single
message; it is that mechanical consistency is no longer something anyone has to
discuss. Nobody has to leave a review comment about spaces around `=` again.

The division of labour the handout describes held up exactly: Flake8 checks
**grammar**, Pylint acts as a **strict reviewer**, Bandit is the **security
guard**. Running only one of the three would have left a whole category of
problem untouched.

---

## Q3. What surprised you, and which fix was the hardest to decide on?

Two things surprised me.

The first was the **inverted relationship between severity and effort**. Pylint
reported 28 messages and 22 of them were naming and docstring conventions —
real but mechanical. The three findings that mattered (`W0102`, `W0718`, and
Bandit's `B605`) were a small minority of a noisy report. The lesson is that a
report's *length* says nothing about its *importance*, and that clearing a
report by count is the wrong instinct. If I had chased the score by adding
docstrings and renaming functions, I would have reached 10.00/10 with the
command injection still in the file.

The second was finding that **a warning can be a symptom rather than the
disease**. I nearly dismissed `W0718` as pedantry — catching `Exception` is
lazy, but it works. Narrowing it is what exposed the missing blood-group
entries. The warning was not the problem; it was the thing hiding the problem.

The hardest decision was **how far to go on the `os.system` fix**. The textbook
answer is `subprocess.run(["send-sms", *phone_list])` — a list argument, no
shell, no injection. I implemented that first, and Bandit still returned three
Low findings: `B404` (importing subprocess at all), `B603` (subprocess with
unvalidated input) and `B607` (partial executable path). I could have silenced
them with `# nosec`, but a suppression comment is a note saying "I decided this
was fine", not a fix.

So I went further and removed the external process entirely: `notify_donors`
now validates each number against `^\+?[0-9]{10,15}$` and returns the queue of
accepted numbers. The reasoning is that the safest way to handle an injection
risk is to delete the interpreter you were injecting into. That took Bandit to
zero without a single suppression. The trade-off is honest and worth stating:
the function no longer actually sends an SMS, so in a real system the dispatch
would move behind a gateway's API client rather than a shell command — which is
how it should have been built in the first place. For a helper the handout
marks as "not called by the demo", removing the attack surface was the right
call; in production the same reasoning points at an HTTP client, not
`os.system`.

---

## Q4. How does static analysis contribute to code quality and maintainability, and would you use it on your own projects?

Its real contribution is **shifting defect discovery left**. Each of these
findings would have cost progressively more the later it was found. The
`os.system` injection, found in a 60-minute lab, is a two-line change; found in
production it is an incident. The mutable default would have shown up as a
support ticket about "notes from the wrong donor", and tracked down by hand it
could have taken an afternoon — Pylint names it in milliseconds.

There is also a compounding effect on maintainability that is easy to
undervalue. Once naming and formatting are enforced by a tool, they stop being
anyone's judgement call. Reviews move from "put a space here" to "is this
compatibility table right?" — and in this file, that second question was the
one that actually mattered. Clearing the noise is what created room to notice
the real bug. The docstrings matter for the same reason: the 90-day donation
gap and the 18–65 age rule are now stated in the code, so the next person does
not have to re-derive the business rules from arithmetic on `timedelta`.

I would use all three, with one qualification. The right place is a **CI gate
on every pull request**, not something run by hand once — a check that only
runs when someone remembers is a check that does not exist. Bandit and Flake8
I would make blocking immediately: they are fast, near-zero false positives,
and nothing good comes of merging past them. Pylint I would introduce with a
tuned configuration and a per-file threshold rather than demanding 10.00/10
everywhere, because a tool that cries wolf gets ignored, and an ignored tool is
worse than no tool.

The caveat I would keep in front of me is the one from Q1: **a clean report is
not a correct program**. This file now scores Pylint 10.00/10, Bandit 0 and
Flake8 0 — and the most dangerous bug in it was one no tool ever mentioned.
Static analysis buys the attention to find that class of defect; it does not
find it for you.
