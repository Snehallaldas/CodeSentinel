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

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def create_user(username, email, hashed_password):
    session = Session()
    user = User(username=username, email=email, password=hashed_password)
    session.add(user)
    session.commit()
    session.close()

def get_user_by_email(email):
    session = Session()
    user = session.query(User).filter(User.email == email).first()
    session.close()
    return user

Base.metadata.create_all(engine)