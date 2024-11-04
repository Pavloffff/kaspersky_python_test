from src.cache import TagCache


def manage_incorrect_tag(cache: TagCache, tag: str,
                         result_tags: dict[str, int]):
    """
    Управляет добавлением некорректного тега в кеш и обработкой его срока истечения.

    Если тег не найден в кеше, добавляет его с текущей датой и устанавливает срок истечения.
    Если срок истечения тега еще не подошел, добавляет его в результат.

    :param cache: Экземпляр TagCache, используемый для управления некорректными тегами.
    :type cache: TagCache
    :param tag: Некорректный тег, который нужно обработать.
    :type tag: str
    :param result_tags: Словарь результатов, где ключ — это тег, а значение — статус включения (например, 0).
                            Тег добавляется в словарь, если срок его истечения еще не подошел.
    :type result_tags: dict[str, int]
    """
    if not cache.find_tag(tag):
        cache.insert_tag(tag)
    if not cache.is_tag_expired(tag):
        result_tags[tag] = 0
