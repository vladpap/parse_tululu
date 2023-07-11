from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server
from more_itertools import chunked


def load_books():
    with open("books.json", "r") as f:
        books_json = f.read()

    return json.loads(books_json)


def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    books = load_books()

    template = env.get_template('template.html')
    rendered_page = template.render(
        books=list(chunked(books, 2)),
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    rebuild()

    server = Server()

    server.watch('template.html', rebuild)

    server.serve(root='.')


if __name__ == '__main__':
    main()
