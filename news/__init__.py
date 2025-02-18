import requests
import random
import ssl
import contextlib

from requests.adapters import HTTPAdapter, Retry
from cloudscraper import CloudScraper

from .parser.general import GeneralNewsHTMLParser


def get_news_content(url: str, mobile: bool = True, desktop: bool = True):
    raw_content, news_url = get_news_raw_content(url, mobile=mobile, desktop=desktop)

    parser = GeneralNewsHTMLParser()

    parser.feed(raw_content)
    return parser.content, news_url


def get_news_raw_content(url: str, mobile: bool = True, desktop: bool = True):
    response = None
    
    try:
        response = get_news_raw_content_by_cloudscraper(url, mobile=mobile, desktop=desktop)
    except requests.exceptions.SSLError:
        with contextlib.suppress(requests.exceptions.SSLError):
            response = get_news_raw_content_by_cloudscraper(url, mobile=mobile, desktop=desktop, ssl_context=ssl.create_default_context())

    if mobile and desktop:
        try:
            if response is None or response.status_code == 403:
                response = get_news_raw_content_by_cloudscraper(url, mobile=False)
        except requests.exceptions.SSLError:
            with contextlib.suppress(requests.exceptions.SSLError):
                response = get_news_raw_content_by_cloudscraper(url, mobile=False, ssl_context=ssl.create_default_context())

        try:
            if response is None or response.status_code == 403:
                response = get_news_raw_content_by_cloudscraper(url, desktop=False)
        except requests.exceptions.SSLError:
            response = get_news_raw_content_by_cloudscraper(url, desktop=False, ssl_context=ssl.create_default_context())

    if response is not None:
        if response.status_code == 404:
            return "", url
        response.raise_for_status()
        return response.text, response.url
    raise RuntimeError("Code should not reach here. Response is None.")


def get_news_raw_content_by_cloudscraper(url: str, mobile: bool = True, desktop: bool = True, ssl_context: ssl.SSLContext = None):
    if ssl_context is not None:
        ssl_context.check_hostname = False

    if not mobile:
        platforms = ['linux', 'windows', 'darwin']

        scraper = CloudScraper(browser={"mobile": False, "platform": random.SystemRandom().choice(platforms)}, ssl_context=ssl_context)
    elif not desktop:
        scraper = CloudScraper(browser={"dessktop": False, "browser": "chrome"}, ssl_context=ssl_context)
    else:
        scraper = CloudScraper(ssl_context=ssl_context)

    scraper.mount(
        url, 
        HTTPAdapter(max_retries=Retry(total=5, backoff_factor=2.1)),
    )

    return scraper.get(url, verify=ssl_context is None)
