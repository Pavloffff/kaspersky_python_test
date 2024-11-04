import re
from pathlib import Path
from typing import List


class HTMLParser:
    """Парсер для поиска и извлечения содержимого HTML-тегов"""

    def __init__(self, path_string: str):
        """
        Инициализирует парсер с содержимым HTML-файла.

        :param path_string: Путь к HTML-файлу.
        :type path_string: str
        """
        html_file_path: Path = Path(path_string)
        self.html_data = html_file_path.read_text(encoding='utf-8')

    def find(self, tag: str) -> List[str]:
        """
        Находит и возвращает содержимое всех вхождений указанного HTML-тега.

        :param tag: Название HTML-тега, содержимое которого нужно найти (например, "td" или "th").
        :type tag: str
        :return: Список строк, содержащих содержимое каждого вхождения тега.
        :rtype: List[str]
        """
        open_tag: str = f"<{tag}>"
        close_tag: str = f"</{tag}>"
        matches: List[str] = []
        for match in re.finditer(
            f"{open_tag}(.*?){close_tag}",
            self.html_data,
                re.DOTALL):
            matches.append(match.group(1).strip())
        return matches
