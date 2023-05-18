import requests
from pathlib import Path
import os.path
import argparse
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse
from time import sleep
import logging


class TululuError(requests.RequestException):
    pass


class TululuNoTxtFile(requests.RequestException):
    pass


def check_for_redirect(response):
    if response.history:
        err_url = response.history[0].url
        err_code = response.history[0].status_code
        err_msg = f'Redirecting, no book\nurl: "{err_url}"'
        err_hrs = response.history[0].headers
        raise HTTPError(err_url, err_code, err_msg, err_hrs, None)


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    filename = sanitize_filename(filename)
    if not os.path.splitext(filename)[-1]:
        filename = f'{filename}.txt'

    file_path = f'{folder}{filename}'

    response = make_request(url)
    if not response:
        return

    check_for_redirect(response)

    book_text = response.text

    Path(folder).mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w') as file:
        file.write(book_text)

    return file_path


def save_image_from_url(url):
    image_path = 'images'
    Path(image_path).mkdir(parents=True, exist_ok=True)
    image_file_name = os.path.join(
        image_path,
        os.path.split(urlparse(url).path)[-1]
    )

    response = make_request(url)
    if not response:
        return

    with open(image_file_name, 'wb') as file:
        file.write(response.content)


def parse_book_page(html_book_page, url):
    soup = BeautifulSoup(html_book_page, 'lxml')

    book_comment_tags = soup.find(
        'div', id='content').find_all(
        'div', class_='texts'
        )
    book_comments = [book_comment_tag.find('span', class_='black').text
                     for book_comment_tag in book_comment_tags]

    book_genre_tags = soup.find(
        'div', id='content').find(
        'span', class_='d_book').find_all('a')
    book_genres = [book_genre_tag.text for book_genre_tag in book_genre_tags]

    book_img_shot_url = soup.find('div', id='content').find('img')['src']
    book_name_tag = soup.find('div', id='content').find('h1')
    book_name = book_name_tag.text.split('::')[0].strip()
    book_author = book_name_tag.text.split('::')[-1].strip()

    book_txt_short_url_tag = soup.find(
            'a', string='скачать txt')
    if not book_txt_short_url_tag:
        raise TululuNoTxtFile('No link download txt file.')

    book_txt_short_url = book_txt_short_url_tag.get('href')

    book = {
        'book_txt_url': urljoin(url, book_txt_short_url),
        'book_name': book_name,
        'book_author': book_author,
        'book_img_url': urljoin(url, book_img_shot_url),
        'book_comments': book_comments,
        'book_genres': book_genres,
    }
    return book


def make_request(url):
    connection_counts = 1
    wait_seconds = 10

    while True:
        try:
            response = requests.get(url, timeout=6)
            response.raise_for_status()
            return response
        except (
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout
                ):
            if connection_counts > 3:
                raise TululuError('No connection')
            sleep(wait_seconds * connection_counts)
            connection_counts += 1


def main():
    logging.basicConfig(
        filename='warning.log',
        format='%(asctime)s %(message)s',
        encoding='utf8',
        level=logging.WARNING)

    parser = argparse.ArgumentParser(
            description='Dowload book from https://tululu.org/')

    parser.add_argument(
        'start_id',
        help='Start id dowload , default=1',
        nargs='?',
        default=1,
        type=int)

    parser.add_argument(
        'end_id',
        help='END id dowload book, if not specified, then start_id + 10',
        nargs='?',
        type=int)

    parser.parse_args()

    parse_args = parser.parse_args()

    start_id = parse_args.start_id
    arg_end_id = parse_args.end_id

    end_id = (
        start_id + 10
    ) if (not arg_end_id) or (arg_end_id < start_id) else arg_end_id

    base_url = 'https://tululu.org/'
    path_url = 'b{}/'
    for book_id in range(start_id, end_id):
        book_url = urljoin(base_url, path_url.format(book_id))

        try:
            response = make_request(book_url)
        except TululuError as err:
            logging.warning(str(err))
            return
        try:
            check_for_redirect(response)
        except HTTPError:
            logging.warning(f'Книги с id: {book_id} на сайте нет.')
            continue

        try:
            book = parse_book_page(response.text, book_url)
        except TululuNoTxtFile:
            logging.warning(f'Для книги с id: {book_id} нет ссылки на txt.')
            continue

        book_txt_url = book['book_txt_url']
        book_name = book['book_name']
        book_img_url = book['book_img_url']
        try:
            download_txt(book_txt_url, book_name)
        except TululuError as err:
            logging.warning(
                f'No download book ({str(err)}), book url{book_txt_url}, title book{book_name}')
        try:
            save_image_from_url(book_img_url)
        except TululuError as err:
            logging.warning(
                f'No save cover book ({str(err)}), book image url{book_img_url}')


if __name__ == '__main__':
    main()
