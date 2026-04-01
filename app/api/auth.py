from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import schemas
from app.models import models
from app.services.auth_service import AuthService
from app.services.log_service import LogService
from fastapi import APIRouter, Depends, HTTPException, status, Request

router =  APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=schemas.UserOut)
def register(
    user_data: schemas.UserCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    user = AuthService.register(db, user_data)

    LogService.log_action(
        db = db,
        user_id = user.user_id,
        user_email = user.email,
        action_type = "USER_REGISTRATION",
        details = {"email": user.email},
        ip_address = request.client.host
    )

    return user


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: schemas.UserLogin,
    request:Request,
    db: Session = Depends(get_db)
):
    result = AuthService.login(db, form_data.email, form_data.password)
    user = db.query(models.User).filter(models.User.email == form_data.email).first()

    LogService.log_action(
        db = db,
        user_id = user.user_id if user else None,
        user_email = form_data.email,
        action_type = "LOGIN",
        details = {"email": form_data.email},
        ip_address = request.client.host
    )

    return result
