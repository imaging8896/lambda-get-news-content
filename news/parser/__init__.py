from html.parser import HTMLParser


class NewsHTMLParser(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)

        self._content = ""

    @property
    def content(self) -> str:
        return self._content
