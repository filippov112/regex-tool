from main import apply_regex_substitution  # Импортируем функцию замены
import unittest

class TestRegexReplace(unittest.TestCase):
    # Простейшая замена по совпадению
    def test_basic_replace(self):
        text = "abc abc"
        pattern = r"abc"
        repl = "XYZ"
        result = apply_regex_substitution(pattern, repl, text)
        self.assertEqual(result, "XYZ XYZ")

    # Проверка подстановки с использованием групп
    def test_replace_with_groups(self):
        text = "name:John age:30"
        pattern = r"(\w+):(\w+)"
        repl = r"\1=\2"
        result = apply_regex_substitution(pattern, repl, text)
        self.assertEqual(result, "name=John age=30")

    # Проверка замены с привязкой к началу строки в многострочном тексте
    def test_multiline_replace(self):
        text = "line1\nline2"
        pattern = r"^line"
        repl = "row"
        result = apply_regex_substitution(pattern, repl, text)
        self.assertEqual(result, "row1\nrow2")

    # Проверка обработки ошибки при недопустимом регулярном выражении
    def test_invalid_pattern(self):
        text = "abc"
        pattern = r"[a-z"
        repl = "-"
        with self.assertRaises(ValueError):
            apply_regex_substitution(pattern, repl, text)

    # Замена в пустом тексте не должна ничего менять
    def test_empty_text(self):
        text = ""
        pattern = r".+"
        repl = "-"
        result = apply_regex_substitution(pattern, repl, text)
        self.assertEqual(result, "")

