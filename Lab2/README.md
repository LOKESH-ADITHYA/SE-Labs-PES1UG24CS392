# Lab 2 — Agile Backlog Creation & Sprint Simulation in Jira

**PES University — Dept. of CSE** · **SRN:** PES1UG24CS392 · **Section:** G
**Problem Statement #24:** Public Bus Live Tracking & Crowding Estimator

Continues the scenario from Lab 1 — the five functional requirements defined there become the five Epics here.

---

## Submission

**[`Lab2_PES1UG24CS392_G.pdf`](Lab2_PES1UG24CS392_G.pdf)** — 6 pages: cover with the Jira workspace link, the four required screenshots (Epics & User Stories, backlog with story points, active sprint board, both burndown charts) and the reflection answers.

**Jira workspace:** `https://stu-team-zdgyycel.atlassian.net/jira/software/projects/SCRUM/boards/1`

---

## Backlog

| Epic | Traces to (Lab 1) | Stories | Points |
|---|---|---|---|
| EPIC 1 — Real-Time Vehicle Tracking & ETA Engine | FR-001 | 3 | 26 |
| EPIC 2 — Passenger Crowding Estimation | FR-002 | 3 | 16 |
| EPIC 3 — Commuter Journey Information | FR-003 | 3 | 18 |
| EPIC 4 — Arrival Alerts & Notifications | FR-004 | 2 | 10 |
| EPIC 5 — Fleet Operations Control | FR-005 | 3 | 21 |
| **Total** | | **14** | **91** |

Every user story is written in `As a / I want / So that` form with acceptance criteria, a priority (High / Medium) and a Fibonacci story-point estimate.

## Sprint outcomes

| | Sprint 1 | Sprint 2 |
|---|---|---|
| Dates | 18 – 25 Aug 2026 | 25 Aug – 1 Sep 2026 |
| Scope | EPIC 1 + EPIC 2 (SCRUM-6 → SCRUM-11) | EPIC 3, 4, 5 (SCRUM-12 → SCRUM-19) |
| Committed | 42 points, 6 stories | 49 points, 8 stories |
| Completed | 42 points (100%) | 36 points (73%) |
| Carried over | none | SCRUM-18 (5 pts), SCRUM-19 (8 pts) |
| Status | Closed | Closed |

Average velocity across the two sprints: **39 points**.

## Reflection — summary

Full answers are in the PDF. In short:

1. **Estimates vs effort** — relative ordering held up (the 13-point ETA engine really is the hardest item), but points don't capture *dependencies*, which is what actually caused Sprint 2 to miss.
2. **Backlog prioritisation** — validated by what slipped: both carried-over stories were Medium-priority items at the end of a dependency chain. No High-priority work was left unfinished.
3. **Plan vs outcome** — Sprint 1 landed exactly; Sprint 2 was over-committed by roughly 10 points because its velocity target was set from Sprint 1's independent work while EPIC 5 is strictly sequential.
4. **Burndown insight** — a line reaching zero is not proof of success. Sprint 2's reached zero only because 13 points left the sprint as a scope reduction at close, not as delivered work.
