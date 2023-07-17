from fastapi import HTTPException, status
from sqlalchemy.orm import Session, load_only
from app.models.labeled_data import LabeledData
from app.models.user import User
from app.schemas.labeled_data import LabeledDataBase

def create_labeled_data(request:LabeledDataBase, db:Session):
    is_labeled_data_existed = db.query(LabeledData).filter(LabeledData.labeled_data_id == request.labeled_data_id).first()
    if is_labeled_data_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail=f"Labeled data with an id {request.labeled_data_id} already existed")
    
    labeled_data = LabeledData(labeled_data_id=request.labeled_data_id,
                                user_id=request.user_id,
                                data_id=request.data_id,
                                labeled_class=request.labeled_class,
                                )
    
    db.add(labeled_data)
    db.commit()
    return {"Created labeled data id": labeled_data.labeled_data_id}

def get_labeled_data_by_id(id, db:Session):
    labeled_data = db.query(LabeledData).filter(LabeledData.labeled_data_id == id).first()
    if not labeled_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found a labeled data with an id: {id}")
    return labeled_data

def get_all_labeled_data(db:Session):
    labeled_data = db.query(LabeledData).all()
    if not labeled_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found any labeled data")
    return labeled_data

def del_labeled_data_by_id(id, db:Session):
    labeled_data = db.query(LabeledData).filter(LabeledData.labeled_data_id == id)

    if not labeled_data.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found a labeled data with an id: {id}")
    labeled_data.delete(synchronize_session=False)
    return {"Deleted labeled data id": id}