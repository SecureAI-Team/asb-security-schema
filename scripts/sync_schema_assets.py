#!/usr/bin/env python3
"""Synchronize schema artifacts into all SDKs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable


SCHEMA_FILENAME = "asb-security-schema-v0.1.json"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_bytes(path: Path) -> bytes:
    if not path.exists():
        raise FileNotFoundError(f"Schema source not found: {path}")
    return path.read_bytes()


def sync_file(source: Path, destination: Path) -> bool:
    destination.parent.mkdir(parents=True, exist_ok=True)
    src_bytes = read_bytes(source)
    if destination.exists() and destination.read_bytes() == src_bytes:
        return False
    destination.write_bytes(src_bytes)
    return True


def sync_python_sdk(root: Path) -> bool:
    dest = root / "python" / "src" / "asb_security_schema" / "data" / SCHEMA_FILENAME
    return sync_file(root / "schema" / SCHEMA_FILENAME, dest)


def sync_go_sdk(root: Path) -> bool:
    dest = root / "go" / "securityschema" / "schema" / SCHEMA_FILENAME
    return sync_file(root / "schema" / SCHEMA_FILENAME, dest)


def sync_all(root: Path) -> Iterable[str]:
    changed_targets: list[str] = []
    if sync_python_sdk(root):
        changed_targets.append("python")
    if sync_go_sdk(root):
        changed_targets.append("go")
    return changed_targets


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Sync schema assets into SDKs.")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if the generated files are not up to date.",
    )
    args = parser.parse_args(argv)

    root = repo_root()
    changed = list(sync_all(root))

    if args.check and changed:
        print(
            "Schema assets are out of sync for: "
            f"{', '.join(changed)}. Run this script without --check."
        )
        return 1

    if changed:
        print("Updated schema assets:", ", ".join(changed))
    else:
        print("Schema assets already up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

