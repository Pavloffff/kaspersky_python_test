import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict


class TagCache:
    """Класс для управления кешем некорректных тегов с функцией отложенного удаления."""

    def __init__(
            self,
            task_id: int,
            expiration_time: timedelta = timedelta(
            weeks=2)):
        """
        Инициализация кеша.

        :param task_id: Идентификатор задачи, используемый для создания уникального файла кеша.
        :type task_id: str
        :param expiration_time: Время, после которого некорректный тег считается просроченным.
        :type expiration_time: timedelta
        """
        project_dir = Path(os.getenv("PROJECT_DIR", Path.cwd()))
        self._cache_file = project_dir / ".cache" / f"cache_{task_id}.json"
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.datetime_now = datetime.now()
        self.expiration_time = expiration_time
        self.cache = self.load_cache()

    def load_cache(self) -> Dict[str, str]:
        """Загружает кеш из файла, если он существует."""
        if self._cache_file.exists():
            with open(self._cache_file, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save_cache(self) -> None:
        """Сохраняет кеш в файл."""
        with open(self._cache_file, "w", encoding="utf-8") as file:
            json.dump(self.cache, file)

    def is_tag_expired(self, tag: str) -> bool:
        """Проверяет, истек ли срок хранения тега в кеше.

        :param tag: Тег, который нужно проверить на истечение срока.
        :type tag: str
        :return: True, если срок хранения тега истек, иначе False.
        :rtype: bool
        """
        expiration_date = datetime.fromisoformat(self.cache.get(tag))
        return self.datetime_now > expiration_date

    def insert_tag(self, tag: str) -> None:
        """Добавляет некорректный тег в кеш с установкой срока истечения.

        :param tag: Некорректный тег, который нужно добавить в кеш.
        :type tag: str
        """
        self.cache[tag] = (
            self.datetime_now +
            self.expiration_time).isoformat()

    def find_tag(self, tag: str) -> bool:
        """Находит тег в кеше.

        :param tag: Некорректный тег, котрый надо найти в кеше.
        :type tag: str
        :return: True, если тег есть в кеше; False, если тег не найден.
        :rtype: bool
        """
        return tag in self.cache
