import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello, World!"}


@app.get("/about/")
def about():
    return {"message": "This is the about page."}


@app.get("/blog")
def about(limit):
    return {"data": f"The limit is {limit}"}


@app.get("/blog/{id}")
def about(id: int):
    return {"data": id}


class Blog(BaseModel):
    title: str
    body: str
    published: bool = True


@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": f'Blog titled "{blog.title}" created successfully!'}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
