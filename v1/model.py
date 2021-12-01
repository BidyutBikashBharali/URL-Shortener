from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship


from .db import Base

from datetime import datetime


class UrlModel(Base):

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    original_url = Column(String, nullable=False)
    shortened_url = Column(String, nullable=False)
    short_code = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    url_expiration = Column(DateTime, nullable=True) # datetime will be inserted after calculating created datetime with the user given "days_for_url_expiration"
    days_for_url_expiration = Column(Integer, nullable=True)
    total_visited_times = Column(Integer, default=0)
