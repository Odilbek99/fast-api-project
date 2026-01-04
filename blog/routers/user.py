from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..repository import user


router = APIRouter(
    tags=["Users"],
    prefix="/user"
    )

@router.post("/",response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create_user(db, request)


@router.get("/", response_model=list[schemas.ShowUser], status_code=status.HTTP_200_OK)
def get_user(db: Session = Depends(get_db)):
    return user.get_all_users(db)

@router.get("/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.get_user_by_id(db, id)




