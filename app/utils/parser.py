from typing import Tuple, List
from bs4 import BeautifulSoup
import httpx
from pathlib import Path

async def parse_file_metadata(filepath: Path) -> Tuple[str, str, List[Tuple[str, str]]]:
    """
    отправляет файл на exif.tools(suip.biz не работает!) POST запросом через httpx.
    парсит html таблицу от exif и возвращает данные по структуре:
    - filename;
    - mimetype;
    - metadata(список кортежей)
    """
    url = "https://exif.tools/upload.php"
    filename = filepath.name

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html",
        "Referer": "https://exif.tools/"
    }

    with open(filepath, "rb") as f:
        files = {"upfile": (filename, f, "application/octet-stream")}
        data = {"submit": "Upload File"}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, data=data, files=files)
            response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table")
    if not table:
        raise ValueError("Метаданные не найдены")

    metadata: List[Tuple[str, str]] = []
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) == 2:
            for tag in cols[0].find_all(["a", "img"]): tag.decompose()
            for tag in cols[1].find_all(["a", "img"]): tag.decompose()
            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            if key and value and "Binary data" not in value:
                metadata.append((key, value))

    mimetype = next((v for k, v in metadata if k.lower() == "mime type"), "application/octet-stream")
    return filename, mimetype, metadata

