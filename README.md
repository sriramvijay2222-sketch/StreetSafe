# StreetSafe

StreetSafe is a local civic-tech prototype for reporting public-space hazards and following a preliminary workflow:

> **Report → Assess → Review → Track → Verify resolution**

It provides a shared map and incident view for citizens and a protected reviewer workflow. It is **not** connected to Guntur Municipal Corporation, any other municipal authority, emergency dispatch, or maintenance team. It must not be used to report an immediate emergency.

## Contents

- [Problem background](#problem-background)
- [Real-world problem analysis](#real-world-problem-analysis)
- [Existing solutions and comparison](#existing-solutions-and-comparison)
- [Research gap and opportunity](#research-gap-and-opportunity)
- [Why StreetSafe](#why-streetsafe)
- [Problem statement and scope](#problem-statement-and-scope)
- [How StreetSafe addresses the problem](#how-streetsafe-addresses-the-problem)
- [Technical implementation](#technical-implementation)
- [Run locally](#run-locally)
- [Evaluation plan](#evaluation-plan)
- [Limitations and future work](#limitations-and-future-work)
- [References](#references)

## Problem background

Open drains, waterlogging, exposed electrical wires, broken streetlights, and unsafe crossings can create safety and accessibility risks in public space. Their severity depends on location, exposure, weather, maintenance conditions, and the people using the space; StreetSafe makes no claim that a report is verified or that its score is a probability of harm.

Road safety provides a relevant, though broader, public-safety context. WHO's 2023 India country profile reports **153,972 road-traffic fatalities recorded in 2021** and a WHO estimate of **216,618** for the same year. This does not attribute crashes to any particular StreetSafe hazard category, but it supports treating safer public roads and crossings as an important public concern. [WHO India road-safety profile (2023 data)](https://cdn.who.int/media/docs/default-source/country-profiles/road-safety/road-safety-2023-ind.pdf?download=true&sfvrsn=b4fb5a5c_3)

Flooding and waterlogging also benefit from timely, intelligible local information. UNDRR's 2024 global assessment emphasizes that risk knowledge, clear communication, preparedness, and coordination are needed for action; it is an early-warning report, not evidence that StreetSafe is an early-warning system. [UNDRR, *Global Status of Multi-Hazard Early Warning Systems 2024*](https://www.undrr.org/reports/global-status-MHEWS-2024)

Digital service delivery can help people find and track public services, but local delivery remains uneven. The UN's 2024 survey reports continued progress in digital government while identifying persistent differences between national and local e-government performance. [UN DESA, *E-Government Survey 2024*](https://desapublications.un.org/publications/un-e-government-survey-2024)

StreetSafe is centred on a map around Guntur for demonstration. This repository does **not** establish the prevalence of these hazards in Guntur or the performance of any local grievance system.

## Real-world problem analysis

| Challenge | Likely root cause and affected users | Consequence StreetSafe is designed to explore | Evidence and boundary |
|---|---|---|---|
| Reports are scattered or hard to follow | Different agencies, channels, and local processes can separate the report, reviewer, and status information. Residents, pedestrians, cyclists, older people, and maintenance staff may need different views. | A shared incident list and map can make a prototype report record easier to find and discuss. | CPGRAMS demonstrates that central lodging, routing, status tracking, feedback, and appeal are feasible in government systems; it does not prove that every city has the same workflow. [CPGRAMS](https://pgportal.gov.in/) |
| Multiple people report the same visible issue | A recurring, location-specific problem can be observed by several people independently. | Same-category reports within about 150 m are presented as **possible** duplicates for human comparison. | This is a design rule in StreetSafe, not an independently validated duplicate-detection model. |
| Attention must be allocated | Reviewers may need an understandable way to examine different categories and reported severities. | A transparent preliminary score provides a review queue, not an automated decision. | UNDRR identifies risk knowledge and governance as important to preparedness, but does not validate this repository's scoring formula. [UNDRR (2024)](https://www.undrr.org/reports/global-status-MHEWS-2024) |
| A report needs verification and accountable follow-up | Citizen submissions can be incomplete, mistaken, stale, false, or malicious; resolving a physical hazard usually requires an institution with authority and resources. | A reviewer can inspect a report, record a note, change status, and leave a timestamped history. | StreetSafe has no field-verification integration or municipal work-order connection. |
| Communities need accurate information | A public map can be useful only when data are current, understandable, and handled responsibly. | The app separates fictional demo reports from submissions and displays status. | Accuracy, adoption, access, privacy, and accessibility require testing with real users and authorities. The UN survey recommends local evaluation rather than assuming digital availability equals effective use. [UN DESA (2024)](https://desapublications.un.org/publications/un-e-government-survey-2024) |

## Existing solutions and comparison

| Existing system | Main purpose | Relevant capabilities | Documented limitations or gaps | Source |
|---|---|---|---|---|
| CPGRAMS (Government of India) | Central public-grievance lodging and redressal for public authorities | 24×7 lodging, a registration ID, status tracking, reminders, clarification, feedback, appeal, role-based government access, and routing across participating ministries/states | It excludes specified matters (for example RTI, court-related/sub judice, and religious matters). Whether it provides StreetSafe's map view, 150 m duplicate suggestions, or this scoring method is **unverified here**. | [CPGRAMS portal](https://pgportal.gov.in/), [CPGRAMS help material](https://pgportal.gov.in/CPGOFFICE/Documents/CPGRAMS-Help.pdf) |
| Swachhata App / Swachh Bharat Mission (Urban) | Citizen cleanliness-related grievance redressal under SBM (Urban) | Official SBM guidance says the app facilitates redressal of cleanliness-related citizen grievances; MoHUA material describes it as a one-stop grievance-redressal platform | Its documented focus is cleanliness-related grievances. Coverage of every StreetSafe category, jurisdiction, duplicate method, or priority formula is **not established by the cited documents**. | [SBM (Urban) guidelines](https://swachhbharaturban.gov.in/writereaddata/SBM_Guideline.pdf), [MoHUA material](https://mohua.gov.in/upload/uploadfiles/files/2688HUA-ENGLISH-19-4-2023.pdf) |
| Open311 GeoReport v2 | Open civic-service request standard | Location-based non-emergency issue reporting, service definitions, request creation, request retrieval, and status-oriented workflows | It is a standard, not a deployed municipal service by itself. Adoption and available service types depend on the jurisdiction. | [Open311 GeoReport v2](https://wiki.open311.org/GeoReport_v2/) |
| Emergency and disaster-warning systems | Warning dissemination and preparedness for hazards and disasters | Risk knowledge, monitoring/forecasting, warning communication, and response preparedness | StreetSafe is not an emergency-call centre, forecast service, or warning system. It must not be substituted for those services. | [UNDRR (2024)](https://www.undrr.org/reports/global-status-MHEWS-2024) |

## Research gap and opportunity

StreetSafe does not claim that maps, tracking, duplicate handling, or civic issue reporting are globally new. Open311 and government grievance systems show that many of these functions already exist.

Its potential contribution is a single, inspectable prototype that combines a map-oriented public incident view, transparent preliminary scoring, deterministic duplicate suggestions, reviewer action, and status history. This is best described as an **integration and evaluation opportunity**, not proof of a missing technology.

- **Existing capability:** CPGRAMS already documents lodging and tracking; Open311 defines a standard location-based request model.
- **Partially addressed need:** A local implementation may need a workflow tailored to a defined service area, categories, responsible teams, languages, and accessibility requirements.
- **Implementation and coordination problem:** Effective handling requires verified routing, staff capacity, budgets, field verification, and public accountability—not just a user interface.
- **Proposed improvement requiring validation:** Whether this combined view improves duplicate review, prioritization, understanding, or resolution outcomes must be tested with a community and authorized public-service partners.

## Why StreetSafe

StreetSafe was selected as a student-built project because it has clear public-safety relevance, an understandable reporting problem, and a complete demonstrable workflow without expensive hardware or paid APIs. It also supports objective technical evaluation: API validation, map/data consistency, duplicate-suggestion precision, reviewer history integrity, and usability testing can all be measured.

Building the prototype does **not** establish that it reduces accidents, improves municipal performance, or solves a verified problem in Guntur. Those claims would require field data, community participation, institutional cooperation, and independent evaluation.

## Problem statement and scope

> Citizens encounter hazardous public-space conditions, but information about these hazards may be scattered, duplicated, difficult to verify, or difficult to track through to resolution. StreetSafe provides a shared interface for reporting hazards, visualizing their locations, assigning preliminary priorities, identifying potentially duplicated reports, and tracking administrative action.

**Target users:** community members reporting non-emergency hazards; prototype reviewers assessing submissions; and, only in a future integrated deployment, authorized maintenance or municipal teams.

**Scope and assumptions:** a reporter enters a category, text description, severity, and coordinates; a reviewer uses the data to make a human status decision. The app assumes the report may be inaccurate and marks demo records explicitly.

**Out of scope:** emergency dispatch, automatic hazard verification, municipal work-order assignment, automated rejection/merging, guaranteed resolution, accounts, production-grade privacy controls, and claims of scientific risk prediction.

## How StreetSafe addresses the problem

1. **Report** — citizens submit one of six implemented categories: open drain, flooding, exposed electrical wire, broken streetlight, unsafe crossing, or other. The form validates title, description, latitude, longitude, and reported severity; map clicks set the coordinates.
2. **Assess** — the backend assigns a deterministic preliminary score and label. This is illustrative triage only and never automatically rejects a report or dispatches an emergency response.
3. **Review** — a reviewer supplies the backend-held administrator key, sees reports sorted by score, searches or filters them, examines detailed possible duplicates, and may add a note.
4. **Track** — the reviewer changes a report to `submitted`, `under review`, `in progress`, `resolved`, or `rejected`; the API stores prior status, new status, note, and timestamp.
5. **Verify resolution** — StreetSafe records a reviewer-selected `resolved` status but does not independently verify the physical outcome. Field verification and evidence capture are future work.

### Preliminary-priority rule

The backend is authoritative. It calculates:

`priority_score = min(100, category_weight + severity_points)`

| Category | Weight |
|---|---:|
| Exposed electrical wire | 60 |
| Open drain | 40 |
| Flooding | 35 |
| Unsafe crossing | 35 |
| Broken streetlight | 20 |
| Other | 10 |

Severity contributes **10** (low), **25** (medium), or **40** (high). Scores below 40 are `low`; 40–69 are `medium`; 70–100 are `high`. Incident details show the category contribution, severity contribution, score, and label.

### Duplicate suggestions

The backend uses the Haversine distance formula. It suggests another report only when it has the same category, is not the report itself, and is within approximately **150 metres**. It exposes each candidate's ID, category, coordinates, and status to the reviewer. Suggestions are informational: StreetSafe never automatically deletes, merges, or rejects reports. If there are no candidates, the reviewer sees an explicit message.

## Technical implementation

```text
React + Vite + React-Leaflet browser client
        │  HTTP (VITE_API_BASE_URL, default http://localhost:8000)
        ▼
FastAPI application
        │  SQLAlchemy sessions
        ▼
SQLite database (backend/streetsafe.db)
```

| Area | Implemented technology and behaviour |
|---|---|
| Frontend | React 18, Vite, TypeScript, React-Leaflet/Leaflet, Lucide icons, responsive CSS |
| Backend | FastAPI with Pydantic validation and SQLAlchemy ORM |
| Persistence | SQLite by default; `STREETSAFE_DATABASE_URL` can override the connection for isolated tests/deployments |
| Map | OpenStreetMap tiles through React-Leaflet; default centre is Guntur for demonstration |
| Data | `Report` records a UUID-based incident ID, category, text, severity, score/label, coordinates, status, demo flag, and timestamp; `StatusHistory` records changes |
| Reviewer access | The backend compares the `X-Admin-Key` header to `ADMIN_API_KEY`; the key is held only in browser memory and never returned by the API |

### API endpoints

| Method | Endpoint | Purpose | Protection |
|---|---|---|---|
| `GET` | `/api/health` | Health check | Public |
| `GET` | `/api/reports` | List reports; optional `category`, `priority_label`, and `status_filter` query filters | Public |
| `GET` | `/api/reports/{report_id}` | Retrieve one report | Public |
| `POST` | `/api/reports` | Create a validated report and preliminary assessment | Public |
| `PATCH` | `/api/reports/{report_id}/status` | Change status and write history | `X-Admin-Key` required |
| `GET` | `/api/reports/{report_id}/history` | Read reviewer status history | `X-Admin-Key` required |
| `GET` | `/api/stats` | Return persisted totals, open reports, high-priority reports, and resolved reports | Public |

**Statistics:** “open” includes `submitted`, `under review`, and `in progress`; it excludes `resolved` and `rejected`. Dashboard values come from `/api/stats`, not hard-coded frontend values.

## Run locally

Open two PowerShell windows in this project directory.

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:ADMIN_API_KEY = "choose-a-local-admin-key"
uvicorn app.main:app --reload --port 8000
```

```powershell
cd frontend
npm install
npm run dev
```

Visit the frontend at http://localhost:5173 and API documentation at http://localhost:8000/docs.

The reviewer area requires the same `ADMIN_API_KEY` value entered when starting the backend. It is a local demo guard, not account authentication.

### Fictional demo data

The optional seed command creates clearly labelled fictional Guntur-area examples only when demo data is absent:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python seed.py
```

To replace only demo records while preserving genuine submissions:

```powershell
python seed.py --reset-demo
```

### Tests and build

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest

cd ..\frontend
npm run build
```

The API tests configure an isolated temporary SQLite database, so they do not intentionally insert test reports into the normal local database.

## Evaluation plan

The following are **proposed metrics**, not measured results:

| Measure | Example method |
|---|---|
| Report-submission success | Percentage of valid submissions saved and displayed correctly |
| Map accuracy | Compare stored coordinates and incident metadata with rendered marker/details |
| Verification time | Measure time from creation to a reviewer’s documented decision in a controlled study |
| Duplicate precision | Have reviewers label suggested pairs as same incident/not same incident; calculate precision and recall where feasible |
| Priority agreement | Compare the rule-based label with independent reviewer judgments using a pre-defined rubric |
| Status-update reliability | Audit whether authorized changes create correct, ordered history records |
| Documented outcomes | Percentage of reports with a status and evidence-defined outcome over a selected period |
| Resolution time | Measure only after real, reliable assignment and completion data are available |

No outcome study has been conducted for this repository. In particular, it does not demonstrate fewer accidents, faster municipal resolution, or improved public safety.

## Limitations and future work

- No municipal, emergency-service, work-order, dispatch, or field-verification integration exists.
- Reports depend on accurate, non-malicious citizen input; moderation, abuse prevention, and evidence workflows are not implemented.
- The score is explainable but rule-based, not a validated danger or accident-probability model.
- The 150 m same-category rule can produce false positives and false negatives.
- A `resolved` status is an administrative record, not proof of physical remediation.
- The API-key guard is not production authentication. A real deployment needs accounts, role-based authorization, HTTPS, rate limiting, audit protections, secret management, privacy/data-retention policy, accessibility testing, and security review.
- SQLite, unpaginated lists, and public report data are suitable for a local MVP, not necessarily a scaled public service.
- Validation with actual residents, municipal staff, and responsible authorities is still needed; such work requires consent, institutional cooperation, and independent evaluation.

## References

1. World Health Organization. **Global status report on road safety 2023: India country profile**. 2024 publication; 2021 fatality data. https://cdn.who.int/media/docs/default-source/country-profiles/road-safety/road-safety-2023-ind.pdf?download=true&sfvrsn=b4fb5a5c_3 — road-safety context.
2. World Health Organization. **Global status report on road safety 2023**. 2023. https://www.who.int/publications/b/72400 — global road-safety methodology and context.
3. United Nations Office for Disaster Risk Reduction. **Global Status of Multi-Hazard Early Warning Systems 2024**. 2024. https://www.undrr.org/reports/global-status-MHEWS-2024 — risk knowledge, communication, preparedness, and coordination context.
4. United Nations Department of Economic and Social Affairs. **UN E-Government Survey 2024**. September 2024. https://desapublications.un.org/publications/un-e-government-survey-2024 — local digital-government context and evaluation considerations.
5. Government of India, Department of Administrative Reforms and Public Grievances. **CPGRAMS**. Accessed 2026-10-14. https://pgportal.gov.in/ — documented national grievance lodging, routing, tracking, feedback, and appeal features.
6. Government of India, Ministry of Housing and Urban Affairs / Swachh Bharat Mission (Urban). **SBM Guidelines**. Accessed 2026-10-14. https://swachhbharaturban.gov.in/writereaddata/SBM_Guideline.pdf — Swachhata mobile application's cleanliness-grievance purpose.
7. Open311. **GeoReport v2**. Accessed 2026-10-14. https://wiki.open311.org/GeoReport_v2/ — location-based non-emergency civic service-request standard.
