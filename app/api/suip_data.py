from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.db.init_db import get_session
from app.schemas.parsed_file import ParsedFileRead
from app.services.crud_service import get_all_parsed_files
from app.services.parser_service import handle_file_parsing


router = APIRouter()

@router.post("/suip-data/parse", response_model=ParsedFileRead, summary="Парсинг и сохранение метаданных", description="Использовал exif.tools")
async def parse_and_save_file(
    uploaded_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session)
):
    try:
        return await handle_file_parsing(uploaded_file, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ОшиБка при парсинге: {str(e)}")

@router.get("/suip-data", response_model=List[ParsedFileRead], summary="GET сохраненных данных", description="Сделал фильтрацию по названию файла, подстроке в ключе/значении")
async def list_parsed_files(
    filename: Optional[str] = Query(None),
    key: Optional[str] = Query(None),
    value: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_session)
):
    return await get_all_parsed_files(db, filename=filename, key=key, value=value)
