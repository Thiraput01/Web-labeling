from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.crud.map_img import (
    create_map_img,
    get_map_img_by_id,
    del_map_img_by_id,
    get_all_map_img
)
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.map_img import (
    MapImageBase
)
from app.core.authentication import validate_token, validate_admin_token

router = APIRouter(
    prefix="/map-img",
    tags=["Map Image"],
    responses={404: {"message": "Not found"}}
)

get_db = init_db.get_db

@router.post('/add-map-img', status_code=status.HTTP_201_CREATED)
async def add_map_img(request: MapImageBase, db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return create_map_img(request, db)

@router.get('/map-img/{id}', response_model=MapImageBase)
async def get_by_id(id, db: Session = Depends(get_db), token = Depends(validate_token)):
    return get_map_img_by_id(id, db)

@router.get('/all', response_model=List[MapImageBase])
async def get_all(db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return get_all_map_img(db)

@router.delete('/delete/{id}')
async def delete_by_id(id, db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return del_map_img_by_id(id, db)