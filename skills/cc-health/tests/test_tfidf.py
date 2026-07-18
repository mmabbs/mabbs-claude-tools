"""Tests for TF-IDF engine."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from lib.tfidf import tokenize, build_tfidf, cosine_similarity, top_shared_terms


def test_tokenize_lowercases():
    assert tokenize("Hello World") == ["hello", "world"]


def test_tokenize_strips_punctuation():
    result = tokenize("audit, review. check!")
    assert result == ["audit", "review", "check"]


def test_tokenize_removes_stopwords():
    result = tokenize("use this when the user asks to audit")
    assert "use" not in result
    assert "this" not in result
    assert "when" not in result
    assert "the" not in result
    assert "audit" in result
    assert "user" not in result
    assert "asks" in result


def test_tokenize_empty_string():
    assert tokenize("") == []


def test_build_tfidf_single_doc():
    tokens = [["audit", "config", "audit"]]
    result = build_tfidf(tokens)
    assert len(result) == 1
    assert result[0]["audit"] > 0
    assert result[0]["config"] > 0


def test_build_tfidf_idf_weighting():
    """Terms appearing in all docs get lower weight than rare terms."""
    tokens = [
        ["audit", "skills"],
        ["audit", "config"],
        ["audit", "memory"],
    ]
    result = build_tfidf(tokens)
    # "audit" appears in all 3 docs → smoothed IDF = log(3/3) + 1 = 1.0
    # Still has positive weight, but lower than rare terms
    assert result[0]["audit"] > 0
    # "skills" appears in 1 doc → IDF = log(3/1) + 1 ≈ 2.1 → higher weight
    assert result[0]["skills"] > result[0]["audit"]


def test_cosine_similarity_identical():
    vec = {"audit": 1.0, "config": 0.5}
    assert cosine_similarity(vec, vec) == pytest.approx(1.0)


def test_cosine_similarity_orthogonal():
    vec_a = {"audit": 1.0}
    vec_b = {"config": 1.0}
    assert cosine_similarity(vec_a, vec_b) == 0.0


def test_cosine_similarity_partial_overlap():
    vec_a = {"audit": 1.0, "config": 1.0}
    vec_b = {"audit": 1.0, "memory": 1.0}
    sim = cosine_similarity(vec_a, vec_b)
    assert 0.0 < sim < 1.0


def test_cosine_similarity_empty_vector():
    assert cosine_similarity({}, {"audit": 1.0}) == 0.0
    assert cosine_similarity({}, {}) == 0.0


def test_top_shared_terms():
    vec_a = {"audit": 0.8, "config": 0.3, "skills": 0.5}
    vec_b = {"audit": 0.9, "memory": 0.4, "skills": 0.2}
    result = top_shared_terms(vec_a, vec_b, n=2)
    assert result == ["audit", "skills"]


def test_top_shared_terms_no_overlap():
    vec_a = {"audit": 0.8}
    vec_b = {"config": 0.9}
    assert top_shared_terms(vec_a, vec_b) == []
