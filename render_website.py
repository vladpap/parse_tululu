from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import os
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
    two_books = list(chunked(books, 2))
    page_books = list(chunked(two_books, 10))

    os.makedirs('pages', exist_ok=True)

    for page_number, two_book in enumerate(page_books, 1):
        template = env.get_template('template.html')
        rendered_page = template.render(
            books=two_book,
            )
        file_name = os.path.join(
            'pages',
            'index%s' % page_number + '.html')
        with open(file_name, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    rebuild()

    server = Server()

    server.watch('template.html', rebuild)

    server.serve(root='.')


if __name__ == '__main__':
    main()
