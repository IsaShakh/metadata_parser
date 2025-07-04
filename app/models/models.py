from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.db.init_db import Base


class ParsedFile(Base):
    __tablename__ = "parsed_file"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    mimetype = Column(String, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())


class SuipData(Base):
    __tablename__ = "suip_data"

    id = Column(Integer, primary_key=True, index=True)
    parsed_file_id = Column(Integer, ForeignKey("parsed_file.id", ondelete="CASCADE"), nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    parsed_file = relationship("ParsedFile", backref="metadata")
