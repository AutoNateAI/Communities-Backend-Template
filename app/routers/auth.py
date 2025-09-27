from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..auth import create_access_token, get_password_hash, verify_password
from ..config import get_settings
from ..database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


@router.post("/signup", response_model=schemas.SignupResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    if db.query(models.Auth).filter(models.Auth.email == user_in.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    if db.query(models.Auth).filter(models.Auth.username == user_in.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    auth_account = models.Auth(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
    )
    user_profile = models.User(
        auth=auth_account,
        email=user_in.email,
        username=user_in.username,
        user_type=user_in.user_type,
    )

    try:
        db.add(auth_account)
        db.add(user_profile)
        db.commit()
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user") from exc

    db.refresh(auth_account)
    db.refresh(user_profile)
    return schemas.SignupResponse(auth=auth_account, user=user_profile)


@router.post("/login", response_model=schemas.Token)
def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    auth_account = db.query(models.Auth).filter(models.Auth.email == form_data.username).first()
    if not auth_account:
        auth_account = db.query(models.Auth).filter(models.Auth.username == form_data.username).first()

    if not auth_account or not verify_password(form_data.password, auth_account.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token = create_access_token(subject=auth_account.email, expires_delta=access_token_expires)
    response.headers["Authorization"] = f"Bearer {token}"
    return schemas.Token(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    """Placeholder logout endpoint."""

    return Response(status_code=status.HTTP_204_NO_CONTENT)
