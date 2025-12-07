from sqlalchemy.orm import Session
from . import models


def create_event(db: Session, payload: dict):
    """
    Store or handle incoming event from inference pipeline.
    Currently only prints, but later can log to DB.
    """
    print("EVENT:", payload)
    # TODO: Save event to DB if required in future
    return payload


def create_student(db: Session, payload):
    """
    Create a new student record using validated Pydantic schema `EnrollIn`.
    """
    student = models.Student(
        reg_no=payload.reg_no,
        name=payload.name,
        phone_number=payload.phone_number
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    # returning a simple dict makes fastapi auto-convert to JSON
    return {
        "id": student.id,
        "reg_no": student.reg_no,
        "name": student.name
    }
