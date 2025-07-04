from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from app.schemas.suip_data import SuipDataCreate, SuipDataRead


class ParsedFileBase(BaseModel):
    filename: str
    mimetype: Optional[str] = None


class ParsedFileCreate(ParsedFileBase):
    metadata: List[SuipDataCreate]


class ParsedFileRead(ParsedFileBase):
    id: int
    uploaded_at: datetime
    metadata: List[SuipDataRead]

    class Config:
        orm_mode = True