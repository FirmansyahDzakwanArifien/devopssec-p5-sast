"""
Unit test untuk modul utils SecureVault.
Jalankan: pytest tests/ -v
"""

import pytest
from app.utils import (
    hash_password,
    validate_username,
    generate_token,
    sanitize_filename,
    truncate_text,
    format_response,
)


class TestHashPassword:
    def test_returns_string(self):
        assert isinstance(hash_password("secret"), str)

    def test_consistent_hash(self):
        assert hash_password("abc") == hash_password("abc")

    def test_different_passwords_different_hashes(self):
        assert hash_password("abc") != hash_password("xyz")

    def test_hash_length(self):
        # SHA-256 menghasilkan 64 karakter hex
        assert len(hash_password("test")) == 64


class TestValidateUsername:
    def test_valid_username(self):
        assert validate_username("firmansyah") is True

    def test_valid_with_numbers(self):
        assert validate_username("user123") is True

    def test_valid_with_underscore(self):
        assert validate_username("user_name") is True

    def test_too_short(self):
        assert validate_username("ab") is False

    def test_too_long(self):
        assert validate_username("a" * 33) is False

    def test_special_chars(self):
        assert validate_username("user@name") is False

    def test_spaces(self):
        assert validate_username("user name") is False


class TestGenerateToken:
    def test_returns_string(self):
        assert isinstance(generate_token(), str)

    def test_default_length(self):
        # 32 bytes = 64 hex chars
        assert len(generate_token()) == 64

    def test_custom_length(self):
        assert len(generate_token(16)) == 32

    def test_unique_tokens(self):
        assert generate_token() != generate_token()


class TestSanitizeFilename:
    def test_normal_filename(self):
        assert sanitize_filename("document.txt") == "document.txt"

    def test_path_traversal(self):
        result = sanitize_filename("../../etc/passwd")
        assert ".." not in result
        assert "/" not in result

    def test_special_chars(self):
        result = sanitize_filename("file name!@#.txt")
        assert " " not in result
        assert "!" not in result

    def test_empty_string(self):
        assert sanitize_filename("") is None


class TestTruncateText:
    def test_short_text_unchanged(self):
        text = "Hello"
        assert truncate_text(text, 200) == text

    def test_long_text_truncated(self):
        text = "a" * 300
        result = truncate_text(text, 200)
        assert len(result) == 203  # 200 + "..."
        assert result.endswith("...")

    def test_exact_length(self):
        text = "a" * 200
        assert truncate_text(text, 200) == text


class TestFormatResponse:
    def test_success_response(self):
        r = format_response("ok", data={"id": 1})
        assert r["status"] == "ok"
        assert r["data"] == {"id": 1}

    def test_error_response(self):
        r = format_response("error", message="Not found")
        assert r["status"] == "error"
        assert r["message"] == "Not found"

    def test_no_data(self):
        r = format_response("ok")
        assert "data" not in r
