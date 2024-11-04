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
        for synonym in self.synonyms.split(","):
            synonym = synonym.strip()
            synonyms_set.add(synonym)
        return synonyms_set
