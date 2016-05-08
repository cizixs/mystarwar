# coding: utf-8

import importlib
from urlparse import urlparse

from crawler import Crawler



def is_link(ustr):
    return ustr.startswith('http')


def find_links(obj):
    """Find links in json-compatible data."""
    if isinstance(obj, dict):
        for key, value in obj.iteritems():
            for url in find_links(value):
                yield url
    elif isinstance(obj, list):
        for item in obj:
            for url in find_links(item):
                yield url
    else:
        try:
            if is_link(str(obj)):
                yield obj
        except Exception:
            pass


def _load_driver(backend, **kargs):
    """Load the correct backend driver for data persistent."""
    bk_module = importlib.import_module('backend', __package__)
    driver_cls = getattr(bk_module, str.capitalize(backend) + 'Backend')
    return driver_cls(**kargs)


class StarwarCrawler(Crawler):
    def __init__(self, init_urls, backend='json', **kargs):
        super(StarwarCrawler, self).__init__(init_urls)
        self.backend = _load_driver(backend, **kargs)

    @staticmethod
    def _get_table_name(url):
        """Get the table name to save data from the url.

        A typical url would be `http://swapi.co/api/films/7/`,
        ignore base url `http://swapi.co/api/` and other unknown urls
        """
        try:
            return urlparse(url).path.strip('/').split('/')[1]
        except IndexError:
            return None

    @staticmethod
    def item_url(url):
        """Check if this url contains an item detail."""
        return all(map(lambda x: str.isdigit(x), str(url.strip('/').split('/')[-1])))


    def save(self, response):
        """Save data from response to backend persistent driver.

        Only save the detail item from a url, filter out the overall items like
        `http://swapi.co/api/films/`
        """
        url = response.url
        if self.item_url(url):
            table_name = self._get_table_name(url)
            if table_name:
                data = response.json()
                self.backend.save(table_name, data)

    @staticmethod
    def find_links(response):
        for url in find_links(response.json()):
            yield url