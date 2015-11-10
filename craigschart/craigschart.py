#!/usr/bin/env python

import argparse
import collections
import sys

from bs4 import BeautifulSoup
import requests

import graph


Listing = collections.namedtuple('Listing', 'id, url, cost, mileage, year')


def setup_args():
    parser = argparse.ArgumentParser(description='Graph Craigslist Results')
    parser.add_argument('-c', '--category', nargs='?', default='cto',
                        help='Category to search, e.g. cto')
    parser.add_argument('-t', '--terms', nargs='*', default='Ford Expedition',
                        help='Search terms, separated by spaces, e.g. Ford Expedition')
    args = parser.parse_args()
    if isinstance(args.terms, str):
        args.terms = [args.terms]  # Convert a single term to a list
    return args


def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    headers = {
        'User-Agent': user_agent
    }
    r = requests.get(url, headers=headers, timeout=5)
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
    print('LISTING HTML\n{}'.format(html))
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


def main():
    args = setup_args()

    print(args)
    domain = 'http://vancouver.craigslist.ca/'
    link = 'search/{}?query={}'.format(args.category, ' '.join(args.terms))
    query_url = domain + link
    print('Searching: {}'.format(query_url))


    all_links = query_search_results(query_url)
    print('Found {} results'.format(len(all_links)))

    LIMIT = 10
    print('All_links: {}'.format(all_links))
    results = [query_listing(domain + link) for link in all_links[:LIMIT]]
    results = validate_results(results)

    print('RESULTS\n-------\n{}'.format(results))

    # Plot price versus odometer
    points = []
    for result in results:
        odo = result.get('odometer', 0)
        price = result.get('price', 0)
        points.append((odo, price))  # (x, y) point
    points = sorted(points, key=lambda t: t[0])
    url = graph.graph(points, args.category, args.terms)
    print('Graph generated at: {}'.format(url))


if __name__ == '__main__':
    main()

