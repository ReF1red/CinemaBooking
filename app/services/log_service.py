import json
from sqlalchemy.orm import Session
from app.models import models
from datetime import datetime

class LogService:
    @staticmethod
    def log_action(
        db: Session,
        user_id: int,
        user_email: str,
        action_type: str,
        details: dict = None,
        ip_address: str = None
    ):
          
        log_entry = models.ActionLog(
            user_id = user_id,
            user_email = user_email,
            action_type = action_type,
            details = json.dumps(details, ensure_ascii=False) if details else None,
            ip_address = ip_address,
            timestamp = datetime.utcnow()
        )
        
        db.add(log_entry)
        db.commit()
        
        return log_entry