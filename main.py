import requests
from pathlib import Path
from pprint import pprint
from urllib.error import HTTPError


def check_for_redirect(response):
    if response.history:
        # print("Exception")
        err_url = response.history[0].url
        err_code = response.history[0].status_code
        err_msg = f"Redirecting, no book\nurl: '{err_url}'"
        err_hrs = response.history[0].headers
        raise HTTPError(err_url, err_code, err_msg, err_hrs, None)


def save_book_in_file(book_text, file_name):
    Path("books").mkdir(parents=True, exist_ok=True)

    with open("books/{}".format(file_name), 'w') as file:
        file.write(book_text)


def main():
    url = "https://tululu.org/txt.php?id={}"

    for id_book in range(1, 11):
        url = "https://tululu.org/txt.php?id={}".format(id_book)
        response = requests.get(url)
        response.raise_for_status()

        try:
            check_for_redirect(response)
        except HTTPError as e:
            print(e)
            continue

        save_book_in_file(response.text, "id_{}.txt".format(id_book))

    # file_name = response.headers["content-disposition"].split("=")[-1].strip('"')
    


if __name__ == "__main__":
    main()