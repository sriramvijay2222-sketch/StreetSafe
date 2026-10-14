import argparse
from app.database import Base, SessionLocal, engine
from app.models import Report
from app.services import priority

samples = [
 ("open drain", "Fictional uncovered drain near Lakshmipuram", "Synthetic example only; not a verified public hazard.", "high", 16.3067, 80.4365),
 ("flooding", "Fictional waterlogging near Brodipet", "Synthetic example only; not a verified public hazard.", "medium", 16.3054, 80.4418),
 ("broken streetlight", "Fictional streetlight outage", "Synthetic example only; not a verified public hazard.", "low", 16.2991, 80.4429),
]
parser = argparse.ArgumentParser(description="Seed clearly labelled fictional StreetSafe reports.")
parser.add_argument("--reset-demo", action="store_true", help="Remove only existing fictional demo reports before seeding.")
args = parser.parse_args()
Base.metadata.create_all(engine); db = SessionLocal()
try:
    existing = db.query(Report).filter(Report.is_demo == True)
    if args.reset_demo:
        existing.delete(synchronize_session=False); db.commit(); print("Removed existing fictional demo reports; genuine reports were preserved.")
    if db.query(Report).filter(Report.is_demo == True).first(): print("Demo reports already exist; no changes made.")
    else:
        for i, (c,t,d,s,lat,lon) in enumerate(samples, 1):
            score,label,_,_ = priority(c,s)
            db.add(Report(incident_id=f"DEMO-GNT-{i:03d}", category=c,title=t,description=d,severity=s,latitude=lat,longitude=lon,priority_score=score,priority_label=label,is_demo=True))
        db.commit(); print("Seeded 3 clearly-labelled fictional demo reports.")
finally: db.close()
