from .models import SessionLocal


def get_db():
    """
    Dependency function that provides a database session to FastAPI routes.
    Ensures DB session is opened before request and properly closed after.
    """
    db = SessionLocal()
    try:
        yield db  # give db session to the route
    finally:
        db.close()  # close after request finishes
