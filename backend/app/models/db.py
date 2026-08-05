from sqlalchemy import Column, String, Boolean, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"
    
    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    claim_object = Column(String)
    user_claim = Column(String)
    image_urls = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
class ClaimResult(Base):
    __tablename__ = "claim_results"
    
    id = Column(String, primary_key=True, index=True)
    claim_id = Column(String, index=True)
    claim_status = Column(String)
    issue_type = Column(String)
    severity = Column(String)
    risk_flags = Column(JSON)
    claim_status_justification = Column(String)
