"""Load ASB Security Schema definitions bundled with the package."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from pathlib import Path
from typing import Any, Dict


SCHEMA_VERSION = "asb-sec-0.1"
SCHEMA_FILENAME = "asb-security-schema-v0.1.json"
_DATA_PACKAGE = "asb_security_schema.data"


def _from_package() -> bytes | None:
    try:
        return resources.read_binary(_DATA_PACKAGE, SCHEMA_FILENAME)
    except (FileNotFoundError, ModuleNotFoundError):
        return None


def _from_repo() -> bytes | None:
    repo_root = Path(__file__).resolve().parents[3]
    candidate = repo_root / "schema" / SCHEMA_FILENAME
    if candidate.exists():
        return candidate.read_bytes()
    return None


def schema_bytes() -> bytes:
    """Return the raw JSON Schema as bytes."""
    for loader in (_from_package, _from_repo):
        data = loader()
        if data:
            return data
    raise FileNotFoundError(
        f"Unable to locate {SCHEMA_FILENAME}. "
        "Run scripts/sync_schema_assets.py to regenerate package assets."
    )


def schema_text() -> str:
    """Return the schema as a UTF-8 string."""
    return schema_bytes().decode("utf-8")


@lru_cache(maxsize=1)
def load_schema() -> Dict[str, Any]:
    """Return the JSON schema as a Python dictionary."""
    return json.loads(schema_text())

