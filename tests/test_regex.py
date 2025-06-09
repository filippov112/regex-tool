import unittest
from main import find_regex_matches  # Импортируем функцию поиска по регулярному выражению

class TestRegexSearch(unittest.TestCase):
    # Проверка простого точного совпадения слова с границами
    def test_basic_match(self):
        text = "abc 123 abc456"
        pattern = r"\babc\b"
        result = find_regex_matches(pattern, text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "abc")
        self.assertEqual(result[0][1], 0)
        self.assertEqual(result[0][2], 3)

    # Проверка нескольких совпадений в строке
    def test_multiple_matches(self):
        text = "123 abc 789 abc"
        pattern = r"abc"
        result = find_regex_matches(pattern, text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], 4)
        self.assertEqual(result[1][1], 12)

    # Проверка отсутствия совпадений
    def test_no_match(self):
        text = "def ghi jkl"
        pattern = r"abc"
        result = find_regex_matches(pattern, text)
        self.assertEqual(result, [])

    # Проверка корректного выброса ошибки при некорректном паттерне
    def test_invalid_regex(self):
        text = "abc"
        pattern = r"abc("
        with self.assertRaises(ValueError):
            find_regex_matches(pattern, text)

    # Проверка поиска с использованием групп в паттерне
    def test_match_with_groups(self):
        text = "foo:123, bar:456"
        pattern = r"(\w+):(\d+)"
        result = find_regex_matches(pattern, text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], "foo:123")
        self.assertEqual(result[1][0], "bar:456")

    # Проверка многострочного режима — поиск по каждой строке
    def test_multiline_behavior(self):
        text = "start\nmiddle\nend"
        pattern = r"^.*$"
        result = find_regex_matches(pattern, text)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1][0], "middle")

    # Проверка поддержки Unicode (русские символы)
    def test_unicode_support(self):
        text = "Привет мир"
        pattern = r"\bмир\b"
        result = find_regex_matches(pattern, text)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], "мир")

    # Проверка поведения при пустом паттерне (совпадения между символами)
    def test_empty_pattern(self):
        text = "abc"
        pattern = ""
        result = find_regex_matches(pattern, text)
        # Пустой паттерн находит совпадения между каждым символом (и в начале, и в конце)
        self.assertEqual(len(result), len(text) + 1)

    # Проверка поведения при пустом тексте — совпадений нет
    def test_empty_text(self):
        text = ""
        pattern = r".+"
        result = find_regex_matches(pattern, text)
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()

