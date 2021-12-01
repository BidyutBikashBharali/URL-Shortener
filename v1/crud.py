from typing import List, Optional
from sqlalchemy.orm import Session
from .model import UrlModel



def get_data_by_short_code(session: Session, short_code: str) -> UrlModel:
    return session.query(UrlModel).filter(UrlModel.short_code == short_code).first()


def get_all_data(session: Session, skip: Optional[int] = 0, limit: Optional[int] = None) -> List[UrlModel]:
    return session.query(UrlModel).offset(skip).limit(limit).all()
