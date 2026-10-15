"""
Fungsi-fungsi utilitas untuk SecureVault.
"""

import hashlib
import os
import re
from typing import Optional


def hash_password(password: str) -> str:
    """
    Hash password menggunakan SHA-256.
    Catatan: untuk production gunakan bcrypt atau argon2.
    """
    # ⚠ SAST: SHA-256 tanpa salt tidak direkomendasikan untuk password
    return hashlib.sha256(password.encode()).hexdigest()


def validate_username(username: str) -> bool:
    """Validasi format username: 3-32 karakter alfanumerik."""
    pattern = r"^[a-zA-Z0-9_]{3,32}$"
    return bool(re.match(pattern, username))


def generate_token(length: int = 32) -> str:
    """Membuat random token untuk session."""
    return os.urandom(length).hex()


def sanitize_filename(filename: str) -> Optional[str]:
    """
    Membersihkan nama file dari karakter berbahaya.
    Mencegah path traversal attack.
    """
    # Hapus path traversal sequences
    filename = os.path.basename(filename)
    # Hanya izinkan karakter aman
    filename = re.sub(r"[^\w\-.]", "_", filename)
    return filename if filename else None


def truncate_text(text: str, max_length: int = 200) -> str:
    """Memotong teks panjang untuk preview."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def format_response(status: str, data=None, message: str = "") -> dict:
    """Format standar response API."""
    response = {"status": status}
    if data is not None:
        response["data"] = data
    if message:
        response["message"] = message
    return response
