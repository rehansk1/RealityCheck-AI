import re
from urllib.parse import urlparse

from app.scraper import extract_article


# =====================================================
# TRUSTED SOURCE PRIORITY
# =====================================================

TRUSTED_DOMAINS = {
    # Government / official
    "pib.gov.in": 100,
    "india.gov.in": 100,
    "mygov.in": 100,
    "education.gov.in": 100,
    "pmindia.gov.in": 100,

    # Major international news
    "reuters.com": 95,
    "apnews.com": 95,
    "bbc.com": 90,
    "bbc.co.uk": 90,

    # Major Indian news
    "thehindu.com": 90,
    "indianexpress.com": 90,
    "hindustantimes.com": 85,
    "timesofindia.indiatimes.com": 85,
    "economictimes.indiatimes.com": 85,
    "livemint.com": 85,
}


# =====================================================
# GET DOMAIN
# =====================================================

def get_domain(url: str) -> str:

    try:

        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:

        return ""


# =====================================================
# TRUST SCORE
# =====================================================

def get_trust_score(url: str) -> int:

    domain = get_domain(url)

    for trusted_domain, score in TRUSTED_DOMAINS.items():

        if (
            domain == trusted_domain
            or domain.endswith("." + trusted_domain)
        ):
            return score

    return 30


# =====================================================
# TEXT TOKENIZATION
# =====================================================

def tokenize(text: str):

    if not text:
        return set()

    words = re.findall(
        r"\b[a-zA-Z0-9]{3,}\b",
        text.lower()
    )

    # Remove common words
    stop_words = {
        "the",
        "and",
        "for",
        "that",
        "this",
        "with",
        "from",
        "has",
        "have",
        "been",
        "are",
        "was",
        "were",
        "will",
        "would",
        "about",
        "into",
        "their",
        "they",
        "them",
        "said",
        "after",
        "before",
        "over",
        "under",
        "india",
        "indian",
    }

    return {
        word
        for word in words
        if word not in stop_words
    }


# =====================================================
# RELEVANCE SCORE
# =====================================================

def calculate_relevance(
    claim: str,
    title: str,
    text: str = ""
) -> int:

    claim_words = tokenize(claim)

    article_words = tokenize(
        f"{title} {text}"
    )

    if not claim_words or not article_words:
        return 0

    matching_words = (
        claim_words & article_words
    )

    score = (
        len(matching_words)
        / len(claim_words)
    ) * 100

    return round(
        min(100, score)
    )


# =====================================================
# FINAL SOURCE SCORE
# =====================================================

def calculate_source_score(
    claim: str,
    title: str,
    text: str,
    url: str
):

    relevance = calculate_relevance(
        claim,
        title,
        text
    )

    trust = get_trust_score(url)

    # Relevance is more important than trust.
    final_score = (
        relevance * 0.70
        + trust * 0.30
    )

    return {
        "relevance_score": round(relevance),
        "trust_score": trust,
        "source_score": round(final_score)
    }


# =====================================================
# ANALYZE NEWS URL
# =====================================================

def analyze_news_url(
    url: str,
    claim: str = ""
):

    result = extract_article(url)

    if not result:
        return {
            "url": url,
            "error": "Unable to extract article."
        }

    if result.get("error"):
        return {
            "url": url,
            "error": result["error"]
        }

    title = result.get(
        "title",
        ""
    )

    text = result.get(
        "text",
        ""
    )

    scores = calculate_source_score(
        claim=claim,
        title=title,
        text=text,
        url=url
    )

    return {
        "url": url,

        "title": title,

        "text": text,

        "authors": result.get(
            "authors",
            []
        ),

        "publish_date": result.get(
            "publish_date"
        ),

        "relevance_score":
            scores["relevance_score"],

        "trust_score":
            scores["trust_score"],

        "source_score":
            scores["source_score"]
    }


# =====================================================
# FILTER SOURCES
# =====================================================

def filter_relevant_sources(
    sources,
    minimum_relevance: int = 35
):

    if not sources:
        return []

    filtered = []

    for source in sources:

        relevance = source.get(
            "relevance_score",
            0
        )

        if relevance >= minimum_relevance:
            filtered.append(source)

    # Highest source score first
    filtered.sort(
        key=lambda item:
            item.get(
                "source_score",
                0
            ),
        reverse=True
    )

    return filtered


# =====================================================
# LIMIT SOURCES SENT TO GEMINI
# =====================================================

def select_best_sources(
    sources,
    limit: int = 5
):

    relevant = filter_relevant_sources(
        sources
    )

    return relevant[:limit]