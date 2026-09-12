from newspaper import Article
from app.utils import clean_text


def extract_article(url: str):
    """
    Extract news content from a URL.
    """

    try:
        article = Article(url)

        # Download webpage
        article.download()

        # Parse content
        article.parse()

        title = article.title
        text = article.text
        authors = article.authors
        publish_date = article.publish_date


        return {
            "title": title,
            "text": clean_text(text),
            "authors": authors,
            "publish_date": str(publish_date)
            if publish_date
            else None
        }


    except Exception as error:

        return {
            "error": str(error)
        }