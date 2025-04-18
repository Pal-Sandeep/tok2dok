from pydantic import BaseModel
from datetime import datetime

class PDFCreate(BaseModel):
    filename: str
    content: str

class PDFResponse(BaseModel):
    id: int
    filename: str
    created_at: datetime

    class Config:
        orm_mode = True
