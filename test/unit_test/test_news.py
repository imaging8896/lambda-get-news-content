from unittest.mock import patch
from news import get_news_content


def test_get_news_content():
    with (
        patch("news.get_news_raw_content") as mock_get_news_raw_content,
        patch("news.GeneralNewsHTMLParser") as mock_GeneralNewsHTMLParser,
    ):
        mock_get_news_raw_content.return_value = "raw_content", "url"
        content, news_url = get_news_content("url")
        
        mock_GeneralNewsHTMLParser.assert_called_once_with()
        mock_GeneralNewsHTMLParser().feed.assert_called_once_with("raw_content")
        
        assert content == mock_GeneralNewsHTMLParser().content
        assert news_url == "url"
    
