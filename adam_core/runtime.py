from __future__ import annotations

import os
import secrets
from pathlib import Path


def persistent_root(base_dir: Path) -> Path:
    """Return Adam's per-user persistent data root."""
    local = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA")
    if local:
        return Path(local) / "Personal_AI_Assistant"
    return base_dir / ".runtime"


def load_or_create_flask_secret(base_dir: Path) -> str:
    """Use an environment secret or generate a persistent local secret.

    The previous build used a hard-coded fallback. Acquisition builds must
    never ship with a shared default session secret.
    """
    configured = os.getenv("FLASK_SECRET_KEY", "").strip()
    if configured and configured != "change-this-to-a-long-random-private-value":
        return configured

    root = persistent_root(base_dir)
    root.mkdir(parents=True, exist_ok=True)
    path = root / "flask_secret.key"
    try:
        existing = path.read_text(encoding="utf-8").strip()
        if len(existing) >= 32:
            return existing
    except FileNotFoundError:
        pass
    except Exception:
        # If persistent storage is unavailable, fall through to an ephemeral
        # cryptographically strong value rather than a predictable default.
        return secrets.token_urlsafe(48)

    generated = secrets.token_urlsafe(48)
    try:
        path.write_text(generated, encoding="utf-8")
        try:
            os.chmod(path, 0o600)
        except Exception:
            pass
    except Exception:
        pass
    return generated


def masked(value: str, visible: int = 3) -> str:
    value = str(value or "")
    if not value:
        return ""
    if len(value) <= visible * 2:
        return "*" * len(value)
    return f"{value[:visible]}…{value[-visible:]}"
