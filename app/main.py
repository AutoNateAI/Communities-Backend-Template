from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import models, schemas
from .config import get_settings
from .database import Base, engine, get_db
from .routers import auth

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(auth.router)


@app.get("/", response_model=schemas.UserRead | None)
def read_root(db: Session = Depends(get_db)):
    """Simple health endpoint that returns the first user if available."""

    return db.query(models.User).first()
