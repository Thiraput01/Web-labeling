from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import  Column, ForeignKey, String, DateTime, Float, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from ..database.init_db import Base

class MapImage(Base):
    __tablename__ = "map_image"

    map_img_id = Column(String(100), primary_key=True)
    map_img_url = Column(String(2048))