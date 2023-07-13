![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


# Скрипт скачивания книг с сайта tululu.org

Скрипт скачивает книги в текстовом формате и обложки к ним с ссайта [tululu.org](https://tululu.org/).

Все ошибки логируются в файл `warning.log`.

## Установка.
- Python3 должен быть уже установлен.
- Рекомендуется использовать среду окружения [venv](https://docs.python.org/3/library/venv.html) 
для изоляции проекта.
 - Используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей
```console
$ pip install -r requirements.txt
```

## Запуск

```bash
$ python3 parse_tululu_category.py
```

## Аргументы

```bash
$ python3 python3 parse_tululu_category.py -h

usage: parse_tululu_category.py [-h] [-s] [-e] [-i] [-t] [-f] [-j]

Dowload books from category https://tululu.org/

options:
  -h, --help           show this help message and exit
  -s , --start_page    Start page dowload , default=1
  -e , --end_page      END page dowload, if not specified, then start_page + 10
  -i, --skip_imgs      Specify do not download images, default=False
  -t, --skip_txt       Specify do not download text book, default=False
  -f , --dest_folder   Path to the directory with parsing results: pictures, books, JSON
  -j , --json_path     Specify the name to *.json file with results
```

## Сайт библиотеки
[Личная библиотека](https://vladpap.github.io/parse_tululu/)

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python [Devman](https://dvmn.org).


<img src="https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg" alt= “” width="102" height="25">
