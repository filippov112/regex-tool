# regex-tool

## Описание

Приложение с графическим интерфейсом для поиска и замены текста с использованием регулярных выражений. Позволяет быстро находить совпадения в тексте, подсвечивать их, а также выполнять замены по заданным паттернам.

## Функционал

- Ввод текста для обработки и регулярного выражения для поиска.
- Подсветка найденных совпадений в исходном тексте.
- Отображение списка всех найденных фрагментов.
- Замена найденных совпадений на указанный пользователем текст.
- Поддержка многострочного текста и юникода.
- Меню справки с описанием синтаксиса регулярных выражений.
- Стандартные горячие клавиши для копирования, вставки и выделения текста.

## Технологии

- Python 3.x
- Tkinter — для создания графического интерфейса
- Модуль re — для работы с регулярными выражениями

## Установка и запуск

1. Клонировать репозиторий или скачать архив с проектом.
2. Убедиться, что установлен Python 3.
3. Установить зависимости из `requirements.txt` командой:
```

pip install -r requirements.txt

```
4. Запустить приложение командой:
```

python main.py

```

Для сборки исполняемого файла с помощью PyInstaller:
```

pyinstaller --onefile --noconsole --icon=icon.ico --add-data "icon.ico;." main.py

```

## Руководство пользователя

1. В поле «Регулярное выражение» ввести нужный паттерн для поиска.
2. В поле «Замещающий текст» указать текст, на который будут заменены найденные совпадения.
3. В левое большое окно вставить или ввести исходный текст.
4. Нажать кнопку «Поиск» для подсветки и отображения найденных совпадений.
5. Нажать кнопку «Замена» для применения замены и отображения результата в правом окне.
6. Для получения справки по регулярным выражениям нажать пункт меню «?» → «Справка по регулярным выражениям».
