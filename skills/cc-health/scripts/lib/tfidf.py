"""Lightweight TF-IDF engine for skill description comparison. Stdlib only."""

import math
import re
from collections import Counter

STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "can", "do",
    "for", "from", "had", "has", "if", "in", "into", "is", "it", "its",
    "no", "not", "of", "on", "or", "so", "that", "the", "them", "they",
    "this", "to", "use", "was", "will", "with", "you", "your",
    "user", "skill", "invoke", "should", "about", "also", "any",
    "before", "been", "does", "doing", "done", "each",
    "even", "every", "first", "get", "have", "how", "just", "may",
    "more", "most", "must", "need", "needs", "new", "only", "other",
    "over", "own", "same", "set", "some", "such", "than", "then",
    "these", "those", "through", "too", "under", "up", "very",
    "want", "wants", "what", "when", "which", "who", "why", "would",
})

_PUNCT_RE = re.compile(r"[^\w\s]", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, split whitespace, remove stopwords."""
    text = _PUNCT_RE.sub(" ", text.lower())
    return [w for w in text.split() if w and w not in STOPWORDS]


def build_tfidf(documents: list[list[str]]) -> list[dict[str, float]]:
    """Build TF-IDF weight vectors from pre-tokenized documents.

    Returns one dict per document mapping term -> weight.
    """
    n = len(documents)
    if n == 0:
        return []

    # Document frequency: how many docs contain each term
    df: Counter = Counter()
    for doc in documents:
        df.update(set(doc))

    result = []
    for doc in documents:
        tf = Counter(doc)
        doc_len = len(doc) if doc else 1
        weights = {}
        for term, count in tf.items():
            idf = math.log(n / df[term]) + 1.0
            weights[term] = (count / doc_len) * idf
        result.append(weights)
    return result


def cosine_similarity(vec_a: dict[str, float], vec_b: dict[str, float]) -> float:
    """Cosine similarity between two sparse vectors. Returns 0.0-1.0."""
    if not vec_a or not vec_b:
        return 0.0

    shared_terms = set(vec_a) & set(vec_b)
    if not shared_terms:
        return 0.0

    dot = sum(vec_a[t] * vec_b[t] for t in shared_terms)
    mag_a = math.sqrt(sum(v * v for v in vec_a.values()))
    mag_b = math.sqrt(sum(v * v for v in vec_b.values()))

    if mag_a == 0 or mag_b == 0:
        return 0.0

    return dot / (mag_a * mag_b)


def top_shared_terms(
    vec_a: dict[str, float], vec_b: dict[str, float], n: int = 3
) -> list[str]:
    """Return the n terms with highest combined TF-IDF weight in both vectors."""
    shared = set(vec_a) & set(vec_b)
    if not shared:
        return []
    ranked = sorted(shared, key=lambda t: vec_a[t] + vec_b[t], reverse=True)
    return ranked[:n]
