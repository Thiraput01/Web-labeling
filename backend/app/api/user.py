from fastapi import APIRouter, HTTPException, status, Depends
from app.core.authentication import verify_password, create_access_token
from app.database import init_db
from sqlalchemy.orm import Session
from app.schemas.user import UserBase, UserAuth, LoginRes, User, UserRegister
from app.schemas.data_for_label import DataForLabel
from app.crud.user import (
    create_user, 
    find_by_username, 
    get_to_label_data_list,
    add_to_label_data,
    get_user_labeled_data,
    add_user_labeled_data
)
from app.core.authentication import (
    validate_token, 
    validate_admin_token, 
    get_current_username
)

router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"message": "Not found"}}
)

get_db = init_db.get_db

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
async def register(request: UserRegister, db: Session = Depends(get_db)):
    return create_user(request, db)

@router.post("/login", response_model=LoginRes, status_code=status.HTTP_200_OK)
async def login(request: UserAuth, db: Session = Depends(get_db)):
    session_user = find_by_username(request.username, db)

    if not session_user or not verify_password(request.password, session_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Incorrect username or password")
    
    access_token = create_access_token(data={"sub": session_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# route for admin to see to label data list of a user
@router.get("/to-label-data/{username}", response_model=list)
async def get_to_label_list(username:str, db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return get_to_label_data_list(username, db)

# route for user to see to label data list of himself
@router.get("/my-to-label-data", response_model=list)
async def get_my_to_label_list(db: Session = Depends(get_db), token = Depends(validate_token)):
    session_user = get_current_username(token, db)
    return get_to_label_data_list(session_user, db)

# route for admin to add data to label data list of a user
@router.post("/add-to-label-data/{username}", response_model=User)
async def add_to_data(username:str, data_id:str, db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return add_to_label_data(username, data_id, db)

# route for user to add labled data to his labeled data list
@router.post("/add-labeled-data", response_model=User)
async def add_labeled_data(data_id:str, db: Session = Depends(get_db), token = Depends(validate_token)):
    session_user = get_current_username(token, db)
    return add_user_labeled_data(session_user, data_id, db)

# route for admin to see labeled data list of a user
@router.get("/labeled-data/{username}", response_model=list)
async def get_labeled_data(username:str, db: Session = Depends(get_db), token = Depends(validate_admin_token)):
    return get_user_labeled_data(username, db)

# route for user to see his labeled data list
@router.get("/my-labeled-data", response_model=list)
async def get_my_labeled_data(db: Session = Depends(get_db), token = Depends(validate_token)):
    session_user = get_current_username(token, db)
    return get_user_labeled_data(session_user, db)