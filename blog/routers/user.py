from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..hashing import Hash


router = APIRouter(tags=["Users"])

@router.post("/user",response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(username=request.username, email=request.email, password=Hash().argon2_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/user", response_model=list[schemas.ShowUser], status_code=status.HTTP_200_OK)
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@router.get("/user/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return user




