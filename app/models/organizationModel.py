from core.config.database import Base
from sqlalchemy import Column, Integer, String

class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True)
    companyregid = Column(String)
    name = Column(String)
    address = Column(String)