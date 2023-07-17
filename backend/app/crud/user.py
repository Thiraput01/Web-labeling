from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.init_db import SessionLocal, get_db
from app.models import user
from app.core import authentication
from app.schemas.user import UserBase, UserAuth, UserRegister
from app.schemas.data_for_label import DataForLabel

def create_user(request:UserRegister, db:Session):
    authentication.validate_register_key(request.register_key)
    is_user_existed = find_by_username(request.username, db)
    if is_user_existed:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
        detail=f"Username {request.username} already existed")
    
    hashed_password = authentication.get_password_hash(request.password)
    new_user = user.User(username=request.username, 
                         password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def find_by_username(username:str, db:Session):
    return db.query(user.User).filter(user.User.username == username).first()

def get_to_label_data_list(username:str, db: Session = Depends(get_db)):
    # format to_label_data string of given user to list
    user_data = db.query(user.User).filter(user.User.username == username).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {username} not found")
    if user_data.to_label_data is None:
        return []
    else:
        to_label_data_list = user_data.to_label_data.split(',')
        return to_label_data_list

def add_to_label_data(username:str, data_id:str, db: Session = Depends(get_db)):
    # add data_id to to_label_data of given user
    user_data = db.query(user.User).filter(user.User.username == username).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {username} not found")
    if user_data.to_label_data is None:
        user_data.to_label_data = str(data_id)
    else:
        user_data.to_label_data = user_data.to_label_data + ',' + str(data_id)
    db.commit()
    db.refresh(user_data)
    return user_data

def get_user_labeled_data(username:str, db: Session = Depends(get_db)):
    # get labeled data of given user
    user_data = db.query(user.User).filter(user.User.username == username).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {username} not found")
    if user_data.labeled_data is None:
        return []
    else:
        labeled_data_list = user_data.labeled_data.split(',')
        return labeled_data_list
    
def add_user_labeled_data(username:str, data_id:str, db: Session = Depends(get_db)):
    # add data_id to labeled_data of given user
    user_data = db.query(user.User).filter(user.User.username == username).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {username} not found")
    if user_data.labeled_data is None:
        user_data.labeled_data = str(data_id)
    else:
        user_data.labeled_data = user_data.labeled_data + ',' + str(data_id)
    db.commit()
    db.refresh(user_data)
    return user_data