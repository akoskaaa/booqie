from .provider_base import ProviderBase
from cached_property import cached_property
from fuzzywuzzy import fuzz


class ProviderBookDepository(ProviderBase):

    @cached_property
    def books(self):
        result_books = []
        for raw_book in self.raw_books:
            info = raw_book.select('.item-info')[0]
            title = info.select('h3.title a')[0].text.strip()
            author = info.select('p.author')[0].text.strip()
            match_rate = fuzz.ratio(self.search_term.lower(), title.lower())

            try:
                price = '{0:.2f}'.format(float(info.select('p.price')[0].text.encode('ascii', 'ignore').split()[0]))
            except IndexError:
                price = '????'

            result_books.append({
                'title': title,
                'author': author,
                'match_rate': match_rate,
                'price': price
            })
        return result_books
