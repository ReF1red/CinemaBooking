from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.auth_config import auth
from app.database import get_db
from app.models import models

def get_current_user(
    user_id: str = Depends(auth.access_token_required),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.user_id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is blocked"
        )
    
    return user

def get_current_active_user(
    current_user = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_current_admin(
    current_user = Depends(get_current_active_user)
):
    role = current_user.role
    if hasattr(role, 'value'):
        role = role.value
    if role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user