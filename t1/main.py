import sys

from pathlib import Path
from src.parsers import ArgumentParser
from src.parsers.argument_parser import print_help
from src.utils.record_transformer import transform_html_to_records
from src.processors import apply_tag_rules


def main():
    arg_parser = ArgumentParser()
    args = sys.argv[1:]
    arg_parser.parse_args(args)

    if arg_parser.show_help:
        print_help()
        return

    input_file = arg_parser.input_file
    if input_file == "stdin":
        tags = input()
    else:
        tags = Path(input_file).read_text()

    rules = transform_html_to_records(arg_parser.rules_table_path)
    result_tags = apply_tag_rules(
        tags,
        rules,
        task_id=arg_parser.task_id,
        delayed_clean=arg_parser.delayed_clean
    )

    output_file = arg_parser.output_file
    if output_file == "stdout":
        print(result_tags)
    else:
        Path(output_file).write_text(result_tags, encoding="utf-8")


if __name__ == '__main__':
    main()
