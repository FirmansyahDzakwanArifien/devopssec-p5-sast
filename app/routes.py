"""
Routes untuk blueprint auth dan notes.
File ini mengandung kerentanan yang disengaja untuk tujuan pembelajaran SAST.
"""

import sqlite3
import subprocess
from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)
notes_bp = Blueprint("notes", __name__)

DB_PATH = "securevault.db"


def get_db():
    """Membuka koneksi database SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─── Auth routes ──────────────────────────────────────────────────────────────

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login endpoint.
    ⚠ VULNERABILITY: SQL Injection — input langsung dimasukkan ke query.
    """
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    conn = get_db()
    cursor = conn.cursor()

    # ⚠ SQL INJECTION — jangan gunakan di production!
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "ok", "user": username})
    return jsonify({"status": "error", "message": "Invalid credentials"}), 401


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register user baru."""
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")

    conn = get_db()
    cursor = conn.cursor()
    # ⚠ Password disimpan plaintext
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (username, password),
    )
    conn.commit()
    conn.close()
    return jsonify({"status": "registered"})


# ─── Notes routes ─────────────────────────────────────────────────────────────

@notes_bp.route("/", methods=["GET"])
def list_notes():
    """Menampilkan semua catatan milik user."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, content FROM notes")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify(rows)


@notes_bp.route("/search", methods=["GET"])
def search_notes():
    """
    Mencari catatan berdasarkan keyword.
    ⚠ VULNERABILITY: Command injection via subprocess.
    """
    keyword = request.args.get("q", "")

    # ⚠ COMMAND INJECTION — shell=True dengan input user langsung
    result = subprocess.run(
        f"grep -r '{keyword}' /tmp/notes/",
        shell=True,
        capture_output=True,
        text=True,
    )
    return jsonify({"matches": result.stdout.splitlines()})


@notes_bp.route("/<int:note_id>", methods=["GET"])
def get_note(note_id):
    """Mengambil satu catatan berdasarkan ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Not found"}), 404


@notes_bp.route("/", methods=["POST"])
def create_note():
    """Membuat catatan baru."""
    data = request.get_json()
    title = data.get("title", "")
    content = data.get("content", "")

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content),
    )
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": note_id, "title": title}), 201
