"""Encrypted Microsoft token cache for deployments with an external Postgres DB.

Set MICROSOFT_DATABASE_URL in the server's environment. Use a dedicated
MICROSOFT_TOKEN_ENCRYPTION_KEY when available; otherwise derive one from the
owner password. Never place the database URL or secrets in source control.
"""
import base64
import hashlib
import os


def _configuration():
    url = os.getenv("MICROSOFT_DATABASE_URL", "").strip()
    if not url:
        return None
    key = os.getenv("MICROSOFT_TOKEN_ENCRYPTION_KEY", "").strip()
    if not key:
        owner_password = os.getenv("ADAM_OWNER_PASSWORD", "")
        if len(owner_password) < 20:
            raise RuntimeError("Set MICROSOFT_TOKEN_ENCRYPTION_KEY or a 20-character ADAM_OWNER_PASSWORD")
        derived = hashlib.pbkdf2_hmac(
            "sha256", owner_password.encode("utf-8"),
            b"adam-microsoft-token-cache-v1", 390000,
        )
        key = base64.urlsafe_b64encode(derived).decode("ascii")
    from cryptography.fernet import Fernet
    try:
        cipher = Fernet(key.encode("ascii"))
    except (ValueError, UnicodeEncodeError) as exc:
        raise RuntimeError("MICROSOFT_TOKEN_ENCRYPTION_KEY must be a Fernet key") from exc
    return url, cipher


def enabled():
    return bool(os.getenv("MICROSOFT_DATABASE_URL", "").strip())


def load():
    config = _configuration()
    if config is None:
        raise RuntimeError("Microsoft database is not configured")
    url, cipher = config
    import psycopg
    with psycopg.connect(url, connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS adam_microsoft_cache (id integer PRIMARY KEY CHECK (id = 1), ciphertext bytea NOT NULL)")
            cur.execute("SELECT ciphertext FROM adam_microsoft_cache WHERE id = 1")
            row = cur.fetchone()
    return cipher.decrypt(bytes(row[0])).decode("utf-8") if row else ""


def save(serialized):
    config = _configuration()
    if config is None:
        raise RuntimeError("Microsoft database is not configured")
    url, cipher = config
    import psycopg
    ciphertext = cipher.encrypt(serialized.encode("utf-8"))
    with psycopg.connect(url, connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS adam_microsoft_cache (id integer PRIMARY KEY CHECK (id = 1), ciphertext bytea NOT NULL)")
            cur.execute("INSERT INTO adam_microsoft_cache (id, ciphertext) VALUES (1, %s) ON CONFLICT (id) DO UPDATE SET ciphertext = EXCLUDED.ciphertext", (ciphertext,))


def clear():
    config = _configuration()
    if config is None:
        raise RuntimeError("Microsoft database is not configured")
    import psycopg
    with psycopg.connect(config[0], connect_timeout=10) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS adam_microsoft_cache (id integer PRIMARY KEY CHECK (id = 1), ciphertext bytea NOT NULL)")
            cur.execute("DELETE FROM adam_microsoft_cache WHERE id = 1")
