from bs4 import BeautifulSoup
import requests


def get_html(url):
    r = requests.get(url)
    return r.text


def add_start(url, start):
    parts = url.split('?')
    return parts[0] + '?s={}'.format(start) + '&' + parts[1]


def main():
    url = 'http://vancouver.craigslist.ca/search/cto?query=Expedition'
    html = get_html(url)

    soup = BeautifulSoup(html, 'lxml')
    print(soup.prettify())

    print('Pages:\n\n')
    links = soup.findAll('a', {'class': 'hdrlnk'})
    for link in links:
        print(link['href'])
    all_links = links

    totalcount_span = soup.find('span', {'class': 'totalcount'})
    total_count = int(totalcount_span.string)
    print('Total result count: {}\n\n'.format(total_count))

    for start in range(0, total_count, 100):
        print('Querying records {}'.format(start))
        if start == 0:  # first page already done
            continue
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

