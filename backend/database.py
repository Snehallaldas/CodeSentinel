from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///scansy.db")
Session = sessionmaker(bind=engine)

class Scan(Base):
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String)
    total_findings = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    result = Column(String)
Base.metadata.create_all(engine)

def save_scan(language, total_findings, results):
    session = Session()
    scan = Scan(
        language=language,
        total_findings=total_findings,
        result=results
    )
    session.add(scan)
    session.commit()
    session.close()

def get_all_scans():
    session = Session()
    scans = session.query(Scan).order_by(Scan.created_at.desc()).all()
    session.close()
    return scans