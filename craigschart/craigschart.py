from bs4 import BeautifulSoup
import requests

def get_html():
    r = requests.get('http://vancouver.craigslist.ca/search/cto?query=Expedition')
    print(r.status_code)
    print(r.text)
    return r.text

def main():
    html = get_html()

    soup = BeautifulSoup(html, 'lxml')
    print(soup.prettify())
    mydivs = soup.findAll('a', {'class': 'hdrlnk'})
    for t in mydivs:
        print(t)

    print('Hello, World.')

if __name__ == '__main__':
    main()

