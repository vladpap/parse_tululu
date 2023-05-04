import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
    response = requests.get(url)
    response.raise_for_status()

    received_text = response.text

    soup = BeautifulSoup(received_text, 'lxml')
    print(soup.find('main').find('header').find('h1').text)
    print(soup.find('main').find('img', class_='attachment-post-image')['src'])
    print(soup.find('main').find('div', class_='entry-content').text)
if __name__ == '__main__':
    main()