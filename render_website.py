import json
import os

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked



def rebuild():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    #books = load_books()
    base_file_name = os.getenv('BASE_FILE_NAME', default='books.json')

    with open(base_file_name, "r") as base_file:
        books = json.load(base_file)

    page_books_column = list(chunked(books, 2))
    page_books = list(chunked(page_books_column, 10))

    os.makedirs('pages', exist_ok=True)

    for page_number, two_book in enumerate(page_books, 1):
        template = env.get_template('template.html')
        rendered_page = template.render(
            books=two_book,
            pages=len(page_books),
            current_page=page_number,

            )
        file_name = os.path.join(
            'pages',
            'index%s' % page_number + '.html')
        with open(file_name, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    load_dotenv()
    # base_file_name = os.getenv('BASE_FILE_NAME', default='books.json')

    # books = load_books(base_file_name)

    rebuild()

    server = Server()

    server.watch('template.html', rebuild)

    server.serve(root='.', default_filename='./pages/index1.html')


if __name__ == '__main__':
    main()
