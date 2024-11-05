import sys
from pathlib import Path

from src.calculator import Calculator
from src.parsers import ArgumentParser, load_config, save_config
from src.parsers.argument_parser import print_help


def main():
    arg_parser = ArgumentParser()
    args = sys.argv[1:]
    arg_parser.parse_args(args)

    if arg_parser.show_help:
        print_help()
        return

    config = load_config(arg_parser.config_path)
    calculator = Calculator(config)

    input_params = load_config(arg_parser.params_path)
    updated_config = calculator.update_config(**input_params)

    output_file = arg_parser.output_file
    if output_file == "stdout":
        print(updated_config)
    else:
        save_config(updated_config, output_file)


if __name__ == "__main__":
    main()
