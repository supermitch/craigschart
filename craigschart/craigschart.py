import collections
import sys

from bs4 import BeautifulSoup
import plotly.plotly as py
from plotly.graph_objs import *
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


def validate_results(results):
    validated = []
    for result in results:
        clean = {}
        for k, v in result.items():
            k, v = validate_attribute(k, v)
            clean[k] = v
        validated.append(clean)
    return validated


def query_listing(url):
    html = get_html(url)
    if not html:
        print('Listing has no content. Please try again.')
        return None

    soup = BeautifulSoup(html, 'lxml')
    price = soup.find('span', {'class': 'price'}).text[1:]  # Remove '$'
    result = {'price': float(price)}

    groups = soup.findAll('p', {'class': 'attrgroup'})
    spans = groups[1].findAll('span')
    result.update({span.text[:span.text.find(':')]: span.b.text for span in spans})
    return result


def graph(points):

    trace0 = Scatter(
        x=[x for x, _ in points],
        y=[y for _, y in points],
        mode='markers'
    )
    data = Data([trace0])
    plot_url = py.plot(data, filename='line-scatter')
    print(plot_url)
    return plot_url


def main():
    domain = 'http://vancouver.craigslist.ca/'
    link = 'search/cto?query=Expedition'

    all_links = query_search_results(domain + link)
    print('Found {} results'.format(len(all_links)))

    LIMIT = 8
    results = [query_listing(domain + link) for link in all_links[:LIMIT]]
    results = validate_results(results)
    print(results)

    # Plot price versus odometer
    points = []
    for result in results:
        odo = result.get('odometer', 0)
        price = result.get('price', 0)
        points.append((odo, price))  # (x, y) point
    points = sorted(points, key=lambda t: t[0])
    url = graph(points)
    print(url)


if __name__ == '__main__':
    main()

