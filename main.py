import traceback

from news import get_news_content


def handler(event: dict | None = None, context=None):
    try:
        if event is None:
            raise ValueError("Given None argument for lambda function")

        content, url = get_news_content(**event)
        return {
            "status": True,
            "result": {
                "content": content,
                "url": url,
            },
        }
    except Exception as e:
        return {
            "status": False,
            "result": {
                "exception_type": str(type(e)),
                "exception_message": str(e),
                "traceback" : traceback.format_exc(),
            },
        }        
