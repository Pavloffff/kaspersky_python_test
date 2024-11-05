import sys
import re
from typing import List


def print_help() -> None:
    """Выводит справочную информацию о возможных флагах программы."""
    help_text = """
    Available flags for Configuration Calculator:
    --config=<path/to/config.json>           : Path to the JSON config file. Required.
    --params=<path/to/params.json>           : Path to the JSON parameters file. Required.
    --output=<output_path>                   : Output file for configuration result. Required, supports 'stdout'.
    -h                                       : Show help message.
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
    """Извлекает значение для флагов --config, --params и --output.

    :param arg: Аргумент командной строки с флагом.
    :type arg: str
    :param flag_name: Название флага для отображения в сообщении об ошибке.
    :type flag_name: str
    :return: Путь к файлу или специальные значения ('stdout').
    :rtype: str
    """
    match: re.Match[str] = re.match(fr'{flag_name}=(.+)', arg)
    if not match or not match.group(1):
        _raise_error(f"Invalid or missing value for {flag_name} flag")
    return match.group(1)


class ArgumentParser:
    """Парсер аргументов командной строки.

    Поддерживаемые аргументы:
    --config=<path/to/config.json>           : Путь к JSON файлу конфигурации (обязательный).
    --params=<path/to/params.json>           : Путь к JSON файлу с параметрами (обязательный).
    --output=<output_path>                   : Выходной файл для результата конфигурации (обязательный), поддерживает 'stdout'.
    -h                                       : Выводит справочную информацию.
    """

    def __init__(self):
        self.config_path: str | None = None
        self.params_path: str | None = None
        self.output_file: str | None = None
        self.show_help: bool = False

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
            elif arg.startswith("--config="):
                self.config_path = _parse_file_path_arg(arg, "--config")
            elif arg.startswith("--params="):
                self.params_path = _parse_file_path_arg(arg, "--params")
            elif arg.startswith("--output="):
                self.output_file = _parse_file_path_arg(arg, "--output")
            else:
                _raise_error(f"Invalid flag: {arg}")

        self._validate_args_combination()

    def _validate_args_combination(self):
        """Валидация комбинации аргументов.

        Проверяет обязательность флагов --config, --params и --output.
        """
        if self.config_path is None:
            _raise_error("Missing required flag: --config")
        if self.params_path is None:
            _raise_error("Missing required flag: --params")
        if self.output_file is None:
            _raise_error("Missing required flag: --output")
