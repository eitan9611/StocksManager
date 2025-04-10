import requests
from bs4 import BeautifulSoup
import StoreTxt


def extract_article_text(url):
    """Fetches and extracts the body of an article from Yahoo Finance."""
    headers = {"User-Agent": "Mozilla/5.0"}  # Avoid bot detection
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error: Unable to fetch URL ({response.status_code})")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Debugging: Print part of the HTML to inspect structure
    print(soup.prettify()[:500])  # Print first 500 characters of the HTML

    # Attempt to find the article body (trying different classes)
    article_body = soup.find("div", {"class": "caas-body"})
    if not article_body:
        article_body = soup.find("article")
        if not article_body:
            article_body = soup.find("div", {"class": "story-body"})

    if not article_body:
        print("❌ Error: Unable to find article content.")
        return None

    paragraphs = [p.get_text() for p in article_body.find_all("p")]
    return " ".join(paragraphs)  # Combine paragraphs into one long text


def store_article_from_url(url):
    """Fetches an article from Yahoo Finance, extracts text, and stores it in Qdrant."""
    article_text = extract_article_text(url)

    if article_text:
        print(f"✅ Extracted article: {article_text[:100]}...")  # Preview
        StoreTxt.store_text(article_text)  # Use your existing store_text function
    else:
        print("❌ Could not extract or store article.")


def store_articles_from_urls(url_list):
    """Takes a list of URLs, extracts their content, and stores each article in Qdrant."""
    for url in url_list:
        print(f"\nProcessing URL: {url}")
        store_article_from_url(url)


# 🔥 Example usage with a list of URLs
urls = [
    "https://finance.yahoo.com/news/why-pinterest-pins-stock-soaring-201406902.html",  # Replace with actual URLs
    "https://finance.yahoo.com/news/p-500-snapped-monthlong-losing-201342556.html",  # Replace with actual URLs
    "https://finance.yahoo.com/news/why-coherent-cohr-stock-soaring-200904975.html",  # Replace with actual URLs
    "https://finance.yahoo.com/news/why-unity-u-stock-today-200858735.html",
    "https://finance.yahoo.com/news/tesla-stock-surges-nearly-12-to-lead-magnificent-7-stocks-higher-as-tariff-worries-ease-200525384.html",
    "https://finance.yahoo.com/news/why-fedex-fdx-stock-rocketing-200406751.html",
    "https://finance.yahoo.com/news/market-action-shows-how-tariffs-remain-the-primary-catalyst-for-stocks-recovery-125026915.html"
]

store_articles_from_urls(urls)
