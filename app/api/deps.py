from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.auth_config import auth
from app.database import get_db
from app.models import models, UserRole

def get_user_id_from_token(
    user_id: str = Depends(auth.access_token_required)
):
    return int(user_id)

def get_current_user(
    user_id: int = Depends(get_user_id_from_token),
    db: Session = Depends(get_db)
):
    
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
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
    current_user: models.User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def get_current_admin(
    current_user: models.User = Depends(get_current_active_user)
):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

def get_current_cinema_admin(
    current_user: models.User = Depends(get_current_active_user)
):
    if current_user.role == UserRole.ADMIN:
        return current_user
    
    if current_user.role == UserRole.CINEMA_ADMIN and current_user.cinema_id:
        return current_user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Cinema admin rights required"
    )

def get_cinema_admin_for_cinema(cinema_id: int):
    async def dependency(
        current_user: models.User = Depends(get_current_active_user)
    ):
        if current_user.role == UserRole.ADMIN:
            return current_user
        
        if (current_user.role == UserRole.CINEMA_ADMIN and 
            current_user.cinema_id == cinema_id):
            return current_user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this cinema"
        )
    return dependency