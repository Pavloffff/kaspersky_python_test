from pathlib import Path
from typing import Tuple, List
from src.entities import AllowedTagRecord
from src.parsers import HTMLParser


def transform_html_to_records(
        html_path_string: str) -> Tuple[AllowedTagRecord, ...]:
    """
        Преобразует HTML-файл в кортеж объектов AllowedTagRecord, основываясь на данных таблицы в HTML.

        :param html_path_string: Путь к HTML-файлу, содержащему таблицу тегов.
        :type html_path_string: str
        :return: Кортеж записей AllowedTagRecord, полученных из таблицы.
        :rtype: Tuple[AllowedTagRecord, ...]
        :raises ValueError: Если заголовки таблицы не соответствуют ожидаемым.
    """

    html_parser: HTMLParser = HTMLParser(html_path_string)

    headers: List[str] = html_parser.find("th")
    expected_headers: List[str] = [
        "Тэг",
        "Комментарий",
        "Синонимы",
        "Оставить как есть",
        "Часть составного тега"]
    if headers != expected_headers:
        raise ValueError("Incorrect table headers")

    cols: List[str] = html_parser.find("td")
    records: List[AllowedTagRecord] = []

    for idx in range(0, len(cols), 5):
        allowed_name: str = cols[idx]
        synonyms: str = cols[idx + 2] or None
        immutable: bool = cols[idx + 3].lower() == "да"
        separated: bool = cols[idx + 4].lower() == "да"

        records.append(
            AllowedTagRecord(
                allowed_name=allowed_name,
                synonyms=synonyms,
                immutable=immutable,
                separated=separated
            )
        )

    return tuple(records)
