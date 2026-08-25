# Lab 1 — Requirements Table

**Problem Statement #24 — Public Bus Live Tracking & Crowding Estimator**
Domain: Smart Cities, Transport & Logistics · SRN: PES1UG24CS392

A municipal transit intelligence platform that ingests GPS feeds from city buses, estimates arrival times (ETA) at downstream stops, and computes passenger crowding levels from ticketing sensors.

---

## 1. Functional Requirements

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| **FR-001** | Functional | The system shall ingest bus GPS coordinates every 5 seconds and recalculate arrival ETAs for all upcoming route stops. | High | **Pass:** ETA for each downstream stop is updated within one 5-second cycle, computed from current traffic speed and remaining route distance.<br>**Fail:** ETA increases while the bus approaches the stop, or the ETA shown is based on telemetry older than 15 seconds. | ETA accuracy is the core value of the platform; every commuter-facing feature depends on this figure, and a stale feed makes predictions drift beyond usefulness. |
| **FR-002** | Functional | The system shall compute an occupancy figure for each active bus from onboard ticketing / passenger-counting sensor events and classify it into a crowding band: *Seats Available* (< 50% of rated capacity), *Standing Room* (50–85%), *Full* (> 85%). | High | **Pass:** For a given sequence of boarding and alighting events the occupancy is computed correctly, the band matches the stated thresholds, and the band is refreshed on every stop departure.<br>**Fail:** Occupancy goes negative, exceeds rated capacity without raising *Full*, or the band is not updated after a stop event. | Crowding is the second capability named in the problem statement. Commuters need it to decide whether to board or wait; controllers need it to detect overloaded services. |
| **FR-003** | Functional | The system shall allow a Commuter to search by route number or by stop and shall display, for every approaching bus, its live position on a map, its ETA at that stop, and its current crowding band. | High | **Pass:** A search on a valid route or stop returns all approaching buses within 3 seconds, each entry carrying position, ETA and crowding band.<br>**Fail:** A valid route or stop returns no result, or a listed bus is missing its ETA or crowding band. | The primary commuter-facing interaction and the entry point to every other commuter feature; without it the computed data never reaches a user. |
| **FR-004** | Functional | The system shall allow a Commuter to subscribe to an arrival alert for a chosen bus at a chosen stop and shall push a notification when the predicted ETA falls below the commuter's chosen lead time (default 5 minutes). | Medium | **Pass:** Exactly one notification is delivered within 30 seconds of the ETA crossing the configured threshold, naming the bus, the stop and the remaining minutes.<br>**Fail:** No notification is delivered, duplicates are sent for one subscription, or a notification arrives after the bus has departed. | Removes the need to keep the app open and watch the map — the main convenience the platform offers to a commuter waiting at a stop. |
| **FR-005** | Functional | The system shall present the Fleet Controller with a dashboard of all active buses, automatically flag any bus delayed beyond a configurable threshold (default 10 minutes) or holding a *Full* crowding band, and allow the controller to dispatch a relief bus onto the affected route. | High | **Pass:** A bus breaching either threshold is shown as flagged within one dashboard refresh cycle; dispatching a relief bus creates an assignment record and the relief bus appears as active on that route.<br>**Fail:** A breaching bus is not flagged, or a dispatch action completes without creating an assignment record. | Turns passive monitoring into operational control. The platform is "transit intelligence" only if the operator can act on what it detects. |

---

## 2. Non-Functional Requirements

| Req ID | Type | Description | Priority | Acceptance Criteria | Rationale |
|---|---|---|---|---|---|
| **NFR-001** | Nonfunctional — Performance & Scalability | The tracking engine shall handle telemetry streams from up to 1,000 active transit vehicles simultaneously and complete a full ETA recomputation cycle across the fleet with a 95th-percentile latency under 2 seconds. | High | **Pass:** A 30-minute benchmark at 1,000 simulated vehicles sustains p95 ETA-refresh latency below 2 seconds with packet loss under 0.1%.<br>**Fail:** p95 latency reaches 2 seconds or more, or packet loss exceeds 0.1% under the same simulated peak load. | A mid-size city fleet is on the order of a thousand vehicles. If the pipeline cannot keep pace at peak hour, ETAs go stale and FR-001 and FR-003 fail in practice even though their logic is correct. |
| **NFR-002** | Nonfunctional — Security & Privacy | All client–server and telemetry traffic shall use TLS 1.3; Fleet Controller functions shall be gated behind role-based access control; commuter location data used for nearest-stop lookup shall be purged within 24 hours and never linked to a persistent identifier. | High | **Pass:** A TLS scan finds no plaintext or down-level endpoint; a Commuter-role token is rejected with HTTP 403 on every controller endpoint; an audit log shows the purge job removing all location records older than 24 hours.<br>**Fail:** Any endpoint accepts plaintext, a Commuter-role token reaches a controller function, or location records survive beyond 24 hours. | Dispatch controls are safety-relevant and must never be publicly actionable, and commuter location traces are personal data subject to India's DPDP Act, 2023. |

---

## 3. Traceability Summary

| Requirement | Realised by Use Case(s) |
|---|---|
| FR-001 | UC-09 Ingest GPS Telemetry, UC-07 Compute ETA |
| FR-002 | UC-03 View Crowding Level, UC-08 Estimate Crowding Level |
| FR-003 | UC-01 Search Route / Stop, UC-02 View Live Bus Location & ETA |
| FR-004 | UC-04 Subscribe to Arrival Alert |
| FR-005 | UC-05 Monitor Fleet Dashboard, UC-06 Dispatch Relief Bus |
| NFR-001 | Constrains UC-09 Ingest GPS Telemetry and UC-07 Compute ETA |
| NFR-002 | Constrains UC-10 Authenticate Controller and all data paths |
