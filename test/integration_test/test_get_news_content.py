import random
import time

import pytest


from news import get_news_content


@pytest.mark.parametrize("url", [
    "https://www.ctee.com.tw/news/20241226701462-430702",
    "https://www.moneydj.com/KMDJ/News/NewsViewer.aspx?a=082db416-e70c-478e-a1d7-e3db7364ef20",
])
def test_get_news_content(url):
    content, _ = get_news_content(url)

    assert content
    time.sleep(random.uniform(1, 3))