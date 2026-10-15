"""
Konfigurasi aplikasi SecureVault.
"""

import os


class BaseConfig:
    """Konfigurasi dasar yang digunakan semua environment."""
    TESTING = False
    DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///securevault.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")


class DevelopmentConfig(BaseConfig):
    """Konfigurasi untuk environment development."""
    DEBUG = True                         # ⚠ SAST: debug aktif
    SECRET_KEY = "dev-secret-key-12345"  # ⚠ SAST: hardcoded secret


class ProductionConfig(BaseConfig):
    """Konfigurasi untuk environment production."""
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")


class TestingConfig(BaseConfig):
    """Konfigurasi untuk environment testing."""
    TESTING = True
    DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-secret"
