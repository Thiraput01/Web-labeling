from fastapi import HTTPException, status
from sqlalchemy.orm import Session, load_only
from app.models.data_for_label import DataForLabel
from app.schemas.data_for_label import DataForLabelBase

def create_data_for_label(request:DataForLabelBase, db:Session):
    is_data_for_label_existed = db.query(DataForLabel).filter(DataForLabel.data_id == request.data_id).first()
    if is_data_for_label_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail=f"Data for label with an id {request.data_id} already existed")

    data = DataForLabel(data_id=request.data_id,
                        map_img_id=request.map_img_id,
                        map_img_url=request.map_img_url,
                        data_coordinate_x=request.data_coordinate_x,
                        data_coordinate_y=request.data_coordinate_y)
                                  
    db.add(data)
    db.commit()
    return {'Created data id':data.data_id}

def get_data_for_label_by_id(id, db:Session):
    data = db.query(DataForLabel).filter(DataForLabel.data_id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found a data for label with an id: {id}")
    return data

def get_all_data_for_label(db:Session):
    data = db.query(DataForLabel).all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found any data for label")
    return data

def del_data_for_label_by_id(id, db:Session):
    data = db.query(DataForLabel).filter(DataForLabel.data_id == id).first()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found a data for label with an id: {id}")
    db.delete(data)
    db.commit()
    return {'Deleted data id':id}