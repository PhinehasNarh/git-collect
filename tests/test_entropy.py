"""Tests for the entropy heuristic."""

from gitcollect.scanner import find_high_entropy_tokens, shannon_entropy


def test_uniform_string_has_zero_entropy():
    assert shannon_entropy("aaaaaaaa") == 0.0


def test_random_string_has_high_entropy():
    assert shannon_entropy("aZ3kP9xL2qW7mB1rT4yU") > 3.5


def test_finds_high_entropy_token():
    text = "key = ZmFrZWhpZ2hlbnRyb3B5c2VjcmV0dmFsdWVzdHJpbmc"
    assert find_high_entropy_tokens(text)


def test_ignores_normal_prose():
    assert find_high_entropy_tokens("the quick brown fox jumps over") == []
