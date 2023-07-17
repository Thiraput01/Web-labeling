from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.crud.labeled_data import (
    create_labeled_data,
    get_labeled_data_by_id,
    del_labeled_data_by_id,
    get_all_labeled_data
)
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.labeled_data import (
    LabeledDataBase,
)
from app.core.authentication import validate_token, validate_admin_token

router = APIRouter(
    prefix="/labeled-data",
    tags=["Labeled Data"],
    responses={404: {"message": "Not found"}}
)

get_db = init_db.get_db

@router.post("/add-labeled-data", status_code=status.HTTP_201_CREATED)
async def add_labeled_data(request: LabeledDataBase, db: Session = Depends(get_db), token = Depends(validate_token)):
    return create_labeled_data(request, db)

@router.get("/data/{id}", response_model=LabeledDataBase)
async def get_by_id(id, db: Session = Depends(get_db), token = Depends(validate_token)):
    return get_labeled_data_by_id(id, db)

@router.get("/all", response_model=List[LabeledDataBase])
async def get_all(db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return get_all_labeled_data(db)

@router.delete("/delete/{id}")
async def delete_by_id(id, db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return del_labeled_data_by_id(id, db)