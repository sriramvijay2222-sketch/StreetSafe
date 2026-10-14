import os
import secrets
from datetime import datetime, timezone
from uuid import uuid4
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Report, StatusHistory
from .schemas import DuplicateOut, HistoryOut, ReportCreate, ReportOut, StatsOut, StatusUpdate
from .services import duplicate_reports, priority

Base.metadata.create_all(bind=engine)
app = FastAPI(title="StreetSafe API", version="0.1.0")
cors_origins = ["http://localhost:5173"]
if configured_origins := os.getenv("CORS_ALLOW_ORIGINS"):
    cors_origins.extend(origin.strip() for origin in configured_origins.split(",") if origin.strip())
app.add_middleware(CORSMiddleware, allow_origins=cors_origins, allow_credentials=False, allow_methods=["GET", "POST", "PATCH"], allow_headers=["Content-Type", "X-Admin-Key"])

def serialize(report: Report, all_reports: list[Report]) -> ReportOut:
    data = {c.name: getattr(report, c.name) for c in report.__table__.columns if c.name != "id"}
    _, _, category_weight, severity_points = priority(report.category, report.severity)
    duplicates = duplicate_reports(report, all_reports)
    data["category_weight"] = category_weight
    data["severity_points"] = severity_points
    data["possible_duplicate_ids"] = [item.incident_id for item in duplicates]
    data["possible_duplicates"] = [DuplicateOut(incident_id=item.incident_id, category=item.category, latitude=item.latitude, longitude=item.longitude, status=item.status) for item in duplicates]
    return ReportOut(**data)

def report_or_404(report_id: str, db: Session):
    report = db.query(Report).filter(Report.incident_id == report_id).first()
    if not report: raise HTTPException(404, "Report not found")
    return report

def require_admin(x_admin_key: str | None = Header(default=None)):
    expected = os.getenv("ADMIN_API_KEY")
    if not expected or not x_admin_key or not secrets.compare_digest(x_admin_key, expected):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="A valid administrator key is required")

@app.get("/api/health")
def health(): return {"status": "ok"}

@app.get("/api/reports", response_model=list[ReportOut])
def reports(category: str | None = None, priority_label: str | None = None, status_filter: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Report)
    if category: q = q.filter(Report.category == category)
    if priority_label: q = q.filter(Report.priority_label == priority_label)
    if status_filter: q = q.filter(Report.status == status_filter)
    all_reports = db.query(Report).all()
    return [serialize(r, all_reports) for r in q.order_by(Report.created_at.desc()).all()]

@app.get("/api/reports/{report_id}", response_model=ReportOut)
def get_report(report_id: str, db: Session = Depends(get_db)):
    return serialize(report_or_404(report_id, db), db.query(Report).all())

@app.post("/api/reports", response_model=ReportOut, status_code=201)
def create_report(payload: ReportCreate, db: Session = Depends(get_db)):
    score, label, _, _ = priority(payload.category, payload.severity)
    r = Report(incident_id=f"SS-{uuid4()}", **payload.model_dump(), priority_score=score, priority_label=label, created_at=datetime.now(timezone.utc))
    db.add(r); db.commit(); db.refresh(r)
    return serialize(r, db.query(Report).all())

@app.patch("/api/reports/{report_id}/status", response_model=ReportOut, dependencies=[Depends(require_admin)])
def update_status(report_id: str, payload: StatusUpdate, db: Session = Depends(get_db)):
    r = report_or_404(report_id, db)
    previous = r.status
    if previous == payload.status:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This report already has that status")
    r.status = payload.status
    db.add(StatusHistory(report_id=r.id, previous_status=previous, new_status=payload.status, note=payload.note))
    db.commit(); db.refresh(r)
    return serialize(r, db.query(Report).all())

@app.get("/api/reports/{report_id}/history", response_model=list[HistoryOut], dependencies=[Depends(require_admin)])
def history(report_id: str, db: Session = Depends(get_db)):
    r = report_or_404(report_id, db)
    return db.query(StatusHistory).filter(StatusHistory.report_id == r.id).order_by(StatusHistory.changed_at.desc()).all()

@app.get("/api/stats", response_model=StatsOut)
def stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Report.id)).scalar() or 0
    return {"total": total, "open": db.query(Report).filter(Report.status.notin_(["resolved", "rejected"])).count(), "high_priority": db.query(Report).filter(Report.priority_label == "high").count(), "resolved": db.query(Report).filter(Report.status == "resolved").count()}
