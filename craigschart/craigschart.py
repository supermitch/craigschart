import sys

from bs4 import BeautifulSoup
import requests


def get_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    else:
        print('Request returned status code {}'.format(r.status_code))
        return None


def add_start(url, start):
    parts = url.split('?')
    return parts[0] + '?s={}'.format(start) + '&' + parts[1]


def main():
    url = 'http://vancouver.craigslist.ca/search/cto?query=Expedition'
    html = get_html(url)

    if not html:
        sys.exit('No content. Please try again.')

    soup = BeautifulSoup(html, 'lxml')
    print(soup.prettify())

    all_links = []
    links = soup.findAll('a', {'class': 'hdrlnk'})
    for i, link in enumerate(links, start=1):
        print('{}. {}'.format(i, link['href']))
        all_links.append(link['href'])

    totalcount_span = soup.find('span', {'class': 'totalcount'})
    total_count = int(totalcount_span.string)
    print('Total result count: {}\n\n'.format(total_count))

    for start in range(100, total_count, 100):
        print('Querying records starting at {}'.format(start))

        query = add_start(url, start)
        html = get_html(query)
        soup = BeautifulSoup(html, 'lxml')

        print('Pages:\n\n')
        links = soup.findAll('a', {'class': 'hdrlnk'})
        for link in links:
            print(link['href'])
        all_links.append(links)

    print('Found {} results'.format(len(all_links)))


if __name__ == '__main__':
    main()

