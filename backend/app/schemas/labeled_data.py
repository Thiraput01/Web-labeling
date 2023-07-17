from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class LabeledDataBase(BaseModel):
    labeled_data_id: str
    user_id: str
    data_id: str
    labeled_class: int

    class Config:
        orm_mode = True