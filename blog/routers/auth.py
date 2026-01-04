from fastapi import APIRouter, Depends
from .. import schemas, database, models
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..hashing import Hash


router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(request: schemas.Login, df: database = Depends(database.get_db)):
    user = df.query(models.User).filter(models.User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect Password")

    return user

