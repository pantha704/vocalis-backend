# models.py
from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

class TextOutput(BaseModel):
    response: str