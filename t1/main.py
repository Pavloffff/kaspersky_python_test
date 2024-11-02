from src.tag_processor import apply_tag_rules, AllowedTagRecord


if __name__ == '__main__':
    # пример таблицы правил
    rules = (
        # зарезервированный тег, менять нельзя
        AllowedTagRecord("SRS", immutable=True),
        AllowedTagRecord("web_engine"),
        # тег с известными синонимами
        AllowedTagRecord("sms", "сообщения, messages"),
        AllowedTagRecord("x86", "QEMU, кему"),
        # тег, при наличии в составе тега, нужно вывести в отдельный, есть
        # синоним
        AllowedTagRecord("svc", "Service", separated=True),
        AllowedTagRecord("contacts", "контакты"),
        AllowedTagRecord("display", "lcd, дисплей"),
        AllowedTagRecord("AUTO", immutable=True),
        AllowedTagRecord("lock_screen", "экран блокировки", separated=True),
    )

    for input_tags, expected_tags in (
            # тег WebEngine заменился на тег из правил web_engine
            # тег AUTO остался неизменным
            ("WebEngine; AUTO", "web_engine; AUTO"),
            # тег-синоним заменился на исходный
            ("экран блокировки; дисплэй", "lock_screen"),
            # тег-синоним заменился на исходный
            ("КеМу", "x86"),
            # тег разделился на два из-за наличия svc
            ("DisplaySvc", "display; svc"),
            # неизвестный тег, удаляем
            ("SomeTrashTag", ""),
            # нет тегов, ну и не надо
            ("", ""),
            # неизвестный тег удален, известный синоним заменен
            ("unknown-tag; lcd", "display"),
    ):
        assert apply_tag_rules(input_tags, rules) == expected_tags
