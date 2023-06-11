import requests
from bs4 import BeautifulSoup
import logging
import argparse
from urllib.parse import urljoin
import json
import os.path
from parse_tululu import (
    make_request,
    check_for_redirect,
    parse_book_page,
    download_txt,
    save_image_from_url,
    TululuError,
    TululuConnectionError)
from tqdm import tqdm


def create_argparse():
    parser = argparse.ArgumentParser(
            description='Dowload books from category https://tululu.org/')

    parser.add_argument(
        '-s',
        '--start_page',
        help='Start page dowload , default=1',
        metavar='',
        default=1,
        type=int)

    parser.add_argument(
        '-e',
        '--end_page',
        help='END page dowload, if not specified, then start_page + 10',
        metavar='',
        type=int)

    parser.add_argument(
        '-i',
        '--skip_imgs',
        help='Specify do not download images, default=False',
        default=False,
        action='store_true')

    parser.add_argument(
        '-t',
        '--skip_txt',
        help='Specify do not download text book, default=False',
        default=False,
        action='store_true')

    parser.add_argument(
        '-f',
        '--dest_folder',
        help='Path to the directory with parsing results: '
             'pictures, books, JSON',
        metavar='',
        default='.')

    parser.add_argument(
        '-j',
        '--json_path',
        help='Specify the name to *.json file with results',
        metavar='',
        default='books.json')

    return parser


def parse_category_page(html_category_page, html_url):
    soup = BeautifulSoup(html_category_page, 'lxml')
    books_url = []

    for book_tag in soup.select('table.d_book'):
        book_short_url = book_tag.select('a')[1].get('href')
        book_url = urljoin(html_url, book_short_url)
        books_url.append(book_url)

    return books_url


def save_book_annotations(filename, book_annotations):
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

    arguments = create_argparse().parse_args()

    category_url = 'https://tululu.org/l55/{}/'
    books_url = []
    start_page = arguments.start_page
    end_page = arguments.end_page
    if not end_page:
        end_page = start_page + 10
    elif end_page <= start_page:
        end_page = start_page + 1

    skip_download_images = arguments.skip_imgs
    skip_download_text = arguments.skip_txt
    destination_folder = arguments.dest_folder
    books_folder = '{}/books/'.format(destination_folder)
    images_folder = '{}/images/'.format(destination_folder)
    json_path = '{}/{}'.format(destination_folder, arguments.json_path)

    print('Parse pagas from category...')
    for number_page in tqdm(range(start_page, end_page)):
        try:
            response = make_request(category_url.format(number_page))
            check_for_redirect(response)
        except TululuError as err:
            logging.warning(str(err))
            return

        books_url.extend(parse_category_page(response.text, response.url))

    if skip_download_text and skip_download_images:
        print('No download txt and images')
        return

    book_annotations = []
    print('Download books...')
    for book_url in tqdm(books_url):
        book_annotation = {}
        try:
            response = make_request(book_url)
            check_for_redirect(response)
            book = parse_book_page(response.text, book_url)
            book_txt_url = book['book_txt_url']
            book_name = book['book_name']
            book_img_url = book['book_img_url']

            if skip_download_text:
                book_path = ''
            else:
                book_path = download_txt(
                    book_txt_url,
                    book_name,
                    folder=books_folder)

            if skip_download_images:
                img_scr = ''
            else:
                img_scr = save_image_from_url(
                    book_img_url,
                    folder=images_folder)

            book_annotation['title'] = book['book_name']
            book_annotation['author'] = book['book_author']
            book_annotation['img_scr'] = img_scr
            book_annotation['book_path'] = book_path
            book_annotation['comments'] = book['book_comments']
            book_annotation['genres'] = book['book_genres']
        except TululuConnectionError as err:
            logging.warning(str(err))
            return
        except TululuError as err:
            logging.warning(str(err))
        except requests.exceptions.HTTPError as err:
            logging.warning(str(err))

        if not skip_download_text and book_annotation:
            book_annotations.append(book_annotation)

    save_book_annotations(json_path, book_annotations)


if __name__ == '__main__':
    main()
