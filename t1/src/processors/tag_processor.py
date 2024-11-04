from typing import Dict, Set

from src.cache import TagCache
from src.entities import AllowedTagRecord
from src.utils import manage_incorrect_tag


def cases_to_flat(text: str) -> str:
    """
    Преобразование строку из стиля snake_case, kebab-case, СamelCase и т.д. в слитное написание в нижнем регистре.

    :param text: Строка в стиле snake_case, kebab-case, СamelCase и т.д.
    :type text: str
    :return: Строка со словами, объединенными без разделителей в нижнем регистре.
    :rtype: str
    """
    return text.translate(str.maketrans('', '', ' -_')).lower()


def separated_tags_treatment(
        tag_str: str,
        rules_tuple: tuple[AllowedTagRecord, ...],
        immutable: bool
) -> list[str]:
    """
    Применение к тегу правил для составных тегов

    :param tag_str: Строка, содержащая составной тег
    :param rules_tuple: Кортеж правил
    :param immutable: Флаг зарезервированности тега текущего правила
    :return: Список тегов, содержащихся в строке
    :rtype: list[str]
    """
    separated_tags: list[str] = []  # модифицировать словарь
    flag: bool = False

    while len(tag_str) > 0:
        for tag_part_rule in rules_tuple:
            for tag_part_synonym in tag_part_rule.get_synonyms_as_set():
                tag_part_key = tag_part_synonym.lower(
                ) if immutable else cases_to_flat(tag_part_synonym.lower())

                if tag_str.startswith(tag_part_key):
                    separated_tags.append(
                        tag_part_rule.allowed_name)
                    tag_str = tag_str[len(tag_part_key):]
                    flag = True

        if not flag:
            return []
    return separated_tags


def apply_tag_rules(
        tags: str,
        rules: tuple[AllowedTagRecord, ...],
        task_id: int | None = None,
        delayed_clean: bool = False
) -> str:
    """
    Применение правил к тегам

    :param tags: Строка, содержащая теги.
    :param rules: Кортеж правил.
    :param task_id: Идентификатор задачи, опциональное поле для дополнительного задания.
    :param delayed_clean: флаг, сигнализирующий о включении дополнительной функциональности -
     отложенного удаления неверных тегов.
    :return str: Возвращает строку с преобразованными тегами.
    """
    if tags == "":
        return ""

    tag_cache: TagCache | None = None
    if delayed_clean:
        tag_cache = TagCache(
            task_id=task_id,
        )
        tag_cache.load_cache()

    result_tags: Dict[str, int] = {}
    for tag in tags.split(";"):
        tag: str = tag.strip()
        is_tag_correct: bool = False
        for rule in rules:
            for synonym in rule.get_synonyms_as_set():
                immutable = rule.immutable

                rule_key = synonym.lower() if immutable else cases_to_flat(synonym.lower())
                tag_key = tag.lower() if immutable else cases_to_flat(tag.lower())

                if tag_key == rule_key:
                    result_tags[rule.allowed_name] = 0
                    is_tag_correct = True
                    break

                elif rule.separated and tag_key.find(rule_key) != -1:
                    separated_tags = separated_tags_treatment(
                        tag_key, rules, immutable)

                    if len(separated_tags) > 0:
                        is_tag_correct = True

                        for separated_tag in separated_tags:
                            result_tags[separated_tag] = 0

                        break

        if not is_tag_correct and delayed_clean:
            manage_incorrect_tag(tag_cache, tag, result_tags)

    if delayed_clean:
        tag_cache.save_cache()

    return "; ".join(result_tags.keys())
