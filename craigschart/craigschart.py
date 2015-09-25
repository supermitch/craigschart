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

    print('Pages:\n\n')
    mydivs = soup.findAll('a', {'class': 'hdrlnk'})
    for t in mydivs:
        print(t['href'])

    totalcount_span = soup.find('span', {'class': 'totalcount'})
    total_count = int(totalcount_span.string)
    print('Total result count: {}\n\n'.format(total_count))

    print('Buttons:')
    next_page = soup.findAll('a', {'class': 'button next'})
    for t in next_page:
        print(t['href'])

if __name__ == '__main__':
    main()

