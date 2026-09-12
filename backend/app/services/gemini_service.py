import os
import json
import time
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

print("Gemini API Key Loaded:", API_KEY is not None)

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=API_KEY
)


# ============================================================
# MODEL
# ============================================================

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# ============================================================
# TRUSTED DOMAINS
# ============================================================

TRUSTED_DOMAINS = {

    # --------------------------------------------------------
    # GOVERNMENT
    # --------------------------------------------------------

    "pib.gov.in": 10,
    "india.gov.in": 10,
    "gov.in": 10,
    "mygov.in": 10,
    "education.gov.in": 10,
    "mha.gov.in": 10,
    "pmindia.gov.in": 10,

    # --------------------------------------------------------
    # INTERNATIONAL NEWS
    # --------------------------------------------------------

    "reuters.com": 9,
    "apnews.com": 9,
    "bbc.com": 8,
    "bbc.co.uk": 8,

    # --------------------------------------------------------
    # INDIAN NEWS
    # --------------------------------------------------------

    "thehindu.com": 8,
    "indianexpress.com": 8,
    "hindustantimes.com": 7,
    "timesofindia.indiatimes.com": 7,
    "economictimes.indiatimes.com": 7,
    "livemint.com": 7,
}


# ============================================================
# GET DOMAIN
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
# SOURCE SCORE
# ============================================================

def get_source_score(url: str) -> int:

    hostname = get_domain(url)

    if not hostname:
        return 3

    for domain, score in TRUSTED_DOMAINS.items():

        if (
            hostname == domain
            or hostname.endswith("." + domain)
        ):
            return score

    return 3


# ============================================================
# SOURCE TYPE
# ============================================================

def get_source_type(url: str) -> str:

    hostname = get_domain(url)

    if (
        hostname == "gov.in"
        or hostname.endswith(".gov.in")
    ):
        return "Government"

    if hostname in {
        "reuters.com",
        "apnews.com",
        "bbc.com",
        "bbc.co.uk"
    }:
        return "International News"

    if hostname in {
        "thehindu.com",
        "indianexpress.com",
        "hindustantimes.com",
        "timesofindia.indiatimes.com",
        "economictimes.indiatimes.com",
        "livemint.com"
    }:
        return "Indian News"

    return "Other"


# ============================================================
# NORMALIZE SOURCES
# ============================================================

def normalize_sources(sources):

    if not isinstance(
        sources,
        list
    ):
        return []

    cleaned = []

    seen = set()

    for source in sources:

        # ----------------------------------------------------
        # Dictionary source
        # ----------------------------------------------------

        if isinstance(
            source,
            dict
        ):

            url = source.get(
                "url",
                ""
            )

            title = source.get(
                "title",
                ""
            )

        # ----------------------------------------------------
        # String source
        # ----------------------------------------------------

        else:

            url = str(
                source
            )

            title = ""

        if not isinstance(
            url,
            str
        ):
            continue

        url = url.strip()

        if not url.startswith(
            (
                "http://",
                "https://"
            )
        ):
            continue

        if url in seen:
            continue

        seen.add(url)

        domain = get_domain(
            url
        )

        cleaned.append({

            "url": url,

            "title":
                title
                or domain
                or "Source",

            "domain": domain,

            "trust_score":
                get_source_score(
                    url
                ),

            "source_type":
                get_source_type(
                    url
                )

        })

    # Highest trusted sources first.

    cleaned.sort(
        key=lambda item:
            item["trust_score"],
        reverse=True
    )

    return cleaned


# ============================================================
# EXTRACT GROUNDING SOURCES
# ============================================================

def extract_grounding_sources(response):

    sources = []

    try:

        candidates = getattr(
            response,
            "candidates",
            []
        )

        if not candidates:
            return []

        candidate = candidates[0]

        metadata = getattr(
            candidate,
            "grounding_metadata",
            None
        )

        if not metadata:
            return []

        chunks = getattr(
            metadata,
            "grounding_chunks",
            []
        )

        for chunk in chunks:

            web = getattr(
                chunk,
                "web",
                None
            )

            if not web:
                continue

            url = getattr(
                web,
                "uri",
                ""
            )

            title = getattr(
                web,
                "title",
                ""
            )

            if url:

                sources.append({

                    "url": url,

                    "title":
                        title
                        or get_domain(url)

                })

    except Exception as error:

        print(
            "Grounding source extraction error:",
            error
        )

    return normalize_sources(
        sources
    )


# ============================================================
# PARSE JSON
# ============================================================

def parse_json_response(response):

    text = getattr(
        response,
        "text",
        ""
    )

    if not text:

        raise ValueError(
            "Gemini returned an empty response."
        )

    text = text.strip()

    # --------------------------------------------------------
    # Remove markdown JSON fences
    # --------------------------------------------------------

    if text.startswith("```"):

        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if (
            lines
            and lines[-1].strip() == "```"
        ):
            lines = lines[:-1]

        text = "\n".join(
            lines
        ).strip()

    # --------------------------------------------------------
    # Parse JSON
    # --------------------------------------------------------

    try:

        return json.loads(
            text
        )

    except json.JSONDecodeError:

        # Try to find JSON object.

        start = text.find("{")
        end = text.rfind("}")

        if (
            start >= 0
            and end > start
        ):

            return json.loads(
                text[start:end + 1]
            )

        raise


# ============================================================
# GEMINI CALL
# ============================================================

def call_gemini(
    prompt: str,
    use_search: bool = True
):

    tools = []

    if use_search:

        tools.append(
            types.Tool(
                google_search=
                    types.GoogleSearch()
            )
        )

    attempts = 2

    for attempt in range(
        attempts
    ):

        try:

            config = (
                types.GenerateContentConfig(
                    response_mime_type=
                        "application/json",

                    temperature=0.1,

                    tools=tools
                )
            )

            response = (
                client.models.generate_content(

                    model=MODEL_NAME,

                    contents=prompt,

                    config=config

                )
            )

            return response

        except Exception as error:

            error_text = str(
                error
            )

            print(
                f"Gemini attempt "
                f"{attempt + 1} failed:"
            )

            print(
                error_text
            )

            retryable = (
                "429" in error_text
                or
                "RESOURCE_EXHAUSTED"
                in error_text
                or
                "503" in error_text
                or
                "UNAVAILABLE" in error_text
                or
                "500" in error_text
            )

            if (
                retryable
                and
                attempt < attempts - 1
            ):

                time.sleep(
                    2
                )

                continue

            raise


# ============================================================
# BUILD RESULT
# ============================================================

def build_result(
    result,
    grounding_sources=None,
    original_url=None
):

    if not isinstance(
        result,
        dict
    ):
        result = {}


    # ========================================================
    # VERDICT
    # ========================================================

    verdict = str(
        result.get(
            "verdict",
            "UNCERTAIN"
        )
    ).upper().strip()

    if verdict not in {
        "REAL",
        "FAKE",
        "UNCERTAIN"
    }:

        verdict = "UNCERTAIN"


    # ========================================================
    # CONFIDENCE
    # ========================================================

    try:

        confidence = float(
            result.get(
                "confidence",
                0
            )
        )

    except Exception:

        confidence = 0

    confidence = max(
        0,
        min(
            100,
            confidence
        )
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    summary = str(
        result.get(
            "summary",
            "There is not enough reliable evidence to verify this claim."
        )
    ).strip()


    # ========================================================
    # WHY
    # ========================================================

    reasons = result.get(
        "reason",
        []
    )

    # Gemini may return one string.

    if isinstance(
        reasons,
        str
    ):

        reasons = [
            reasons
        ]

    # Or multiple strings.

    elif isinstance(
        reasons,
        list
    ):

        reasons = [
            str(item).strip()
            for item in reasons
            if str(item).strip()
        ]

    else:

        reasons = []


    # Compatibility with explanation.

    if not reasons:

        explanation = result.get(
            "explanation",
            []
        )

        if isinstance(
            explanation,
            list
        ):

            reasons = [
                str(item).strip()
                for item in explanation
                if str(item).strip()
            ]

        elif explanation:

            reasons = [
                str(explanation)
            ]


    if not reasons:

        reasons = [
            "No detailed explanation was returned."
        ]


    # ========================================================
    # SOURCES FROM GEMINI JSON
    # ========================================================

    sources = normalize_sources(
        result.get(
            "sources",
            []
        )
    )


    # ========================================================
    # SOURCES FROM GOOGLE SEARCH GROUNDING
    # ========================================================

    if grounding_sources:

        existing_urls = {
            source["url"]
            for source in sources
        }

        for source in grounding_sources:

            if (
                source["url"]
                not in existing_urls
            ):

                sources.append(
                    source
                )

                existing_urls.add(
                    source["url"]
                )


    # ========================================================
    # ORIGINAL ARTICLE
    # ========================================================

    if original_url:

        original_sources = normalize_sources([
            {
                "url": original_url,
                "title": "Original article"
            }
        ])

        existing_urls = {
            source["url"]
            for source in sources
        }

        for source in original_sources:

            if (
                source["url"]
                not in existing_urls
            ):

                sources.insert(
                    0,
                    source
                )


    # ========================================================
    # SORT SOURCES
    # ========================================================

    # Original article stays first if present.

    if original_url and sources:

        original_item = None

        for source in sources:

            if source["url"] == original_url:

                original_item = source

                break

        remaining = [
            source
            for source in sources
            if source["url"] != original_url
        ]

        remaining.sort(
            key=lambda item:
                item["trust_score"],
            reverse=True
        )

        if original_item:

            sources = [
                original_item
            ] + remaining

        else:

            sources = remaining

    else:

        sources.sort(
            key=lambda item:
                item["trust_score"],
            reverse=True
        )


    sources = sources[:10]


    # ========================================================
    # RELEVANCE
    # ========================================================

    relevance = result.get(
        "relevance",
        []
    )

    if not isinstance(
        relevance,
        list
    ):

        relevance = []


    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "success": True,

        "verdict": verdict,

        "prediction": verdict,

        "confidence":
            round(confidence),

        "summary": summary,

        # React can display this as bullet points.

        "reason": reasons,

        "explanation": reasons,

        # Simple URL array.

        "sources": [
            source["url"]
            for source in sources
        ],

        # Full source information.

        "source_details": sources,

        "relevance": relevance

    }


# ============================================================
# NEWS TEXT VERIFICATION
# ============================================================

async def verify_news(
    news_text: str
):

    news_text = str(
        news_text or ""
    ).strip()

    if not news_text:

        raise ValueError(
            "News text cannot be empty."
        )


    prompt = f"""
You are RealityCheck AI, a professional news
fact-checking system.

Your job is to verify the important factual claims
in the news content below.

NEWS CONTENT:

{news_text[:18000]}


============================================================
STEP 1 — IDENTIFY THE MAIN CLAIM
============================================================

Identify the most important factual claim.

Ignore opinions, advertisements and unnecessary wording.


============================================================
STEP 2 — SEARCH FOR EVIDENCE
============================================================

Use Google Search to find current and independent evidence.

Search for the SAME:

- event
- people
- place
- date
- organization
- numbers
- government announcement
- important factual claims


============================================================
STEP 3 — PRIORITIZE SOURCES
============================================================

Prefer:

1. Official government sources
2. PIB
3. Government department websites
4. Reuters
5. AP
6. BBC
7. The Hindu
8. Indian Express
9. Hindustan Times
10. Times of India
11. Economic Times
12. Mint

Do NOT include a source just because it is famous.

The source must actually discuss the same claim/event.


============================================================
STEP 4 — VERDICT
============================================================

REAL:

Reliable evidence supports the important claim.

FAKE:

Reliable evidence directly contradicts an important
factual claim.

UNCERTAIN:

Reliable evidence is insufficient or genuinely conflicting.


IMPORTANT:

Do not guess.

Do not automatically trust the article.

Do not automatically call something REAL because
a famous newspaper published it.

Do not call something FAKE simply because it is unusual.

Compare the actual facts.


============================================================
STEP 5 — CONFIDENCE
============================================================

90-100:
Very strong evidence.

75-89:
Strong evidence.

60-74:
Moderate evidence.

0-59:
Weak, insufficient or conflicting evidence.


============================================================
STEP 6 — SUMMARY
============================================================

Write ONE simple sentence that an ordinary person
can understand.

Example:

"The main claim is supported by reliable sources."

OR:

"The main claim is contradicted by reliable sources."

OR:

"There is not enough reliable evidence to confirm this claim."


============================================================
STEP 7 — WHY
============================================================

Return 2 to 5 short bullet-style explanations.

Examples:

"Government source supports the claim."

"Reuters reported the same event."

"The official announcement matches the article."

"No major contradiction was found."

"The available sources contradict the reported date."

Each reason must be based on evidence.


============================================================
STEP 8 — SOURCES
============================================================

Return REAL URLs found through Google Search.

NEVER invent URLs.

For each source provide:

- title
- URL
- short reason why it is relevant

Use sources that directly support or contradict
the main claim.


============================================================
OUTPUT
============================================================

Return ONLY valid JSON.

Use this exact structure:

{{
    "verdict": "REAL",

    "confidence": 85,

    "summary":
        "The main claim is supported by reliable sources.",

    "reason": [
        "Government source supports the claim.",
        "Reuters reported the same event.",
        "No major contradiction was found."
    ],

    "sources": [
        {{
            "title": "Official Government Source",
            "url": "https://example.gov.in/example",
            "reason": "The official source confirms the event."
        }},
        {{
            "title": "Reuters",
            "url": "https://www.reuters.com/example",
            "reason": "Reuters independently reported the same event."
        }}
    ],

    "relevance": []
}}
"""


    try:

        response = call_gemini(
            prompt,
            use_search=True
        )

        # ----------------------------------------------------
        # Get model result
        # ----------------------------------------------------

        result = parse_json_response(
            response
        )

        # ----------------------------------------------------
        # Get actual Google grounding sources
        # ----------------------------------------------------

        grounding_sources = (
            extract_grounding_sources(
                response
            )
        )

        return build_result(
            result,
            grounding_sources=
                grounding_sources
        )

    except Exception as error:

        print(
            "Verification error:",
            str(error)
        )

        return {

            "success": True,

            "verdict": "UNCERTAIN",

            "prediction": "UNCERTAIN",

            "confidence": 0,

            "summary":
                "AI verification is temporarily unavailable.",

            "reason": [
                "The verification service could not complete the evidence check."
            ],

            "explanation": [
                "The verification service could not complete the evidence check."
            ],

            "sources": [],

            "source_details": [],

            "relevance": []

        }


# ============================================================
# URL VERIFICATION
# ============================================================

async def verify_url(
    article_url: str,
    article_text: str = ""
):

    article_url = str(
        article_url or ""
    ).strip()

    if not article_url:

        raise ValueError(
            "Article URL cannot be empty."
        )


    parsed = urlparse(
        article_url
    )

    if parsed.scheme not in {
        "http",
        "https"
    }:

        raise ValueError(
            "Please provide a valid HTTP or HTTPS URL."
        )


    domain = get_domain(
        article_url
    )


    # --------------------------------------------------------
    # Article content
    # --------------------------------------------------------

    content = str(
        article_text or ""
    ).strip()

    if not content:

        content = (
            "The article is available at this URL:\n"
            f"{article_url}\n"
            f"Domain: {domain}"
        )


    prompt = f"""
You are RealityCheck AI, a professional news
fact-checking system.

Verify the following online news article.

============================================================
ORIGINAL ARTICLE
============================================================

URL:

{article_url}

DOMAIN:

{domain}


============================================================
ARTICLE CONTENT
============================================================

{content[:18000]}


============================================================
TASK
============================================================

Identify the main factual claims in the article.

Search the web for independent evidence.

Compare:

1. Article claims
2. Official announcements
3. Independent news reports
4. Dates
5. People
6. Locations
7. Numbers
8. Events


============================================================
VERDICT
============================================================

REAL:

Reliable evidence supports the important claims.

FAKE:

Reliable evidence directly contradicts an important
factual claim.

UNCERTAIN:

Evidence is insufficient or genuinely conflicting.


Do not guess.

Do not trust the article merely because the website
is well known.

Do not mark the article FAKE simply because no source
was found.

Use the evidence.


============================================================
CONFIDENCE
============================================================

90-100 = Very strong evidence

75-89 = Strong evidence

60-74 = Moderate evidence

0-59 = Weak or conflicting evidence


============================================================
SUMMARY
============================================================

Write ONE simple sentence.

Example:

"The main claim is supported by reliable sources."


============================================================
WHY
============================================================

Return 2-5 short evidence-based points.

Example:

"Government source supports the claim."

"Reuters reported the same event."

"The official announcement matches the article."

"No major contradiction was found."


============================================================
SOURCES
============================================================

Return actual URLs from Google Search.

NEVER invent URLs.

Prefer:

Government / PIB
Reuters
AP
BBC
The Hindu
Indian Express
Hindustan Times
Times of India
Economic Times
Mint


Each source must have:

title
url
reason


============================================================
OUTPUT
============================================================

Return ONLY valid JSON:

{{
    "verdict": "REAL",

    "confidence": 85,

    "summary":
        "The main claim is supported by reliable sources.",

    "reason": [
        "Government source supports the claim.",
        "Reuters reported the same event.",
        "No major contradiction was found."
    ],

    "sources": [
        {{
            "title": "Official Government Source",
            "url": "https://example.gov.in/example",
            "reason": "The official source confirms the event."
        }},
        {{
            "title": "Reuters",
            "url": "https://www.reuters.com/example",
            "reason": "Reuters independently reported the same event."
        }}
    ],

    "relevance": []
}}
"""


    try:

        response = call_gemini(
            prompt,
            use_search=True
        )

        result = parse_json_response(
            response
        )

        grounding_sources = (
            extract_grounding_sources(
                response
            )
        )

        return build_result(
            result,
            grounding_sources=
                grounding_sources,
            original_url=
                article_url
        )

    except Exception as error:

        print(
            "URL verification error:",
            str(error)
        )

        return {

            "success": True,

            "verdict": "UNCERTAIN",

            "prediction": "UNCERTAIN",

            "confidence": 0,

            "summary":
                "AI verification is temporarily unavailable.",

            "reason": [
                "The verification service could not complete the evidence check."
            ],

            "explanation": [
                "The verification service could not complete the evidence check."
            ],

            "sources": [
                article_url
            ],

            "source_details":
                normalize_sources([
                    {
                        "url": article_url,
                        "title": "Original article"
                    }
                ]),

            "relevance": []

        }


# ============================================================
# COMPATIBILITY ALIAS
# ============================================================

async def analyze_url(
    article_url: str,
    article_text: str = ""
):

    return await verify_url(
        article_url,
        article_text
    )