from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import schemas
from app.models import models
from app.services.auth_service import AuthService
from app.services.log_service import LogService
from app.core.auth_config import auth
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response

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


@router.post("/login", response_model=schemas.TokenOut)
def login(
    form_data: schemas.UserLogin,
    request:Request,
    response: Response,
    db: Session = Depends(get_db)
):
    tokens = AuthService.login(db, form_data.email, form_data.password, request)

    user = db.query(models.User).filter(models.User.email == form_data.email).first()

    LogService.log_action(
        db = db,
        user_id = user.user_id if user else None,
        user_email = form_data.email,
        action_type = "LOGIN",
        details = {"email": form_data.email},
        ip_address = request.client.host
    )

    return tokens

@router.post("/refresh", response_model=schemas.RefreshTokenOut)
def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):  
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Refresh token missing"
        )
    
    tokens = AuthService.refresh_token(db, refresh_token)
    auth.set_access_cookies(tokens["access_token"], response)
    
    return tokens

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        AuthService.logout(db, refresh_token)
    
    auth.unset_access_cookies(response)
    auth.unset_refresh_cookies(response)
    
    return {"message": "Logged out successfully"}