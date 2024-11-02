from typing import NamedTuple


class AllowedTagRecord(NamedTuple):
    """Запись в таблице правил"""
    allowed_name: str
    synonyms: str | None = None
    immutable: bool = False
    separated: bool = False

    def get_synonyms_as_set(self):
        """
        Представление атрибута synonyms в виде сета ее подстрок, разделенных ', '

        :return: Сет подстрок атрибута synonyms
        :rtype: set[str]
        """
        synonyms_set = {self.allowed_name}
        if self.synonyms is None:
            return synonyms_set
        for synonym in self.synonyms.split(", "):
            synonyms_set.add(synonym)
        return synonyms_set


def cases_to_flat(text: str) -> str:
    """
    Преобразование строку из стиля snake_case, kebab-case, СamelCase и т.д. в слитное написание в нижнем регистре.

    :param text: Строка в стиле snake_case, kebab-case, СamelCase и т.д.
    :type text: str
    :return: Строка со словами, объединенными без разделителей в нижнем регистре.
    :rtype: str
    """
    return text.translate(str.maketrans('', '', '-_')).lower()


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
    separated_tags: list[str] = []
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

    result_tags: dict[str, int] = {}
    for tag in tags.split("; "):
        for rule in rules:
            for synonym in rule.get_synonyms_as_set():
                immutable = rule.immutable

                rule_key = synonym.lower() if immutable else cases_to_flat(synonym.lower())
                tag_key = tag.lower() if immutable else cases_to_flat(tag.lower())

                if tag_key == rule_key:
                    result_tags[rule.allowed_name] = 0
                    break

                elif rule.separated and tag_key.find(rule_key) != -1:
                    separated_tags = separated_tags_treatment(
                        tag_key, rules, immutable)

                    for separated_tag in separated_tags:
                        result_tags[separated_tag] = 0

    return "; ".join(result_tags.keys())
