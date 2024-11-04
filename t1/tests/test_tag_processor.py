import unittest
from src.processors import apply_tag_rules, AllowedTagRecord


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

    def run_test_cases(self, test_cases):
        for input_tags, expected_tags in test_cases:
            with self.subTest(input_tags=input_tags):
                result = apply_tag_rules(input_tags, self.rules)
                self.assertEqual(result, expected_tags)

    def test_common_cases(self):
        """Тестирование тегов из задания"""
        test_cases = [
            ("WebEngine; AUTO", "web_engine; AUTO"),
            ("экран блокировки; дисплэй", "lock_screen"),
            ("КеМу", "x86"),
            ("DisplaySvc", "display; svc"),
            ("SomeTrashTag", ""),
            ("", ""),
            ("unknown-tag; lcd", "display"),
        ]
        self.run_test_cases(test_cases)

    def test_separated_tags(self):
        """Тестирование тегов с флагом separated=True."""
        test_cases = [
            ("DisplaySvc", "display; svc"),
            ("DisplayServiceContacts", "display; svc; contacts"),
            ("svcdisplay", "svc; display"),
            ("ServiceDisplay", "svc; display"),
            ("экранблокировки", "lock_screen"),
            ("экран блокировкидисплей", "lock_screen; display"),
            ("svcdisplaycontacts", "svc; display; contacts"),
        ]
        self.run_test_cases(test_cases)

    def test_synonyms(self):
        """Тестирование тегов-синонимов."""
        test_cases = [
            ("сообщения; messages; SMS", "sms"),
            ("контакты", "contacts"),
            ("lcd; дисплей", "display"),
            ("QEMU", "x86"),
            ("кему", "x86"),
            ("экран блокировки", "lock_screen"),
            ("дисплэй", ""),
        ]
        self.run_test_cases(test_cases)

    def test_unknown_tags(self):
        """Тестирование неизвестных тегов."""
        test_cases = [
            ("unknown-tag; _-_", ""),
            ("", ""),
            ("!!!", ""),
            (" ; ", ""),
            ("12345", ""),
        ]
        self.run_test_cases(test_cases)

    def test_mixed_tags(self):
        """Тестирование смешанных случаев."""
        test_cases = [
            ("WebEngine; AUTO; unknown", "web_engine; AUTO"),
            ("SRS; unknown-tag; lcd", "SRS; display"),
            ("AU_TO", ""),
            ("экран блокировки; SomeTrashTag", "lock_screen"),
            ("contacts; unknown; svc", "contacts; svc"),
        ]
        self.run_test_cases(test_cases)


if __name__ == '__main__':
    unittest.main()
