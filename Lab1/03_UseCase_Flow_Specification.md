# Use-Case Flow Specification — UC-02 View Live Bus Location & ETA

**Problem Statement #24 — Public Bus Live Tracking & Crowding Estimator** · SRN: PES1UG24CS392

| Field | Value |
|---|---|
| Use Case | **UC-02 — View Live Bus Location & ETA** |
| Primary Actor | Commuter |
| Secondary Actors | Onboard GPS Unit, Ticketing / APC Sensor |
| Related Requirements | FR-001, FR-002, FR-003 (constrained by NFR-001, NFR-002) |
| Includes | UC-01 Search Route / Stop, UC-07 Compute ETA, UC-03 View Crowding Level |
| Extended by | UC-04 Subscribe to Arrival Alert, at extension point *ETA displayed* |
| Trigger | The Commuter requests live arrival information for a route or stop. |

## Preconditions

1. The Commuter has the application open and the device has network connectivity.
2. At least one bus is in active service on the selected route, and its Onboard GPS Unit has reported a position within the last 15 seconds.
3. Route stop sequence, timetable and rated vehicle capacity are loaded in reference data.

## Postconditions

**Success:** the Commuter is shown each approaching bus with its live map position, ETA at the selected stop and crowding band, refreshing at the 5-second telemetry cadence for as long as the view stays open.

**On failure:** the Commuter is told explicitly that live data is unavailable and is shown the scheduled timetable instead; no ETA is presented as if it were live.

## Main Success Scenario

| # | Actor | Action |
|---|---|---|
| 1 | Commuter | Requests arrival information for a route or stop. |
| 2 | System | **«include» UC-01 Search Route / Stop** — validates the input against reference data and retrieves every in-service bus whose remaining path includes the selected stop. |
| 3 | System | **«include» UC-07 Compute ETA** — for each such bus, computes arrival time at the stop from the latest GPS fix, remaining route distance and current traffic speed. |
| 4 | System | **«include» UC-03 View Crowding Level** — for each such bus, retrieves the crowding band computed from ticketing / APC sensor counts and prepares it for display. |
| 5 | System | Renders each bus at its live position on the map, listed with ETA in minutes and a colour-coded crowding badge, sorted by soonest arrival. *(Extension point: **ETA displayed**.)* |
| 6 | Commuter | Reviews the list and selects a bus to see its stop-by-stop progress. |
| 7 | System | Refreshes position, ETA and crowding band every 5 seconds as new telemetry arrives, until the Commuter leaves the view. |

## Alternate Flow — 5a. GPS telemetry stale or unavailable

*Branches at step 3.*

| # | Action |
|---|---|
| 5a.1 | System detects that the latest GPS fix for a bus is older than 15 seconds (dropped signal, tunnel, or onboard unit fault). |
| 5a.2 | System suppresses the live ETA for that bus rather than extrapolating from the stale fix. |
| 5a.3 | System substitutes the scheduled arrival time from the timetable, marks the entry *"Scheduled — live tracking unavailable"*, and greys out the bus icon at its last known position with the age of that fix shown. |
| 5a.4 | System raises a *telemetry gap* event on the Fleet Controller dashboard for investigation (feeds FR-005). |
| 5a.5 | When a fresh GPS fix arrives, the entry reverts to a live ETA on the next refresh cycle and the flow rejoins the main scenario at step 5. |

**Outcome:** the Commuter still receives usable arrival guidance and is never misled into treating a scheduled time as a live prediction.
