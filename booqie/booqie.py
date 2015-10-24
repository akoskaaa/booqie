
import requests
import sys

from bs4 import BeautifulSoup
from collections import namedtuple
from fuzzywuzzy import fuzz

def main():

    Book = namedtuple('Book', ['title', 'author', 'match_rate', 'price'])
    search_term = sys.argv[1]
    result_books = []

    # bookdepository
    url_template = 'http://www.bookdepository.com/search?searchTerm={search_term}&search=Find+book'
    response = requests.get(url_template.format(
        search_term=search_term
    ))
    soup = BeautifulSoup(response.text, 'lxml')
    raw_books = soup.select('div.book-item')

    for raw_book in raw_books:
        info = raw_book.select('.item-info')[0]
        title = info.select('h3.title a')[0].text.strip()
        author = info.select('p.author')[0].text.strip()
        match_rate = fuzz.ratio(search_term.lower(), title.lower())

        try:
            price = ' '.join(info.select('p.price')[0].text.encode('ascii', 'ignore').split()[:2])
        except IndexError:
            price = '????'

        result_books.append(Book(
            title=title,
            author=author,
            match_rate=match_rate,
            price=price
        ))

    # amazon.co.uk
    url_template = 'http://www.amazon.co.uk/s/ref=nb_sb_noss_2?url=search-alias%3Dstripbooks&field-keywords={search_term}'
    response = requests.get(url_template.format(
        search_term=search_term
    ))
    soup = BeautifulSoup(response.text, 'lxml')
    raw_books = soup.select('div.s-item-container')

    for raw_book in raw_books:
        title_select = raw_book.select('a.s-access-detail-page')
        if title_select:
            title = title_select[0].text
            price_base_select = raw_book.select('span.s-price') or raw_book.select('span.a-color-price')
            match_rate = fuzz.ratio(search_term.lower(), title.lower())

            try:
                author = raw_book.select('div.a-row.a-spacing-none')[0].select('span')[1].text
            except IndexError:
                author = '????'

            try:
                price = price_base_select[0].text
            except IndexError:
                price = '????'

            result_books.append(Book(
                title=title,
                author=author,
                match_rate=match_rate,
                price=price
            ))

    print result_books


if __name__ == '__main__':
    main()
