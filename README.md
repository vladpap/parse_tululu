![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)


# Парсер книг с сайта tululu.org

Скрипт скачивает книги в текстовом формате и обложки к ни с ссайта [tululu.org](https://tululu.org/)

## Установка.
- Python3 должен быть уже установлен.
- Рекомендуется использовать среду окружения [venv](https://docs.python.org/3/library/venv.html) 
для изоляции проекта.
 - Используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей
```console
$ pip install -r requirements.txt
```

## Аргументы

Скрипт принимает до 2 аргументов:
 - если не заданы скачивает книги id c 1 по 10
 - если задан один аргумент, скачивает книги id с указанного по + 10
 - если заданы 2 аргумента, скачивает согласно указанным аргументам, причем 2-ой аргумент должен быть больше иначе скачивается как с 1 аргументом.

## Запуск

```bash
$ python parse_tululu.py
# скачает книги id  с 1 по 10

$ python parse_tululu.py 25
# скачает книги id  с 25 по 35

$ python parse_tululu.py 32 33
# скачает книги id  с 32 по 33

$ python parse_tululu.py 35 10
# скачает книги id  с 35 по 45


```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python [Devman](https://dvmn.org).


<img src="https://dvmn.org/assets/img/logo.8d8f24edbb5f.svg" alt= “” width="102" height="25">
