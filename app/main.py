from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .config import get_settings
from .database import Base, engine, get_db
from .routers import auth

settings = get_settings()

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)


@app.get("/", response_model=schemas.UserRead | None)
def read_root(db: Session = Depends(get_db)):
    """Simple health endpoint that returns the first user if available."""

    return db.query(models.User).first()
