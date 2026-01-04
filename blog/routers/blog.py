from fastapi import APIRouter
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from ..repository import blog

router = APIRouter(tags=["Blogs"], prefix="/blog")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    return blog.create_blog(db, request)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(get_db)):
    return blog.delete_blog(db, id)


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(get_db)
):
    return blog.update_blog(db, id, request.title, request.body)

@router.get("/", response_model=list[schemas.ShowBlog], status_code=status.HTTP_200_OK)
def get_blogs(db: Session = Depends(get_db)):
    return blog.get_all_blogs(db)

@router.get("/{id}", response_model=schemas.ShowBlog, status_code=status.HTTP_200_OK)
def get_blog(id: int, db: Session = Depends(get_db)):
    return blog.get_blog_by_id(db, id)

