import tempfile
import shutil
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.parsed_file import ParsedFileCreate, ParsedFileRead
from app.schemas.suip_data import SuipDataCreate
from app.services.crud_service import create_parsed_file_with_metadata
from app.utils.parser import parse_file_metadata


async def handle_file_parsing(uploaded_file, db: AsyncSession) -> ParsedFileRead:
    """
    загруженный файл сохраняется сперва на диске, 
    после чего парсится метадата со всеми преобразованиями,
    сохраняется в файл json и бд.
    в блоке finally загруженный файл удаляется.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.filename) as tmp:
        shutil.copyfileobj(uploaded_file.file, tmp)
        temp_path = Path(tmp.name)

    try:
        filename, mimetype, raw_metadata = await parse_file_metadata(temp_path)
        metadata_objs = [SuipDataCreate(key=k, value=v) for k, v in raw_metadata]
        parsed_file_schema = ParsedFileCreate(
            filename=filename,
            mimetype=mimetype,
            metadata=metadata_objs
        )
        result = await create_parsed_file_with_metadata(db, parsed_file_schema)
        json_entry = {
            "filename": filename,
            "mimetype": mimetype,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
            "metadata": [{"key": m.key, "value": m.value} for m in metadata_objs]
        }
        try:
            with open("suip_data.json", "r", encoding="utf-8") as f:
                existing = json.load(f)
        except FileNotFoundError:
            existing = []

        existing.append(json_entry)

        with open("suip_data.json", "w", encoding="utf-8") as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

        return result

    finally:
        try:
            temp_path.unlink()
        except:
            pass
