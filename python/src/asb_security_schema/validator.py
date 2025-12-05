"""Schema-based validation helpers."""

from __future__ import annotations

from functools import lru_cache
from typing import Any, Iterable, Mapping

from jsonschema import Draft7Validator, ValidationError

from .schema_loader import load_schema


@lru_cache(maxsize=1)
def _validator() -> Draft7Validator:
    return Draft7Validator(load_schema())


def validate_event(event: Mapping[str, Any]) -> Mapping[str, Any]:
    """Validate an event dict. Raises jsonschema.ValidationError when invalid."""
    _validator().validate(event)
    return event


def iter_errors(event: Mapping[str, Any]) -> Iterable[ValidationError]:
    """Yield all validation errors for an event without raising immediately."""
    return _validator().iter_errors(event)

