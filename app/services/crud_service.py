from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models.models import ParsedFile, SuipData
from app.schemas.parsed_file import ParsedFileCreate


async def create_parsed_file_with_metadata(
    db: AsyncSession,
    file_data: ParsedFileCreate
) -> ParsedFile:
    """
    создает запись ParsedFile и связывает все ее метаданные в бд.
    flush используется для вытягивания айдишника parsed_file перед транзакцией.
    """
    parsed_file = ParsedFile(
        filename=file_data.filename,
        mimetype=file_data.mimetype,
    )
    db.add(parsed_file)
    await db.flush()

    metadata = [
        SuipData(
            key=meta.key,
            value=meta.value,
            parsed_file_id=parsed_file.id
        )
        for meta in file_data.metadata
    ]
    db.add_all(metadata)
    await db.commit()
    await db.refresh(parsed_file, attribute_names=["metadata"])

    return parsed_file

async def get_all_parsed_files(
    db: AsyncSession,
    filename: Optional[str] = None,
    key: Optional[str] = None,
    value: Optional[str] = None
) -> List[ParsedFile]:
    stmt = select(ParsedFile).options(selectinload(ParsedFile.metadata))

    if filename:
        stmt = stmt.where(ParsedFile.filename.ilike(f"%{filename}%"))

    if key or value:
        stmt = stmt.join(ParsedFile.metadata)
        if key:
            stmt = stmt.where(SuipData.key.ilike(f"%{key}%"))
        if value:
            stmt = stmt.where(SuipData.value.ilike(f"%{value}%"))

    result = await db.execute(stmt)
    return result.scalars().unique().all()

