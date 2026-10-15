"""
Inisialisasi dan migrasi database SQLite untuk SecureVault.
"""

import sqlite3
import os

DB_PATH = os.environ.get("DATABASE_PATH", "securevault.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    NOT NULL UNIQUE,
    password TEXT    NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS notes (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER REFERENCES users(id),
    title      TEXT    NOT NULL,
    content    TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""


def init_db(db_path: str = DB_PATH) -> None:
    """Membuat tabel database jika belum ada."""
    conn = sqlite3.connect(db_path)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"[DB] Database initialized at: {db_path}")


def drop_db(db_path: str = DB_PATH) -> None:
    """Menghapus file database (untuk keperluan testing)."""
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"[DB] Database removed: {db_path}")


if __name__ == "__main__":
    init_db()
