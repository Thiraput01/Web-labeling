from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, ForeignKey, String, DateTime, Float, Integer,Text
from sqlalchemy.orm import relationship
from ..database.init_db import Base

class LabeledData(Base):
    __tablename__ = "labaled_data"

    labeled_data_id = Column(String(100), primary_key=True)
    user_id = Column(String(100))
    data_id = Column(String(100))
    labeled_class = Column(Integer)



