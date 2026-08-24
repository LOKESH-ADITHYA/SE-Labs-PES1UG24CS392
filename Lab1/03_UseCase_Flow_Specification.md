# Lab 1 — Use-Case Flow Specification

**Problem Statement #24 — Public Bus Live Tracking & Crowding Estimator**
**SRN:** PES1UG24CS392

---

| Field | Value |
|---|---|
| **Use Case ID** | UC-02 |
| **Use Case Name** | View Live Bus Location & ETA |
| **Primary Actor** | Commuter |
| **Secondary Actors** | Onboard GPS Unit, Ticketing / APC Sensor |
| **Related Requirements** | FR-001, FR-002, FR-003 (constrained by NFR-001) |
| **Included Use Cases** | Compute ETA, View Crowding Level |
| **Extending Use Case** | Subscribe to Arrival Alert («extend») |
| **Trigger** | The Commuter selects a route or a stop and requests live arrival information. |
| **Priority** | High |

---

## 1. Preconditions

1. The Commuter has the application open and the device has network connectivity.
2. At least one bus is in active service on the selected route, and its Onboard GPS Unit has reported a position within the last 15 seconds.
3. The route's stop sequence, timetable and rated vehicle capacity are loaded in the system's reference data.
4. The Ticketing / APC Sensor feed for the active buses is available to the crowding estimator.

## 2. Postconditions

**Success guarantee**

1. The Commuter is shown each approaching bus with its live map position, its ETA at the selected stop, and its crowding band (*Seats Available* / *Standing Room* / *Full*).
2. The displayed view continues to refresh at the 5-second telemetry cadence for as long as it stays open.
3. The query is written to the usage log; any coarse commuter location used for nearest-stop lookup is held only for the 24-hour retention window (NFR-002).

**Minimal guarantee (on failure)**

4. The Commuter is told explicitly that live data is unavailable and is shown the scheduled timetable instead; no ETA is presented as if it were live.

---

## 3. Main Success Scenario

| Step | Actor | Action |
|---|---|---|
| 1 | Commuter | Enters a route number or selects a stop from the map / nearby-stops list. |
| 2 | System | Validates the input against the reference route and stop data. |
| 3 | System | Retrieves every bus currently in service whose remaining path includes the selected stop. |
| 4 | System | **«include» Compute ETA** — for each such bus, uses the latest GPS fix, remaining route distance and current traffic speed to compute the arrival time at the selected stop. |
| 5 | System | **«include» View Crowding Level** — for each such bus, derives occupancy from the ticketing / APC sensor counts and maps it to a crowding band. |
| 6 | System | Renders the result: each bus is drawn at its live position on the map and listed with its ETA in minutes and a colour-coded crowding badge, sorted by soonest arrival. |
| 7 | Commuter | Reviews the list and selects a bus to see its stop-by-stop progress. |
| 8 | System | Continues to refresh position, ETA and crowding band every 5 seconds as new telemetry arrives, until the Commuter leaves the view. |

> *Extension point (after step 6):* the Commuter may invoke **Subscribe to Arrival Alert** («extend», UC-04) on any listed bus. This is optional; the main flow completes without it.

---

## 4. Alternate Flow

### 4A — GPS telemetry is stale or unavailable for a bus

*Branches at step 4 of the main success scenario.*

| Step | Actor | Action |
|---|---|---|
| 4A.1 | System | Detects that the most recent GPS fix for a bus is older than 15 seconds (dropped signal, tunnel, or onboard unit fault). |
| 4A.2 | System | Suppresses the live ETA for that bus rather than extrapolating from the stale fix. |
| 4A.3 | System | Substitutes the **scheduled** arrival time from the timetable and marks the entry clearly as *"Scheduled — live tracking unavailable"*, with the bus icon greyed out at its last known position and the age of that fix shown. |
| 4A.4 | System | Raises a *telemetry gap* event on the Fleet Controller dashboard so the fault can be investigated (feeds FR-005). |
| 4A.5 | System | Continues polling; when a fresh GPS fix arrives, the entry reverts to a live ETA on the next refresh cycle and the flow rejoins the main scenario at step 6. |

**Outcome:** the Commuter still receives usable arrival guidance and is never misled into treating a scheduled time as a live prediction.

---

## 5. Business Rules & Constraints

| Ref | Rule |
|---|---|
| BR-01 | A GPS fix older than 15 seconds is *stale* and must not be used to present a live ETA. |
| BR-02 | Crowding bands: *Seats Available* < 50%, *Standing Room* 50–85%, *Full* > 85% of the vehicle's rated capacity. |
| BR-03 | The full ETA recomputation cycle must complete with a p95 latency under 2 seconds at a fleet size of 1,000 vehicles (NFR-001). |
| BR-04 | Any commuter location captured for nearest-stop lookup is purged within 24 hours and is never linked to a persistent identifier (NFR-002). |
