import sys
import re
from typing import List


def print_help() -> None:
    """Выводит справочную информацию о возможных флагах программы."""
    help_text = """
    Available flags:
    --path-to-rules-table=<rules_table_path> : Path to the HTML file. Required.
    -h                                       : Show help message.
    --task-id=<int>                          : Specify task ID (integer). Optional, required for --delayed-clean.
    --delayed-clean                          : Flag for enabling delayed clean mode. Optional, requires --task-id.
    --input=<input_path>                     : Input file with tags. Required, supports 'stdin'.
    --output=<output_path>                   : Output file for tags. Required, supports 'stdout'.
    """
    print(help_text)


def _raise_error(message: str) -> None:
    """Выводит сообщение об ошибке и завершает программу.

    :param message: Текст ошибки.
    :type message: str
    """
    print(f"Error: {message}")
    print("Use -h to see available options.")
    sys.exit(1)


def _parse_file_path_arg(arg: str, flag_name: str) -> str:
    """Извлекает значение для флагов --input, --output и --path-to-rules-table.

    :param arg: Аргумент командной строки с флагом.
    :type arg: str
    :param flag_name: Название флага для отображения в сообщении об ошибке.
    :type flag_name: str
    :return: Путь к файлу или специальные значения ('stdin', 'stdout').
    :rtype: str
    """
    match: re.Match[str] = re.match(fr'{flag_name}=(.+)', arg)
    if not match or not match.group(1):
        _raise_error(f"Invalid or missing value for {flag_name} flag")
    return match.group(1)


def _parse_task_id(arg: str) -> int:
    """Извлекает значение task_id из аргумента --task-id.

    :param arg: Аргумент командной строки с флагом --task-id.
    :type arg: str
    :return: Значение task_id.
    :rtype: int
    """
    match: re.Match[str] = re.match(r'--task-id=(\d+)', arg)
    if not match:
        _raise_error("Invalid task_id: must be an integer")
    return int(match.group(1))


class ArgumentParser:
    """Парсер аргументов командной строки.

    Поддерживаемые аргументы:
    --path-to-rules-table=<rules_table_path> : Путь к HTML файлу с правилами (обязательный).
    -h                                       : Выводит справочную информацию.
    --task-id=<int>                          : Устанавливает ID задачи (необязательный, требуется для --delayed-clean).
    --delayed-clean                          : Устанавливает флаг отложенного удаления (требует указания --task-id).
    --input=<input_path>                     : Входной файл с тегами (обязательный), поддерживает 'stdin'.
    --output=<output_path>                   : Выходной файл для тегов (обязательный), поддерживает 'stdout'.
    """

    def __init__(self):
        self.rules_table_path: str | None = None
        self.show_help: bool = False
        self.task_id: int | None = None
        self.delayed_clean: bool = False
        self.input_file: str | None = None
        self.output_file: str | None = None

    def parse_args(self, args: List[str]):
        """Парсит аргументы командной строки.

        :param args: Список аргументов командной строки.
        :type args: list[str]
        """
        if not args:
            _raise_error("No flags provided")

        for arg in args:
            if arg == "-h":
                self.show_help = True
                return
            elif arg.startswith("--path-to-rules-table="):
                self.rules_table_path = _parse_file_path_arg(
                    arg, "--path-to-rules-table")
            elif arg.startswith("--task-id="):
                self.task_id = _parse_task_id(arg)
            elif arg == "--delayed-clean":
                self.delayed_clean = True
            elif arg.startswith("--input="):
                self.input_file = _parse_file_path_arg(arg, "--input")
            elif arg.startswith("--output="):
                self.output_file = _parse_file_path_arg(arg, "--output")
            else:
                _raise_error(f"Invalid flag: {arg}")

        self._validate_args_combination()

    def _validate_args_combination(self):
        """Валидация комбинации аргументов.

        Проверяет обязательность флагов --path-to-rules-table, --input, --output,
        и зависимости --delayed-clean от --task-id.
        """
        if self.delayed_clean and self.task_id is None:
            _raise_error("--delayed-clean flag requires --task-id")
        if self.rules_table_path is None and not self.show_help:
            _raise_error("Missing required flag: --path-to-rules-table")
        if self.input_file is None:
            _raise_error("Missing required flag: --input")
        if self.output_file is None:
            _raise_error("Missing required flag: --output")
