# StreetSafe

StreetSafe is a local civic-tech MVP for reporting public hazards and tracking a preliminary workflow: **report → assess → review → resolve**. It is not connected to municipal authorities or emergency services.

## Run locally (Windows PowerShell)

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

Optional fictional sample reports around Guntur may be added once, without affecting user reports:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python seed.py
```

## Tests and build

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pytest

cd ..\frontend
npm run build
```

## Safety and security notes

Priority is a deterministic preliminary assessment: category weight plus reported severity, capped at 100. It is not a scientifically validated danger probability and requires reviewer judgement. Duplicate suggestions use same-category reports within about 150 metres; they do not delete, merge, or reject reports.

The reviewer key is read only by the backend from `ADMIN_API_KEY`, supplied via the `X-Admin-Key` header, and held only in browser memory. It is a hackathon guard, not production authentication. Real deployment needs account authentication, authorization, HTTPS, rate limiting, audit protections, and security review.

