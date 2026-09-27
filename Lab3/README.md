# Lab 3 — Component Modelling & Architectural Pattern Selection

**PES University — Dept. of CSE** · **SRN:** PES1UG24CS392 · **Section:** G
**Problem Statement #24:** Public Bus Live Tracking & Crowding Estimator

Continues the scenario used in Lab 1 (requirements and use cases) and Lab 2 (Agile backlog).

---

## Submission

**[`Lab3_PES1UG24CS392_G.pdf`](Lab3_PES1UG24CS392_G.pdf)** — the submitted file: component diagram (page 1) and the one-page architectural justification (page 2).

| # | Deliverable | File |
|---|---|---|
| 1 | UML Component Diagram | [`01_Component_Diagram.png`](01_Component_Diagram.png) · [SVG](01_Component_Diagram.svg) |
| 2 | Architectural Justification (1 page) | [`02_Architectural_Justification.md`](02_Architectural_Justification.md) |

Source for the diagram: [`01_Component_Diagram_source.py`](01_Component_Diagram_source.py) (generates the SVG).

---

## Architecture

**Microservices**, chosen over Layered and Client–Server because:

1. Telemetry ingestion (constant ~200 msg/s from 1,000 vehicles) and commuter queries (sharply rush-hour peaked) scale for unrelated reasons and must be provisioned separately.
2. Crowding estimation depends on the least reliable hardware in the system; isolating it means a sensor outage degrades one badge instead of taking ETAs down with it.

**Security:** the Fleet Operations Service — the only component that can dispatch a bus (FR-005) — is a separate deployable reachable only through the API Gateway's RBAC boundary, so a flaw in the commuter API has no network route to it (NFR-002).

**Performance:** the ETA Engine is replicated independently with route state partitioned by route ID, meeting NFR-001's p95 < 2 s recomputation across 1,000 vehicles without over-provisioning anything else.

---

## Components (7)

| Component | Responsibility | Traces to |
|---|---|---|
| API Gateway Component | TLS termination, authentication, RBAC, request routing | NFR-002 |
| Telemetry Ingestion Service | Receives GPS fixes every 5 s, publishes position events | FR-001 |
| ETA Engine Service | Computes arrival times from position, distance and traffic speed | FR-001, NFR-001 |
| Crowding Estimator Service | Derives occupancy from ticketing / APC sensors, bands it | FR-002 |
| Commuter Query Service | Route and stop search, arrivals list, alert subscriptions | FR-003, FR-004 |
| Fleet Operations Service | Fleet dashboard, exception flagging, relief-bus dispatch | FR-005 |
| Transit Data Store Component | Routes, timetables, vehicle state, capacities | all |

External: Onboard GPS Unit, Ticketing / APC Sensor, Commuter Mobile App, Fleet Controller Console, Push Notification Provider.

## Interfaces (10)

| Interface | Provided by | Required by |
|---|---|---|
| `ITelemetryIngest` | Telemetry Ingestion | Onboard GPS Unit (MQTT / TLS 1.3) |
| `ICrowdingIngest` | Crowding Estimator | Ticketing / APC Sensor (MQTT / TLS 1.3) |
| `IVehiclePosition` | Telemetry Ingestion | ETA Engine (event stream) |
| `IEtaQuery` | ETA Engine | Commuter Query, Fleet Operations (REST) |
| `ICrowdingQuery` | Crowding Estimator | Commuter Query, Fleet Operations (REST) |
| `ICommuterQuery` | Commuter Query | API Gateway (REST) |
| `IFleetControl` | Fleet Operations | API Gateway (REST + RBAC) |
| `ICommuterApi` | API Gateway | Commuter Mobile App (HTTPS) |
| `IFleetConsoleApi` | API Gateway | Fleet Controller Console (HTTPS) |
| `ITransitData` | Transit Data Store | Telemetry Ingestion, ETA Engine, Crowding Estimator, Fleet Operations |
