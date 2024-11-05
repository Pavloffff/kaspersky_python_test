def snake_to_camel(snake_text: str) -> str:
    camel_text: str = ""
    under_flag: bool = False
    for idx, sym in enumerate(snake_text):
        if idx == 0 or under_flag:
            camel_text += sym.upper()
        elif sym.isalpha():
            camel_text += sym.lower()
        elif sym in ['-', '_']:
            under_flag = True
            continue
        under_flag = False

    return camel_text
