from typing import List
from fastapi import FastAPI, HTTPException, status
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from models import Todo, TodoIn_Pydantic, Todo_Pydantic

from pydantic import BaseModel


class Message(BaseModel):
    msg: str


app = FastAPI(title="Todo API", version="v 1.0.1")

# Create, Read, Update, Delete

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/todos", response_model=Todo_Pydantic)
async def create_todo(todo: TodoIn_Pydantic):
    obj = await Todo.create(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_tortoise_orm(obj)


@app.get("/todos/{todo_id}", response_model=Todo_Pydantic, responses={404: {'model': HTTPNotFoundError}})
async def get_todo_by_id(todo_id: int):
    try:
        return await Todo_Pydantic.from_queryset_single(Todo.get(id=todo_id))
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found: Todo is not created")


@app.get("/todos", response_model=List[Todo_Pydantic], responses={404: {'model': HTTPNotFoundError}})
async def get_all_todos():
    try:
        return await Todo_Pydantic.from_queryset(List[Todo])
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found: Todo is not created")


@app.put("/todos/{todo_id}", response_model=Todo_Pydantic, responses={404: {'model': HTTPNotFoundError}})
async def update_todo(todo_id: int, todo: TodoIn_Pydantic):
    await Todo.filter(id=todo_id).update(**todo.dict(exclude_unset=True))
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=todo_id))


@app.delete("/todos/{todo_id}", response_model=Message, responses={404: {'model': HTTPNotFoundError}})
async def delete_todo(todo_id: int):
    delete_obj = await Todo.filter(id=todo_id).delete()
    if not delete_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return Message(msg="Successfully deleted")



register_tortoise(
    app,
    db_url="sqlite://store.db",
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)