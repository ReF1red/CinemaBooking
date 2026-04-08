from sqlalchemy.orm import Session
from app.schemas import schemas
from app.core.auth_config import auth
from fastapi import HTTPException, status, Request
from app.models import models
from app.core.security import get_password_hash, verify_password
from datetime import datetime, timedelta
import hashlib
import os

class AuthService:
    @staticmethod
    def register(db: Session, user_data: schemas.UserCreate):
        existing = db.query(models.User).filter(models.User.email == user_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
                )
        password_hash = get_password_hash(user_data.password)

        new_user = models.User(
            email = user_data.email,
            password_hash = password_hash,
            full_name = user_data.full_name,
            role = "client",
            is_active = True 
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    
    @staticmethod
    def login(db: Session, email: str, password: str, request: Request):
        user = db.query(models.User).filter(models.User.email == email).first()

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is blocked",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        access_token = auth.create_access_token(uid=str(user.user_id))
        refresh_token = auth.create_refresh_token(uid=str(user.user_id))

        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()

        refresh_token_record = models.RefreshToken(
            user_id=user.user_id,
            token_hash=token_hash,
            expires_at=datetime.utcnow() + timedelta(days=7),
            is_revoked=False
        )
        db.add(refresh_token_record)
        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    @staticmethod
    def refresh_token(db: Session, refresh_token: str):
        try:
            payload = auth._decode_token(refresh_token, "refresh")
            user_id = int(payload.sub)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        record = db.query(models.RefreshToken).filter(
            models.RefreshToken.token_hash == token_hash,
            models.RefreshToken.is_revoked == False,
            models.RefreshToken.expires_at > datetime.utcnow()
        ).first()

        if not record:
            raise HTTPException(status_code=401, detail="Refresh token not found or revoked")

        new_access_token = auth.create_access_token(uid=str(user_id))

        return {"access_token": new_access_token, "token_type": "bearer"}

    @staticmethod
    def logout(db: Session, refresh_token: str):
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        record = db.query(models.RefreshToken).filter(
            models.RefreshToken.token_hash == token_hash
        ).first()

        if record:
            record.is_revoked = True
            db.commit()

        return {"message": "Logged out successfully"}
    