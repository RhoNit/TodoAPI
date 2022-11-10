from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Todo(Model):
    id = fields.IntField(pk=True)
    todo = fields.CharField(max_length=50)
    due_date = fields.CharField(max_length=250)

    class PydanticMeta:
        table = "Todo-list"


Todo_Pydantic = pydantic_model_creator(Todo, name="Todo")
TodoIn_Pydantic = pydantic_model_creator(Todo, name="TodoIn", exclude_readonly=True)