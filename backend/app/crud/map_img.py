from fastapi import HTTPException, status
from sqlalchemy.orm import Session, load_only
from app.models.map_img import MapImage
from app.schemas.map_img import MapImageBase

def create_map_img(request:MapImageBase, db:Session):
    is_map_img_existed = db.query(MapImage).filter(MapImage.map_img_id == request.map_img_id).first()
    if is_map_img_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail=f"Map image with an id {request.map_img_id} already existed")
    
    map_img = MapImage(map_img_id=request.map_img_id,
                        map_img_url=request.map_img_url,
                        )
    db.add(map_img)
    db.commit()
    return {"Created map image id":map_img.map_img_id}

def get_map_img_by_id(id, db:Session):
    map_img = db.query(MapImage).filter(MapImage.map_img_id == id).first()
    if not map_img:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found a map image with an id: {id}")
    return map_img

def get_all_map_img(db:Session):
    map_img = db.query(MapImage).all()
    if not map_img:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found any map image")
    return map_img

def del_map_img_by_id(id, db:Session):
    map_img = db.query(MapImage).filter(MapImage.map_img_id == id).first()
    if not map_img:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Not found a map image with an id: {id}")
    db.delete(map_img)
    db.commit()
    return {'Deleted map image id':id}