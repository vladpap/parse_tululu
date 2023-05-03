import requests
from pathlib import Path
from pprint import pprint


def save_book_in_file(book_text, file_name):
    Path("books").mkdir(parents=True, exist_ok=True)

    with open("books/{}".format(file_name), 'w') as file:
        file.write(book_text)


def main():
    url = "https://tululu.org/txt.php?id={}"

    for id_book in range(1, 11):
        response = requests.get(url.format(id_book))
        response.raise_for_status()
        save_book_in_file(response.text, "id_{}.txt".format(id_book))

    # file_name = response.headers["content-disposition"].split("=")[-1].strip('"')
    


if __name__ == "__main__":
    main()