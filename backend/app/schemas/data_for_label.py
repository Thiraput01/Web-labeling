from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class DataForLabelBase(BaseModel):
    data_id: str
    map_img_url: str
    map_img_id: str
    data_coordinate_x: float
    data_coordinate_y: float

    class Config:
        orm_mode = True

class DataForLabel(BaseModel):
    data_id: UUID

    class Config:
        orm_mode = True
