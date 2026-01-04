from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from .. import database, models, token
from ..hashing import Hash

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(),
    df: database = Depends(database.get_db),
):
    user = (
        df.query(models.User).filter(models.User.username == request.username).first()
    )
    if not user:
        raise HTTPException(status_code=404, detail="Invalid Credentials")
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect Password")

    access_token = token.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
