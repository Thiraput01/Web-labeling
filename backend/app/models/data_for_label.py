from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, ForeignKey, String, DateTime, Float, Integer,Text
from sqlalchemy.orm import relationship
from ..database.init_db import Base

class DataForLabel(Base):
    __tablename__ = "data_for_label"

    data_id = Column(String(100), primary_key=True)
    map_img_id = Column(String(100))
    map_img_url = Column(String(2048))
    data_coordinate_x = Column(Float)
    data_coordinate_y = Column(Float)