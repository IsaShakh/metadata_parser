from pydantic import BaseModel
from datetime import datetime


class SuipDataBase(BaseModel):
    key: str
    value: str


class SuipDataCreate(SuipDataBase):
    pass


class SuipDataRead(SuipDataBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True