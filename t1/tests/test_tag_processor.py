import unittest
from src.tag_processor import apply_tag_rules, AllowedTagRecord


class TestTagProcessor(unittest.TestCase):
    def setUp(self):
        self.rules = (
            AllowedTagRecord("SRS", immutable=True),
            AllowedTagRecord("web_engine"),
            AllowedTagRecord("sms", "сообщения, messages"),
            AllowedTagRecord("x86", "QEMU, кему"),
            AllowedTagRecord("svc", "Service", separated=True),
            AllowedTagRecord("contacts", "контакты"),
            AllowedTagRecord("display", "lcd, дисплей"),
            AllowedTagRecord("AUTO", immutable=True),
            AllowedTagRecord("lock_screen", "экран блокировки", separated=True),
        )

    def test_apply_tag_rules(self):
        test_cases = [
            ("WebEngine; AUTO", "web_engine; AUTO"),
            ("экран блокировки; дисплэй", "lock_screen"),
            ("КеМу", "x86"),
            ("DisplaySvc", "display; svc"),
            ("SomeTrashTag", ""),
            ("", ""),
            ("unknown-tag; lcd", "display"),
        ]
        for input_tags, expected_tags in test_cases:
            with self.subTest(input_tags=input_tags):
                result = apply_tag_rules(input_tags, self.rules)
                self.assertEqual(result, expected_tags)


if __name__ == '__main__':
    unittest.main()
