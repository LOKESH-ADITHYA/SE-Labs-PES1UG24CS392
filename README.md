# SE-Labs-PES1UG24CS392

Software Engineering lab deliverables — **PES University, Dept. of CSE**

| Field | Value |
|---|---|
| **SRN** | PES1UG24CS392 |
| **Section** | G |
| **Problem Statement** | #24 — Public Bus Live Tracking & Crowding Estimator |
| **Primary Domain** | Smart Cities, Transport & Logistics |
| **Target Actors** | Commuter, Fleet Controller |

> A municipal transit intelligence platform ingesting GPS feeds from city buses, estimating arrival times (ETA) at downstream stops, and computing passenger crowding levels from ticketing sensors.

---

## Labs

| Lab | Title | Deliverables |
|---|---|---|
| [Lab 1](Lab1/) | Requirements Engineering & UML Use-Case Modelling | Requirements table (5 FR + 2 NFR), use-case diagram, use-case flow specification |
| [Lab 3](Lab3/) | Component Modelling & Architectural Pattern Selection | UML component diagram, architectural justification |

Lab 2 (Agile Backlog & Sprint Simulation) was delivered in Jira rather than as repository files.

---

## Repository Structure

```
SE-Labs-PES1UG24CS392/
├── README.md
├── Lab1/
│   ├── README.md
│   ├── 00_Lab1_Complete_Submission.pdf     # submitted PDF
│   ├── 01_Requirements_Table.md
│   ├── 02_UseCase_Diagram.png
│   ├── 02_UseCase_Diagram.puml
│   └── 03_UseCase_Flow_Specification.md
└── Lab3/
    ├── README.md
    ├── Lab3_PES1UG24CS392_G.pdf            # submitted PDF
    ├── 01_Component_Diagram.png
    ├── 01_Component_Diagram.svg
    ├── 01_Component_Diagram_source.py
    └── 02_Architectural_Justification.md
```

---

## Continuity across labs

The five functional requirements defined in Lab 1 carry through the whole series:

| Lab 1 requirement | Lab 2 epic | Lab 3 component |
|---|---|---|
| FR-001 GPS ingestion & ETA | EPIC 1 | Telemetry Ingestion Service, ETA Engine Service |
| FR-002 Crowding estimation | EPIC 2 | Crowding Estimator Service |
| FR-003 Commuter query | EPIC 3 | Commuter Query Service |
| FR-004 Arrival alerts | EPIC 4 | Commuter Query Service → Push Notification Provider |
| FR-005 Fleet control | EPIC 5 | Fleet Operations Service |
