from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models
from ..hashing import Hash


def get_all_users(db: Session):
    users = db.query(models.User).all()
    return users


def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found"
        )
    return user


def create_user(db: Session, request):
    new_user = models.User(
        username=request.username,
        email=request.email,
        password=Hash.hash_password(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
