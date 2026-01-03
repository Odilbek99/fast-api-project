from fastapi import FastAPI, Depends, status, Response, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from . import schemas,models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog  


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=["Blogs"])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"Blog with id {id} deleted successfully"}
        )


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,tags=["Blogs"])
def update_blog(
    id: int,
    request: schemas.Blog,
    db: Session = Depends(get_db)
):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog.title = request.title
    blog.body = request.body

    db.commit()
    db.refresh(blog)
    return blog





@app.get("/blog", response_model=list[schemas.ShowBlog], status_code=status.HTTP_200_OK,tags=["Blogs"])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{id}", response_model=schemas.ShowBlog, status_code=status.HTTP_200_OK,tags=["Blogs"])
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog

@app.post("/user",response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED,tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    new_user = models.User(username=request.username, email=request.email, password=Hash().argon2_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user", response_model=list[schemas.ShowUser], status_code=status.HTTP_200_OK,tags=["Users"])
def get_user(db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user

@app.get("/user/{id}", response_model=schemas.ShowUser, status_code=status.HTTP_200_OK,tags=["Users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return user


