import requests
from pathlib import Path
import os.path
from pprint import pprint
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urlparse, urljoin, urlsplit


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


def get_book_link_and_name(url):
    response = requests.get(url)
    response.raise_for_status()

    check_for_redirect(response)

    soup = BeautifulSoup(response.text, 'lxml')
    
    book_name_tag = soup.find('div', id='content').find('h1')
    book_name = book_name_tag.text.split(':')[0].strip()
    author_name = book_name_tag.text.split(':')[-1].strip()
    try:
        book_urlpath = soup.find_all('a', string='скачать txt')[0].get('href')
    except IndexError:
        return None

    url_components = urlsplit(url)
    book_url_components = url_components._replace(path=book_urlpath)
    book_txt_url = book_url_components.geturl()

    return (book_txt_url, book_name)


def main():
    url = 'https://tululu.org/b{}/'
    for id_book in range(1, 11):
        try:
            book_link_and_name = get_book_link_and_name(url.format(id_book))
            if book_link_and_name:
                download_txt(book_link_and_name[0], book_link_and_name[1])
        except HTTPError as e:
            print(e)
            continue


if __name__ == '__main__':
    main()