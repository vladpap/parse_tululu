import requests
from pathlib import Path
import os.path
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse


def check_for_redirect(response):
    if response.history:
        # print("Exception")
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
        filename += '.txt'
    file_path = (folder + filename)

    response = requests.get(url)
    response.raise_for_status()

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

    response = requests.get(url)
    response.raise_for_status()

    with open(image_file_name, 'wb') as file:
        file.write(response.content)


def parse_book_page(html_book_page):
    soup = BeautifulSoup(html_book_page, 'lxml')

    book_comment_tags = soup.find(
        'div', id='content').find_all(
        'div', class_='texts'
        )
    book_comments = []
    for book_comment_tag in book_comment_tags:
        book_comments.append(
            book_comment_tag.find('span', class_='black').text
        )

    book_genre_tags = soup.find(
        'div', id='content').find(
        'span', class_='d_book').find_all('a')
    book_genres = []
    for book_genre_tag in book_genre_tags:
        book_genres.append(book_genre_tag.text)

    book_img_shot_url = soup.find('div', id='content').find('img')['src']
    book_name_tag = soup.find('div', id='content').find('h1')
    book_name = book_name_tag.text.split('::')[0].strip()
    book_author = book_name_tag.text.split('::')[-1].strip()

    try:
        book_txt_short_url = soup.find_all(
            'a', string='скачать txt')[0].get('href')
    except IndexError:
        return None

    book_page_metadata = {
        'book_txt_short_url': book_txt_short_url,
        'book_name': book_name,
        'book_author': book_author,
        'book_img_shot_url': book_img_shot_url,
        'book_comments': book_comments,
        'book_genres': book_genres,
    }
    return book_page_metadata


def main():
    base_url = 'https://tululu.org/'
    path_url = 'b{}/'
    for id_book in range(1, 11):
        book_url = urljoin(base_url, path_url.format(id_book))
        response = requests.get(book_url)
        response.raise_for_status()

        try:
            check_for_redirect(response)
        except HTTPError:
            continue

        book_page_metadata = parse_book_page(response.text)

        if book_page_metadata:
            book_txt_url = urljoin(
                base_url,
                book_page_metadata['book_txt_short_url']
            )
            book_name = book_page_metadata['book_name']
            book_img_url = urljoin(
                base_url,
                book_page_metadata['book_img_shot_url']
            )
            # book_comments = book_page_metadata['book_comments']
            # book_genres = book_page_metadata['book_genres']
            # book_author = book_page_metadata['book_author']
            download_txt(book_txt_url, book_name)
            save_image_from_url(book_img_url)
        continue


if __name__ == '__main__':
    main()
