from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
import os


# -------------------------------------------------------------------
# DATABASE INITIALIZATION
# -------------------------------------------------------------------

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./smart_attendance.db")

# If using SQLite, need check_same_thread=False
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


# -------------------------------------------------------------------
# DATABASE MODELS (TABLE SCHEMAS)
# -------------------------------------------------------------------

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    reg_no = Column(String, unique=True, index=True)   # registration number
    name = Column(String)
    phone_number = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)                       # links to students.id
    vector = Column(LargeBinary)                       # Face embedding saved as bytes
    model_version = Column(String, default="v1")       # Which model generated embedding


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)                       # links to students.id
    date = Column(String)                              # "2025-12-05"
    first_seen = Column(DateTime)                      # first webcam detection
    last_seen = Column(DateTime)                       # last seen within same session
    status = Column(String)                            # "Present" / "Absent" / etc.


class BehaviorLog(Base):
    __tablename__ = "behavior_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer)                       # links to students.id
    track_id = Column(String)                          # YOLO track ID
    behavior_type = Column(String)                     # e.g., "phone usage", "drowsiness"
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    confidence = Column(Float)                         # ML confidence score


# -------------------------------------------------------------------
# CREATE ALL TABLES IF NOT EXIST
# -------------------------------------------------------------------
Base.metadata.create_all(bind=engine)
