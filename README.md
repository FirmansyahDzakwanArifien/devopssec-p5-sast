# SecureVault — DevSecOps Pipeline Demo

> Aplikasi manajemen catatan sederhana berbasis Flask, dibangun untuk mendemonstrasikan implementasi pipeline DevSecOps menggunakan GitHub Actions dan SAST tool Bandit.

---

## Nama Aplikasi & Fungsinya

**SecureVault** adalah REST API sederhana untuk menyimpan dan mengelola catatan personal. Aplikasi ini sengaja dirancang dengan beberapa kerentanan keamanan sebagai bahan pembelajaran SAST (Static Application Security Testing) dalam mata kuliah DevSecOps.

---

## Bahasa & Framework

| Komponen | Teknologi |
|----------|-----------|
| Bahasa | Python 3.11 |
| Framework | Flask 3.x |
| Database | SQLite |
| Testing | pytest + pytest-cov |
| SAST Tool | Bandit 1.7.x |
| CI/CD | GitHub Actions |

---

## Struktur Project

```
devsecops-p5-0110223282/
├── app/
│   ├── __init__.py
│   ├── main.py          # Entry point & application factory
│   ├── config.py        # Konfigurasi environment
│   ├── routes.py        # Blueprint: auth & notes
│   ├── database.py      # Inisialisasi SQLite
│   └── utils.py         # Fungsi utilitas
├── tests/
│   └── test_utils.py    # Unit test (pytest)
├── .github/
│   └── workflows/
│       └── devsecops.yml  # Pipeline CI/CD
├── requirements.txt
└── README.md
```

---

## Cara Menjalankan Aplikasi

### Prasyarat
- Python 3.11+
- pip

### Instalasi & Menjalankan

```bash
# Clone repository
git clone https://github.com/FirmansyahDzakwanArifien/devsecops-p5-0110223282.git
cd devsecops-p5-0110223282

# Install dependencies
pip install -r requirements.txt

# Inisialisasi database
python -m app.database

# Jalankan aplikasi
python -m app.main
# Aplikasi berjalan di http://localhost:5000
```

### Menjalankan Unit Test

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Menjalankan SAST Scan Manual

```bash
bandit -r app/ --severity-level medium --confidence-level medium
```

---

## Overview Pipeline CI/CD

Pipeline DevSecOps diimplementasikan menggunakan **GitHub Actions** dengan dua job yang berjalan secara berurutan:

```
Push/PR ke main
      │
      ▼
┌─────────────────┐
│   Job 1: build  │   ← Install deps + pytest + coverage
└────────┬────────┘
         │ needs: build
         ▼
┌──────────────────────┐
│  Job 2: sast-scan    │   ← Bandit SAST + Quality Gate
└──────────────────────┘
```

### Job 1 — `build`
- Set up Python 3.11
- Install dependencies dari `requirements.txt`
- Jalankan unit test dengan `pytest`
- Upload coverage report sebagai artifact

### Job 2 — `sast-scan`
- Bergantung pada keberhasilan Job 1 (`needs: build`)
- Jalankan **Bandit** untuk analisis keamanan statis seluruh folder `app/`
- Simpan laporan JSON sebagai artifact
- **Quality Gate**: pipeline gagal jika ditemukan issue severity HIGH

### Trigger
- `push` ke branch `main`
- `pull_request` ke branch `main`

---

## Kerentanan yang Sengaja Ditanamkan

| File | Kerentanan | Severity |
|------|-----------|---------|
| `routes.py` | SQL Injection (f-string query) | HIGH |
| `routes.py` | Command Injection (subprocess shell=True) | HIGH |
| `config.py` | Hardcoded secret key | MEDIUM |
| `utils.py` | Weak hash (SHA-256 tanpa salt) | MEDIUM |

> ⚠️ **Peringatan**: Aplikasi ini mengandung kerentanan yang disengaja untuk keperluan pembelajaran. **Jangan gunakan di production.**

---

*Dibuat untuk tugas praktikum DevSecOps — STT Terpadu Nurul Fikri 2026*
