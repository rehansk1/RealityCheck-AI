# ============================================================
# REALITYCHECK AI
# EVIDENCE COLLECTION SERVICE
# ============================================================

import re
import html
import requests
import xml.etree.ElementTree as ET

from urllib.parse import (
    quote_plus,
    urlparse
)

from bs4 import BeautifulSoup


# ============================================================
# CONFIG
# ============================================================

REQUEST_TIMEOUT = 15
MAX_SEARCH_RESULTS = 8
MAX_SOURCE_TEXT = 12000


# ============================================================
# TRUSTED DOMAINS
# ============================================================

TRUSTED_DOMAINS = {
    # Government
    "pib.gov.in": 10,
    "india.gov.in": 10,
    "gov.in": 10,
    "mygov.in": 10,
    "pmindia.gov.in": 10,

    # International
    "reuters.com": 9,
    "apnews.com": 9,
    "bbc.com": 8,
    "bbc.co.uk": 8,

    # Indian
    "thehindu.com": 8,
    "indianexpress.com": 8,
    "hindustantimes.com": 7,
    "timesofindia.indiatimes.com": 7,
    "economictimes.indiatimes.com": 7,
    "livemint.com": 7,

    # Other established news
    "ndtv.com": 7,
    "news18.com": 6,
    "deccanherald.com": 6,
    "telegraphindia.com": 6,
    "theprint.in": 6,
}


# ============================================================
# USER AGENT
# ============================================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}


# ============================================================
# DOMAIN
# ============================================================

def get_domain(url: str) -> str:

    try:

        hostname = urlparse(
            url
        ).netloc.lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        return hostname

    except Exception:

        return ""


# ============================================================
# TRUST SCORE
# ============================================================

def get_trust_score(url: str) -> int:

    domain = get_domain(url)

    if not domain:
        return 2

    for trusted_domain, score in TRUSTED_DOMAINS.items():

        if (
            domain == trusted_domain
            or domain.endswith(
                "." + trusted_domain
            )
        ):
            return score

    return 3


# ============================================================
# SOURCE TYPE
# ============================================================

def get_source_type(url: str) -> str:

    domain = get_domain(url)

    if (
        domain == "gov.in"
        or domain.endswith(".gov.in")
    ):
        return "Government"

    if domain in {
        "reuters.com",
        "apnews.com",
        "bbc.com",
        "bbc.co.uk"
    }:
        return "International News"

    if domain in {
        "thehindu.com",
        "indianexpress.com",
        "hindustantimes.com",
        "timesofindia.indiatimes.com",
        "economictimes.indiatimes.com",
        "livemint.com",
        "ndtv.com",
        "news18.com"
    }:
        return "Indian News"

    return "Other"


# ============================================================
# CLEAN TEXT
# ============================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    text = html.unescape(
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# FETCH ARTICLE
# ============================================================

def fetch_page(url: str) -> dict:

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form",
            "noscript",
            "svg"
        ]):
            element.decompose()

        title = ""

        if soup.title:

            title = clean_text(
                soup.title.get_text(
                    " ",
                    strip=True
                )
            )

        article = soup.find(
            "article"
        )

        if article:

            text = article.get_text(
                " ",
                strip=True
            )

        else:

            paragraphs = soup.find_all(
                "p"
            )

            text = " ".join(
                p.get_text(
                    " ",
                    strip=True
                )
                for p in paragraphs
            )

        text = clean_text(
            text
        )

        return {
            "success": True,
            "url": url,
            "title": title,
            "text": text[:MAX_SOURCE_TEXT]
        }

    except Exception as e:

        print(
            "Source fetch failed:",
            url,
            str(e)
        )

        return {
            "success": False,
            "url": url,
            "title": "",
            "text": ""
        }


# ============================================================
# IMPORTANT WORDS
# ============================================================

STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "this",
    "with",
    "from",
    "have",
    "has",
    "had",
    "was",
    "were",
    "are",
    "been",
    "will",
    "would",
    "could",
    "should",
    "about",
    "after",
    "before",
    "into",
    "their",
    "they",
    "them",
    "than",
    "then",
    "also",
    "said",
    "says",
    "news",
    "according",
    "reported",
    "report",
    "article",
}


def keywords(text: str) -> set:

    words = re.findall(
        r"[a-zA-Z][a-zA-Z0-9'-]{2,}",
        text.lower()
    )

    return {
        word
        for word in words
        if word not in STOPWORDS
    }


# ============================================================
# SEARCH QUERY
# ============================================================

def build_search_query(
    title: str,
    article_text: str
) -> str:

    title_words = list(
        keywords(title)
    )

    article_words = list(
        keywords(article_text)
    )

    selected = []

    # Title words have priority
    for word in title_words:

        if len(selected) >= 12:
            break

        selected.append(
            word
        )

    # Add article words
    for word in article_words:

        if len(selected) >= 18:
            break

        if word not in selected:

            selected.append(
                word
            )

    return " ".join(
        selected
    )


# ============================================================
# GOOGLE NEWS RSS SEARCH
# ============================================================

def google_news_search(
    query: str
) -> list:

    if not query:
        return []

    url = (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query)}"
        "&hl=en-IN"
        "&gl=IN"
        "&ceid=IN:en"
    )

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()

        root = ET.fromstring(
            response.content
        )

        results = []

        for item in root.findall(
            ".//item"
        ):

            title = item.findtext(
                "title",
                ""
            )

            link = item.findtext(
                "link",
                ""
            )

            description = item.findtext(
                "description",
                ""
            )

            pub_date = item.findtext(
                "pubDate",
                ""
            )

            title = clean_text(
                title
            )

            link = clean_text(
                link
            )

            description = clean_text(
                BeautifulSoup(
                    description,
                    "html.parser"
                ).get_text(
                    " ",
                    strip=True
                )
            )

            if not link:
                continue

            results.append({

                "url": link,

                "title": title,

                "snippet": description,

                "published": pub_date

            })

            if len(results) >= MAX_SEARCH_RESULTS:
                break

        return results

    except Exception as e:

        print(
            "Google News search failed:",
            str(e)
        )

        return []


# ============================================================
# TEXT SIMILARITY
# ============================================================

def similarity(
    claim_text: str,
    source_text: str
) -> float:

    claim_words = keywords(
        claim_text
    )

    source_words = keywords(
        source_text
    )

    if not claim_words:
        return 0.0

    common = (
        claim_words
        & source_words
    )

    return (
        len(common)
        / len(claim_words)
    )


# ============================================================
# FIND EVIDENCE
# ============================================================

def collect_evidence(
    article_url: str,
    title: str,
    article_text: str
) -> dict:

    print(
        "Collecting independent evidence..."
    )

    query = build_search_query(
        title,
        article_text
    )

    print(
        "Evidence search query:",
        query
    )

    search_results = google_news_search(
        query
    )

    evidence = []

    original_domain = get_domain(
        article_url
    )

    seen_domains = set()

    # --------------------------------------------------------
    # Fetch source pages
    # --------------------------------------------------------

    for result in search_results:

        source_url = result.get(
            "url",
            ""
        )

        if not source_url:
            continue

        source_domain = get_domain(
            source_url
        )

        # Avoid duplicates
        if source_domain in seen_domains:
            continue

        seen_domains.add(
            source_domain
        )

        page = fetch_page(
            source_url
        )

        source_text = page.get(
            "text",
            ""
        )

        combined_source = (
            result.get("title", "")
            + " "
            + result.get("snippet", "")
            + " "
            + source_text
        )

        match_score = similarity(
            article_text,
            combined_source
        )

        trust_score = get_trust_score(
            source_url
        )

        # Don't use the original article as independent evidence
        independent = (
            source_domain
            != original_domain
        )

        if not independent:
            continue

        evidence.append({

            "url": source_url,

            "title": (
                result.get("title")
                or page.get("title")
                or source_domain
            ),

            "domain": source_domain,

            "source_type": get_source_type(
                source_url
            ),

            "trust_score": trust_score,

            "match_score": round(
                match_score * 100
            ),

            "snippet": result.get(
                "snippet",
                ""
            ),

            "text": source_text[:6000]

        })

    # --------------------------------------------------------
    # Sort
    # --------------------------------------------------------

    evidence.sort(
        key=lambda item: (
            item["trust_score"],
            item["match_score"]
        ),
        reverse=True
    )

    evidence = evidence[:8]

    print(
        "Independent sources found:",
        len(evidence)
    )

    return {

        "query": query,

        "sources": evidence

    }