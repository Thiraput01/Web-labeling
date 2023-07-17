from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class MapImageBase(BaseModel):
    map_img_url: str
    map_img_id: str

    class Config:
        orm_mode = True