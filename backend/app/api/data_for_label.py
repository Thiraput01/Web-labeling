from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.crud.data_for_label import (
    create_data_for_label,
    get_data_for_label_by_id,
    del_data_for_label_by_id,
    get_all_data_for_label
)
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.data_for_label import (
    DataForLabelBase
)
from app.core.authentication import validate_token, validate_admin_token

router = APIRouter(
    prefix="/data-for-label",
    tags=["Data for label"],
    responses={404: {"message": "Not found"}}
)

get_db = init_db.get_db

@router.post('/add-data', status_code=status.HTTP_201_CREATED)
async def add_data(request: DataForLabelBase, db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return create_data_for_label(request, db)

@router.get('/data/{id}', response_model=DataForLabelBase)
async def get_by_id(id, db: Session = Depends(get_db), token = Depends(validate_token)):
    return get_data_for_label_by_id(id, db)

@router.get('/all', response_model=List[DataForLabelBase])
async def get_all(db: Session = Depends(get_db), token = Depends(validate_token)):
    return get_all_data_for_label(db)

@router.delete('/delete/{id}')
async def delete_by_id(id, db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return del_data_for_label_by_id(id, db)