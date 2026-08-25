# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**PES University — Dept. of CSE**
**Problem Statement #24:** Public Bus Live Tracking & Crowding Estimator
**Primary Domain:** Smart Cities, Transport & Logistics
**SRN:** PES1UG24CS392

A municipal transit intelligence platform that ingests GPS feeds from city buses, estimates arrival times (ETA) at downstream stops, and computes passenger crowding levels from ticketing sensors.

---

## Deliverables

**All three deliverables in one file:** [`00_Lab1_Complete_Submission.pdf`](00_Lab1_Complete_Submission.pdf) — cover page, requirements table, use-case diagram and flow specification, 5 pages.

They are also committed individually below, in the formats the handout names:

| # | Deliverable | Required format | File |
|---|---|---|---|
| 1 | Requirements Table — 5 FRs + 2 NFRs with Req ID, Type, Description, Priority, Acceptance Criteria, Rationale | Word / Excel | [`01_Requirements_Table.docx`](01_Requirements_Table.docx) · [PDF](01_Requirements_Table.pdf) |
| 2 | UML Use-Case Diagram — all actors, use cases labelled UC-01…UC-10, «include» and «extend» relationships | PDF | [`02_UseCase_Diagram.pdf`](02_UseCase_Diagram.pdf) |
| 3 | Use-Case Flow Specification — UC-02, one page, preconditions / postconditions / main success scenario / one alternate flow | Word (p.3) / PDF (p.5) | [`03_UseCase_Flow_Specification.docx`](03_UseCase_Flow_Specification.docx) · [PDF](03_UseCase_Flow_Specification.pdf) |

The handout asks for the flow document as Word on page 3 and as an exported PDF on page 5, so both are included.

Supporting files: [`02_UseCase_Diagram.puml`](02_UseCase_Diagram.puml) (PlantUML source), [`02_UseCase_Diagram.png`](02_UseCase_Diagram.png) (README preview), and Markdown copies of both documents so they render directly on GitHub.

---

## Use-Case Diagram

![Use-Case Diagram](02_UseCase_Diagram.png)

### Actors

| Actor | Kind | Role |
|---|---|---|
| Commuter | Primary | Searches routes/stops, views live ETA and crowding, subscribes to arrival alerts |
| Fleet Controller | Primary | Monitors the fleet dashboard, dispatches relief buses |
| Onboard GPS Unit | Secondary | Supplies the 5-second position telemetry stream |
| Ticketing / APC Sensor | Secondary | Supplies boarding/alighting counts for crowding estimation |
| Push Notification Service | Secondary | Delivers arrival alerts to the commuter's device |

### Use Cases

| ID | Use Case | ID | Use Case |
|---|---|---|---|
| UC-01 | Search Route / Stop | UC-06 | Dispatch Relief Bus |
| UC-02 | View Live Bus Location & ETA | UC-07 | Compute ETA |
| UC-03 | View Crowding Level | UC-08 | Estimate Crowding Level |
| UC-04 | Subscribe to Arrival Alert | UC-09 | Ingest GPS Telemetry |
| UC-05 | Monitor Fleet Dashboard | UC-10 | Authenticate Controller |

### Relationships

**«include»** — the base use case always performs the included one:

- UC-02 → UC-01 Search Route / Stop
- UC-02 → UC-07 Compute ETA
- UC-02 → UC-03 View Crowding Level
- UC-05 → UC-10 Authenticate Controller

**«extend»** — the extending use case runs conditionally at the base's extension point:

- UC-04 Subscribe to Arrival Alert ⇢ UC-02, at extension point *ETA displayed* — only if the commuter opts in
- UC-06 Dispatch Relief Bus ⇢ UC-05, at extension point *Exception flagged* — only when a bus is delayed beyond threshold or holding a *Full* crowding band

---

## Regenerating the diagram

```bash
java -jar plantuml.jar -tpng 02_UseCase_Diagram.puml   # preview
java -jar plantuml.jar -tsvg 02_UseCase_Diagram.puml   # then convert to PDF
```
