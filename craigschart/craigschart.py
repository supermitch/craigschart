import collections
import sys

from bs4 import BeautifulSoup
import requests


Listing = collections.namedtuple('Listing', 'id, url, cost, mileage, year')


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


def query_search_results(url):
    html = get_html(url)
    if not html:
        sys.exit('No content. Please try again.')

    soup = BeautifulSoup(html, 'lxml')
    #A print(soup.prettify())

    all_links = []
    links = soup.findAll('a', {'class': 'hdrlnk'})
    for i, link in enumerate(links, start=1):
        all_links.append(link['href'])

    totalcount_span = soup.find('span', {'class': 'totalcount'})
    total_count = int(totalcount_span.string)
    print('Total result count: {}\n\n'.format(total_count))

    for start in range(100, total_count, 100):
        print('Querying records starting at {}'.format(start))

        query = add_start(url, start)
        html = get_html(query)
        soup = BeautifulSoup(html, 'lxml')

        links = soup.findAll('a', {'class': 'hdrlnk'})
        for link in links:
            all_links.append(link['href'])

    return all_links


def validate_attribute(label, value):
    if label == 'odometer':
        try:
            return label, int(value)
        except (TypeError, ValueError):  # None or bad odometer
            logging.info('Validation error: odometer value is {}'.format(value))
            return label, 1
    return label, value


def query_listing(url):
    html = get_html(url)
    if not html:
        print('Listing has no content. Please try again.')
        return None

    soup = BeautifulSoup(html, 'lxml')
    price = soup.find('span', {'class': 'price'}).text[1:]  # Remove '$'
    result = {'price': float(price)}

    groups = soup.findAll('p', {'class': 'attrgroup'})
    attribs = groups[1].findAll('span')
    for attrib in attribs:
        label = attrib.text[:attrib.text.find(':')].lower()  # Attrib, e.g. 'condition'
        value = attrib.b.text.lower()  # e.g. 'good'
        label, value = validate_attribute(label, value)  # TODO: Do this elsewhere
        result[label] = value  # Add to our dictionary
    return result


def main():
    domain = 'http://vancouver.craigslist.ca/'
    link = 'search/cto?query=Expedition'

    all_links = query_search_results(domain + link)
    print('Found {} results'.format(len(all_links)))

    LIMIT = 8
    results = [query_listing(domain + link) for link in all_links[:LIMIT]]
    print(results)


if __name__ == '__main__':
    main()

