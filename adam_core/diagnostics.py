from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any


def build_health_payload(*, base_dir: Path, version: str, app_name: str) -> dict[str, Any]:
    """Non-secret runtime status safe to show in a buyer/demo build."""
    data_dir = base_dir / "data"
    return {
        "ok": True,
        "ready": True,
        "product": app_name,
        "version": version,
        "channel": "acquisition",
        "python": sys.version.split()[0],
        "runtime": {
            "data_dir_available": data_dir.exists() and data_dir.is_dir(),
            "ai_provider_configured": bool(os.getenv("AI_API_KEY", "").strip()),
            "microsoft_client_configured": bool(os.getenv("MICROSOFT_CLIENT_ID", "").strip()),
            "whatsapp_configured": bool(
                os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip()
                and os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
            ),
            "alpaca_paper_configured": bool(
                os.getenv("ALPACA_API_KEY", "").strip()
                and os.getenv("ALPACA_SECRET_KEY", "").strip()
            ),
        },
        "safety": {
            "owner_approval_model": True,
            "live_trading_blocked": True,
            "hardcoded_flask_secret": False,
        },
    }
