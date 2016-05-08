# coding: utf-8

"""A simple web crawler that is supposed to be extensive.

"""
import time
from urlparse import urlparse

from eventlet import Queue
import eventlet
import requests


eventlet.monkey_patch()


def get_netloc(url):
    return urlparse(url).netloc


class Crawler(object):
    """
    A crawler will traverse all the pages of a site and process the content
    in a defined way.

    :param init_urls: the very first urls to start with.
    :param q: the queue that stores all urls to be crawled
    :param urls: a set stores all urls already crawled
    """

    def __init__(self, init_urls, max_workers=200):
        self.init_urls = init_urls
        self.max_workers = max_workers
        self.q = Queue()
        self.urls = set()
        self.s = requests.Session()
        self.root_hosts = set()
        for url in init_urls:
            self.q.put(url)
            self.urls.add(url)
            self.root_hosts.add(get_netloc(url))

    def url_allowed(self, url):
        """Check if given url will be crawled.

        Current, only if the url belongs to the same host as init_urls.
        """
        return get_netloc(url) in self.root_hosts


    def save(self, response):
        """Save data at the given url."""
        raise NotImplementedError(
            "Please implement your own save logic in subclass.")

    def parse(self, response):
        self.save(response)

        new_links = set()

        for url in self.find_links(response):
            if url not in self.urls and self.url_allowed(url):
                new_links.add(url)
                self.urls.add(url)
                self.q.put(url)
        if len(new_links) != 0:
            print("Find %d new urls to crawl" % len(new_links))


    def fetch(self, url):
        """Fetch content of the url from network."""

        response = self.s.get(url)
        print("Getting content from %s, length: %d" % (url,
                                                       len(response.content)))
        return response

    def work(self, i):
        """Define the work process.

        Retrieve a url from queue, fetch the content from it,
        process it and get new urls to crawl.
        Continue the process until all pages are crawled.

        :param i: indicate the worker number
        """
        while True:
            url = self.q.get()
            print("Worker %d: Getting url %s from queue." % (i, url))
            response = self.fetch(url)
            self.parse(response)
            self.q.task_done()

    def run(self):
        """Start the crawling process.

        This is the main entrance for our crawler. It will start several
        workers, crawling in parallel.
        """
        pool = eventlet.GreenPool()
        start = time.time()
        for i in range(self.max_workers):
            pool.spawn(self.work, i)

        self.q.join()
        end = time.time()

        print("Finished crawling, takes %s seconds." % str(end - start))
        print("Have fun hacking!")