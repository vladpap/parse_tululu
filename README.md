
## Сайт библиотеки
[Личная библиотека](https://vladpap.github.io/parse_tululu/)

## Установка.
- Python3 должен быть уже установлен.
- Рекомендуется использовать среду окружения [venv](https://docs.python.org/3/library/venv.html) 
для изоляции проекта.
 - Используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей
```console
$ pip install -r requirements.txt
```

## Изменить имя файла базы библиотеки.

Создать в корне файл ```.env``` с переменной BASE_FILE_NAME

```console
BASE_FILE_NAME=books.json
```

## Запуск

```bash
$ python3 render_website.py
```

[Открыть библиотеку](http://127.0.0.1:5500/)

## Чтение библиотеки оффлайн

1. Скачать проект
```bash
$ git clone https://github.com/vladpap/parse_tululu.git
```
или скачать zip файл проекта

![download zip from github](https://github.com/vladpap/parse_tululu/raw/main/for_readme/download_progect_zip.png)

2. Если скачивали zip проекта - распаковать архив.

3. Зайти в папку ```parse_tululu```

4. Открыть браузером файл ```index.html```




## Скрипты для скачивания книг
[Scripts](https://github.com/vladpap/parse_tululu/tree/main/scripts)

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python [Devman](https://dvmn.org).


<img src="https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg" alt= “” width="102" height="25">
