from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import os.path
from parse_tululu import *
from tqdm import tqdm


def parse_category_page(html_category_page, html_url):
    soup = BeautifulSoup(html_category_page, 'lxml')
    books_url = []

    for book_tag in soup.select('table.d_book'):
        book_short_url = book_tag.select('a')[1].get('href')
        book_url = urljoin(html_url, book_short_url)
        books_url.append(book_url)

    return books_url


def save_book_annotations(book_annotations):
    filename = 'books.json'
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            book_file_annotations = json.load(file)
    else:
        book_file_annotations = []

    book_annotations_json = json.dumps(
        book_file_annotations + book_annotations,
        ensure_ascii=False)

    with open(filename, "w", encoding='utf8') as file:
        file.write(book_annotations_json)


def main():
    logging.basicConfig(
        filename='warning.log',
        format='%(asctime)s %(message)s',
        encoding='utf8',
        level=logging.WARNING)

    category_url = 'https://tululu.org/l55/{}/'
    books_url = []
    start_page = 1
    end_page = 2

    for number_page in tqdm(range(start_page, end_page)):
        response = make_request(category_url.format(number_page))

        try:
            check_for_redirect(response)
        except TululuError as err:
            logging.warning(str(err))

        books_url.extend(parse_category_page(response.text, response.url))

    book_annotations = []
    for book_url in tqdm(books_url):
        try:
            response = make_request(book_url)
            check_for_redirect(response)
            book = parse_book_page(response.text, book_url)
            book_txt_url = book['book_txt_url']
            book_name = book['book_name']
            book_img_url = book['book_img_url']
            book_path = download_txt(book_txt_url, book_name)
            img_scr = save_image_from_url(book_img_url)
        except TululuConnectionError as err:
            logging.warning(str(err))
            return
        except TululuError as err:
            logging.warning(str(err))
        except requests.exceptions.HTTPError as err:
            logging.warning(str(err))

        book_annotation = {}
        book_annotation['title'] = book['book_name']
        book_annotation['author'] = book['book_author']
        book_annotation['img_scr'] = img_scr
        book_annotation['book_path'] = book_path
        book_annotation['comments'] = book['book_comments']
        book_annotation['genres'] = book['book_genres']

        book_annotations.append(book_annotation)

    save_book_annotations(book_annotations)


if __name__ == '__main__':
    main()