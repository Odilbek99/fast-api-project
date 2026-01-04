from sqlalchemy.orm import Session
from ..models import Blog
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

def get_all_blogs(db: Session):
    blogs = db.query(Blog).all()
    return blogs

def get_blog_by_id(db: Session, blog_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found") 
    return blog

def update_blog(db: Session, blog_id: int, title: str, body: str):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found") 
    blog.title = title
    blog.body = body
    db.commit()
    db.refresh(blog)
    return blog

def delete_blog(db: Session, blog_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found") 
    db.delete(blog)
    db.commit()
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Blog with id {id} deleted successfully"}
        )


def create_blog(db: Session, request):
    new_blog = Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog