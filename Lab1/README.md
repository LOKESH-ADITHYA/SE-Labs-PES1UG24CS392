# Lab 1 — Requirements Engineering & UML Use-Case Modelling

**PES University — Dept. of CSE**
**Problem Statement #24:** Public Bus Live Tracking & Crowding Estimator
**Primary Domain:** Smart Cities, Transport & Logistics
**SRN:** PES1UG24CS392

A municipal transit intelligence platform that ingests GPS feeds from city buses, estimates arrival times (ETA) at downstream stops, and computes passenger crowding levels from ticketing sensors.

---

## Submission

**[`00_Lab1_Complete_Submission.pdf`](00_Lab1_Complete_Submission.pdf)** — all three deliverables in one 5-page PDF:

| Page | Deliverable |
|---|---|
| 1 | Cover — SRN, problem statement, contents |
| 2–3 | **Requirements Table** — 5 FRs (FR-001…FR-005) + 2 NFRs (NFR-001, NFR-002) with Req ID, Type, Description, Priority, Acceptance Criteria and Rationale |
| 4 | **UML Use-Case Diagram** — 5 actors, 10 use cases (UC-01…UC-10), «include» and «extend» relationships |
| 5 | **Use-Case Flow Specification** — UC-02 View Live Bus Location & ETA: preconditions, postconditions, main success scenario and one alternate flow |

Source files: [`01_Requirements_Table.md`](01_Requirements_Table.md), [`03_UseCase_Flow_Specification.md`](03_UseCase_Flow_Specification.md) (render directly on GitHub) and [`02_UseCase_Diagram.puml`](02_UseCase_Diagram.puml) (PlantUML).

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

### Traceability

FR-001 → UC-09, UC-07 · FR-002 → UC-03, UC-08 · FR-003 → UC-01, UC-02 · FR-004 → UC-04 · FR-005 → UC-05, UC-06 · NFR-001 constrains UC-09 and UC-07 · NFR-002 constrains UC-10 and all data paths.

---

## Regenerating the diagram

```bash
java -jar plantuml.jar -tpng 02_UseCase_Diagram.puml
```
