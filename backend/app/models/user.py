from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, Float, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from ..database.init_db import Base

class User(Base):
    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True,
                      index=True, default=uuid4)
    username = Column(String(50), nullable=False)
    password = Column(String(64), nullable=False)

    # list of data id that user have to label
    to_label_data = Column(Text)

    # list of data id that user have labeled
    labeled_data = Column(Text)