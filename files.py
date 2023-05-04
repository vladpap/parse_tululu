import requests
import os.path
from pathlib import Path
from pathvalidate import sanitize_filename


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

    book_text = response.text

    Path(folder).mkdir(parents=True, exist_ok=True)

    with open(file_path, 'w') as file:
        file.write(book_text)

    return file_path

if __name__ == '__main__':
    url = 'http://tululu.org/txt.php?id=1'

    filepath = download_txt(url, 'Алиби.py')
    print(filepath)  # Выведется books/Алиби.txt

    filepath = download_txt(url, 'Али/би', folder='books/')
    print(filepath)  # Выведется books/Алиби.txt

    filepath = download_txt(url, 'Али\\би', folder='txt/')
    print(filepath)  # Выведется txt/Алиби.txt
