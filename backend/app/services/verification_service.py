# ============================================================
# REALITYCHECK AI
# VERIFICATION DECISION ENGINE
# ============================================================

import re
import os
import json
from pathlib import Path

from dotenv import load_dotenv

from app.services.evidence_service import (
    collect_evidence,
    fetch_page,
    get_domain,
    get_trust_score,
    get_source_type
)


# ============================================================
# OPTIONAL GEMINI
# ============================================================

try:

    from google import genai
    from google.genai import types

    GEMINI_AVAILABLE = True

except Exception:

    GEMINI_AVAILABLE = False


BASE_DIR = Path(
    __file__
).resolve().parent.parent.parent

load_dotenv(
    BASE_DIR / ".env"
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

MODEL_NAME = "gemini-3.6-flash"

gemini_client = None

if (
    GEMINI_AVAILABLE
    and GEMINI_API_KEY
):

    try:

        gemini_client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    except Exception as e:

        print(
            "Gemini initialization failed:",
            str(e)
        )

        gemini_client = None


# ============================================================
# CLAIM KEYWORDS
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
    "report",
    "reported",
    "article"
}


def words(text: str) -> set:

    found = re.findall(
        r"[a-zA-Z][a-zA-Z0-9'-]{2,}",
        text.lower()
    )

    return {
        word
        for word in found
        if word not in STOPWORDS
    }


# ============================================================
# SOURCE AGREEMENT
# ============================================================

def source_agreement(
    article_text: str,
    source: dict
) -> float:

    article_words = words(
        article_text
    )

    source_text = (
        source.get("title", "")
        + " "
        + source.get("snippet", "")
        + " "
        + source.get("text", "")
    )

    source_words = words(
        source_text
    )

    if not article_words:
        return 0

    common = (
        article_words
        & source_words
    )

    return (
        len(common)
        / len(article_words)
    )


# ============================================================
# CONTRADICTION DETECTION
# ============================================================

CONTRADICTION_PATTERNS = [

    (
        r"\bnot\b",
        "negative statement"
    ),

    (
        r"\bdenied\b",
        "denial"
    ),

    (
        r"\bdenies\b",
        "denial"
    ),

    (
        r"\bfalse\b",
        "false claim"
    ),

    (
        r"\bfake\b",
        "fake claim"
    ),

    (
        r"\bincorrect\b",
        "incorrect claim"
    ),

    (
        r"\bmisleading\b",
        "misleading claim"
    ),

    (
        r"\bno such\b",
        "no such event"
    ),

    (
        r"\bdid not\b",
        "negative statement"
    ),

    (
        r"\bhas not\b",
        "negative statement"
    ),

    (
        r"\bwas not\b",
        "negative statement"
    ),

    (
        r"\bwere not\b",
        "negative statement"
    ),

]


def contradiction_score(
    source: dict
) -> float:

    text = (
        source.get("title", "")
        + " "
        + source.get("snippet", "")
        + " "
        + source.get("text", "")
    ).lower()

    score = 0

    for pattern, _ in CONTRADICTION_PATTERNS:

        if re.search(
            pattern,
            text
        ):

            score += 1

    return min(
        score / 4,
        1
    )


# ============================================================
# GEMINI JUDGMENT
# ============================================================

def gemini_judge(
    article_text: str,
    sources: list
):

    if not gemini_client:
        return None

    evidence_text = ""

    for source in sources[:5]:

        evidence_text += f"""

SOURCE:
{source.get("title", "")}

DOMAIN:
{source.get("domain", "")}

CONTENT:
{source.get("text", "")[:2500]}

--------------------------------
"""

    prompt = f"""
You are the final fact-checking judge for RealityCheck AI.

Determine whether the article is REAL, FAKE, or UNCERTAIN.

ARTICLE:
{article_text[:12000]}

INDEPENDENT EVIDENCE:
{evidence_text}

Rules:

REAL:
Reliable independent evidence supports the main factual claims.

FAKE:
Reliable evidence directly contradicts an important factual claim.

UNCERTAIN:
The evidence is insufficient or conflicting.

Do not call something fake simply because one source
does not report it.

Do not call something real simply because the original
article exists.

Use the actual evidence.

Return ONLY JSON:

{{
    "verdict": "REAL",
    "confidence": 90,
    "summary": "Short factual explanation.",
    "reason": "Why the evidence supports or contradicts the article."
}}
"""

    try:

        response = gemini_client.models.generate_content(

            model=MODEL_NAME,

            contents=prompt,

            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )

        )

        text = getattr(
            response,
            "text",
            ""
        )

        if not text:
            return None

        text = text.strip()

        if text.startswith("```"):

            lines = text.splitlines()

            lines = lines[1:]

            if (
                lines
                and lines[-1].strip()
                == "```"
            ):
                lines = lines[:-1]

            text = "\n".join(
                lines
            )

        return json.loads(
            text
        )

    except Exception as e:

        print(
            "Gemini judge unavailable:",
            str(e)
        )

        # IMPORTANT:
        # Do not allow Gemini failure to break verification.
        return None


# ============================================================
# DECISION ENGINE
# ============================================================

def decide(
    article_text: str,
    evidence: list
) -> dict:

    if not evidence:

        return {

            "verdict": "UNCERTAIN",

            "confidence": 20,

            "summary":
                "No sufficiently relevant independent evidence was found.",

            "reason":
                "The article could not be independently confirmed or contradicted."

        }

    support_points = 0
    contradiction_points = 0

    strong_sources = []
    contradictory_sources = []

    # --------------------------------------------------------
    # Evaluate each source
    # --------------------------------------------------------

    for source in evidence:

        agreement = source_agreement(
            article_text,
            source
        )

        contradiction = contradiction_score(
            source
        )

        trust = source.get(
            "trust_score",
            3
        )

        match = source.get(
            "match_score",
            0
        )

        # Strong relevance
        if agreement >= 0.15 or match >= 15:

            # Trusted source
            if trust >= 7:

                support_points += 3

                strong_sources.append(
                    source
                )

            elif trust >= 5:

                support_points += 2

            else:

                support_points += 1

        # Possible contradiction
        if (
            contradiction >= 0.50
            and (
                agreement >= 0.10
                or match >= 10
            )
        ):

            if trust >= 7:

                contradiction_points += 4

                contradictory_sources.append(
                    source
                )

            elif trust >= 5:

                contradiction_points += 2

    # --------------------------------------------------------
    # Decision
    # --------------------------------------------------------

    # Strong direct contradiction wins
    if contradiction_points >= 6:

        verdict = "FAKE"

        confidence = min(
            98,
            70 + contradiction_points * 3
        )

        summary = (
            "Reliable independent evidence "
            "contradicts an important claim in the article."
        )

        reason = (
            "Multiple relevant sources contain evidence "
            "that conflicts with the article's claim."
        )

        return {
            "verdict": verdict,
            "confidence": confidence,
            "summary": summary,
            "reason": reason
        }

    # Strong confirmation
    if support_points >= 8:

        verdict = "REAL"

        confidence = min(
            97,
            70 + support_points * 2
        )

        summary = (
            "The article's main claims are supported "
            "by relevant independent sources."
        )

        reason = (
            "Multiple independent sources agree with "
            "the important facts reported in the article."
        )

        return {
            "verdict": verdict,
            "confidence": confidence,
            "summary": summary,
            "reason": reason
        }

    # Moderate confirmation
    if support_points >= 4:

        return {
            "verdict": "REAL",
            "confidence": 72,
            "summary":
                "The article is supported by relevant independent evidence.",
            "reason":
                "Independent reporting is consistent with the article, "
                "although the evidence is not comprehensive."
        }

    # Some contradiction
    if contradiction_points >= 3:

        return {
            "verdict": "FAKE",
            "confidence": 68,
            "summary":
                "Some relevant evidence contradicts the article.",
            "reason":
                "The available independent evidence raises substantial "
                "contradictions with the article's claims."
        }

    # Not enough
    return {

        "verdict": "UNCERTAIN",

        "confidence": 35,

        "summary":
            "The available evidence is not strong enough "
            "to establish whether the article is real or fake.",

        "reason":
            "Some related sources were found, but they do not provide "
            "enough direct evidence for a confident verdict."

    }


# ============================================================
# FINAL VERIFICATION
# ============================================================

def verify_article(
    article_url: str,
    title: str,
    article_text: str
) -> dict:

    print(
        "\n========================================"
    )

    print(
        "REALITYCHECK AI VERIFICATION"
    )

    print(
        "========================================"
    )

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    evidence_result = collect_evidence(

        article_url,

        title,

        article_text

    )

    evidence = evidence_result.get(
        "sources",
        []
    )

    # --------------------------------------------------------
    # Rule-based decision
    # --------------------------------------------------------

    decision = decide(

        article_text,

        evidence

    )

    # --------------------------------------------------------
    # Optional Gemini
    # --------------------------------------------------------

    gemini_result = None

    if evidence:

        gemini_result = gemini_judge(

            article_text,

            evidence

        )

    # --------------------------------------------------------
    # Use Gemini only when it gives a valid answer
    # --------------------------------------------------------

    if isinstance(
        gemini_result,
        dict
    ):

        gemini_verdict = str(
            gemini_result.get(
                "verdict",
                ""
            )
        ).upper()

        try:

            gemini_confidence = float(
                gemini_result.get(
                    "confidence",
                    0
                )
            )

        except Exception:

            gemini_confidence = 0

        if gemini_verdict in {
            "REAL",
            "FAKE",
            "UNCERTAIN"
        }:

            # ------------------------------------------------
            # Agreement with evidence engine
            # ------------------------------------------------

            if gemini_verdict == decision["verdict"]:

                decision["confidence"] = min(
                    98,
                    max(
                        decision["confidence"],
                        round(
                            (
                                decision["confidence"]
                                + gemini_confidence
                            ) / 2
                        )
                    )
                )

                if gemini_result.get(
                    "summary"
                ):

                    decision["summary"] = (
                        gemini_result[
                            "summary"
                        ]
                    )

                if gemini_result.get(
                    "reason"
                ):

                    decision["reason"] = (
                        gemini_result[
                            "reason"
                        ]
                    )

            # ------------------------------------------------
            # Disagreement
            # ------------------------------------------------

            elif (
                gemini_verdict != "UNCERTAIN"
                and decision["verdict"] != "UNCERTAIN"
            ):

                # When two independent methods disagree,
                # don't falsely claim certainty.
                decision = {

                    "verdict": "UNCERTAIN",

                    "confidence": 45,

                    "summary":
                        "Reliable evidence is conflicting.",

                    "reason":
                        "The evidence-based analysis and secondary "
                        "AI analysis reached different conclusions."

                }

    # --------------------------------------------------------
    # Format sources
    # --------------------------------------------------------

    formatted_sources = []

    # Original article
    formatted_sources.append({

        "url": article_url,

        "title": title or get_domain(
            article_url
        ),

        "domain": get_domain(
            article_url
        ),

        "trust_score": get_trust_score(
            article_url
        ),

        "source_type": get_source_type(
            article_url
        ),

        "role": "Original article"

    })

    # Independent sources
    for source in evidence:

        formatted_sources.append({

            "url": source.get(
                "url",
                ""
            ),

            "title": source.get(
                "title",
                ""
            ),

            "domain": source.get(
                "domain",
                ""
            ),

            "trust_score": source.get(
                "trust_score",
                0
            ),

            "source_type": source.get(
                "source_type",
                "Other"
            ),

            "match_score": source.get(
                "match_score",
                0
            ),

            "role": "Independent evidence"

        })

    # --------------------------------------------------------
    # Final
    # --------------------------------------------------------

    final_result = {

        "success": True,

        "url": article_url,

        "title": title,

        "prediction": decision[
            "verdict"
        ],

        "verdict": decision[
            "verdict"
        ],

        "confidence": decision[
            "confidence"
        ],

        "summary": decision[
            "summary"
        ],

        "reason": decision[
            "reason"
        ],

        "explanation": [
            decision[
                "reason"
            ]
        ],

        "sources": [
            source["url"]
            for source in formatted_sources
        ],

        "source_details": formatted_sources,

        "evidence_count": len(
            evidence
        ),

        "gemini_used": (
            gemini_result is not None
        )

    }

    print(
        "\nVERDICT:",
        final_result["verdict"]
    )

    print(
        "CONFIDENCE:",
        final_result["confidence"]
    )

    print(
        "SOURCES:",
        len(formatted_sources)
    )

    print(
        "========================================\n"
    )

    return final_result