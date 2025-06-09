import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu
import re


class RegexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Regex Tool")
        root.iconbitmap("icon.ico")  # Установка иконки приложения
        
        # Создаем верхнюю панель с полями для ввода и кнопками
        self.create_top_panel()
        # Создаем две области для ввода и вывода текста
        self.create_text_areas()
        # Создаем нижнюю панель для отображения найденных фрагментов
        self.create_bottom_panel()
        # Создаем меню справки
        self.create_menu()

        # Привязываем стандартные горячие клавиши копирования/вставки/вырезания/выделения к виджетам
        self.bind_copy_paste(self.regex_entry)
        self.bind_copy_paste(self.replace_entry)
        self.bind_copy_paste(self.input_text)
        self.bind_copy_paste(self.output_text)
        self.bind_copy_paste(self.results_text)

    def bind_copy_paste(self, widget):
        """
        Добавляет стандартные горячие клавиши (Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+A)
        для Entry и Text виджетов tkinter.
        """
        widget_class = widget.winfo_class()

        if widget_class == 'Entry':
            widget.bind_class("Entry", "<Control-c>", lambda e: (e.widget.event_generate("<<Copy>>"), "break"))
            widget.bind_class("Entry", "<Control-v>", lambda e: (e.widget.event_generate("<<Paste>>"), "break"))
            widget.bind_class("Entry", "<Control-x>", lambda e: (e.widget.event_generate("<<Cut>>"), "break"))
            widget.bind_class("Entry", "<Control-a>", lambda e: (e.widget.select_range(0, 'end'), "break"))

        elif widget_class == 'Text':
            widget.bind_class("Text", "<Control-c>", lambda e: (e.widget.event_generate("<<Copy>>"), "break"))
            widget.bind_class("Text", "<Control-v>", lambda e: (e.widget.event_generate("<<Paste>>"), "break"))
            widget.bind_class("Text", "<Control-x>", lambda e: (e.widget.event_generate("<<Cut>>"), "break"))
            widget.bind_class("Text", "<Control-a>", lambda e: (e.widget.tag_add("sel", "1.0", "end"), "break"))

    def create_top_panel(self):
        """
        Создает верхнюю панель с полями для ввода регулярного выражения,
        замещающего текста и кнопками "Поиск" и "Замена".
        """
        top_frame = tk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Label(top_frame, text="Регулярное выражение:").grid(row=0, column=0, sticky=tk.W)
        self.regex_entry = tk.Entry(top_frame, width=40)
        self.regex_entry.grid(row=0, column=1, padx=5, sticky=tk.W)

        tk.Label(top_frame, text="Замещающий текст:").grid(row=1, column=0, sticky=tk.W)
        self.replace_entry = tk.Entry(top_frame, width=40)
        self.replace_entry.grid(row=1, column=1, padx=5, sticky=tk.W)

        self.search_btn = tk.Button(top_frame, text="Поиск", command=self.on_search)
        self.search_btn.grid(row=0, column=2, padx=5)

        self.replace_btn = tk.Button(top_frame, text="Замена", command=self.on_replace)
        self.replace_btn.grid(row=1, column=2, padx=5)

    def create_text_areas(self):
        """
        Создает области ввода исходного текста (слева)
        и вывода результата (справа), обе с прокруткой.
        """
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.input_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=40, height=20)
        self.input_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, width=40, height=20)
        self.output_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_bottom_panel(self):
        """
        Создает нижнюю панель для вывода списка найденных совпадений.
        """
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

        tk.Label(bottom_frame, text="Найденные фрагменты:").pack(anchor=tk.W)
        self.results_text = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, height=5)
        self.results_text.pack(fill=tk.BOTH, expand=True)

    def create_menu(self):
        """
        Создает меню с пунктом справки, открывающим отдельное окно с текстом.
        """
        menubar = Menu(self.root)

        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Справка по регулярным выражениям", command=self.show_regex_help)
        menubar.add_cascade(label="?", menu=helpmenu)

        self.root.config(menu=menubar)

    def on_search(self):
        """
        Обработчик кнопки "Поиск".
        Выполняет поиск совпадений по регулярному выражению,
        подсвечивает их в правом окне вывода
        и выводит список найденных фрагментов в нижнем поле.
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.results_text.delete("1.0", tk.END)

        input_content = self.input_text.get("1.0", tk.END)
        pattern = self.regex_entry.get()

        try:
            matches = find_regex_matches(pattern, input_content)
        except ValueError as e:
            messagebox.showerror("Ошибка регулярного выражения", str(e))
            return

        self.output_text.insert("1.0", input_content)
        self.output_text.tag_remove("highlight", "1.0", tk.END)
        self.output_text.tag_config("highlight", background="yellow")

        self.results_text.insert(tk.END, f"Найдено совпадений: {len(matches)}\n")
        for group, start, end in matches:
            start_index = f"1.0 + {start} chars"
            end_index = f"1.0 + {end} chars"
            # Подсветка найденных фрагментов в тексте
            self.output_text.tag_add("highlight", start_index, end_index)
            self.results_text.insert(tk.END, f"{group}\n")

        self.output_text.config(state=tk.DISABLED)

    def on_replace(self):
        """
        Обработчик кнопки "Замена".
        Выполняет замену всех совпадений регулярного выражения на заданный текст,
        выводит результат в правом окне.
        """
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        input_content = self.input_text.get("1.0", tk.END)
        pattern = self.regex_entry.get()
        replacement = self.replace_entry.get()

        try:
            replaced_text = apply_regex_substitution(pattern, replacement, input_content)
        except re.error as e:
            messagebox.showerror("Ошибка регулярного выражения", str(e))
            return

        self.output_text.insert("1.0", replaced_text)
        self.output_text.config(state=tk.DISABLED)

    def show_regex_help(self):
        """
        Открывает новое окно со справочным текстом по регулярным выражениям,
        загруженным из файла regex_help.txt.
        """
        try:
            with open("regex_help.txt", encoding="utf-8") as f:
                help_text = f.read()
        except FileNotFoundError:
            help_text = "Файл справки не найден."

        help_window = tk.Toplevel(self.root)
        help_window.title("Справка по регулярным выражениям")

        text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, width=60, height=20)
        text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text.insert(tk.INSERT, help_text)
        text.config(state=tk.DISABLED)


def find_regex_matches(pattern: str, text: str):
    """
    Ищет все совпадения регулярного выражения в тексте с режимом MULTILINE.
    Возвращает список кортежей (совпадение, старт, конец).
    При ошибке регулярного выражения выбрасывает ValueError.
    """
    try:
        matches = list(re.finditer(pattern, text, re.MULTILINE))
        return [(m.group(), m.start(), m.end()) for m in matches]
    except re.error as e:
        raise ValueError(f"Ошибка регулярного выражения: {e}")


def apply_regex_substitution(pattern: str, replacement: str, text: str) -> str:
    """
    Выполняет замену всех совпадений регулярного выражения на replacement.
    Возвращает полученный текст.
    При ошибке регулярного выражения выбрасывает ValueError.
    """
    try:
        return re.sub(pattern, replacement, text, flags=re.MULTILINE)
    except re.error as e:
        raise ValueError(f"Ошибка регулярного выражения: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RegexApp(root)
    root.geometry("800x600")  # Размер окна
    root.mainloop()
