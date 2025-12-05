from datetime import datetime, timezone

import pytest

from asb_security_schema import (
    SCHEMA_VERSION,
    SecurityEventBuilder,
    ValidationError,
    load_schema,
    validate_event,
)


def _sample_event():
    builder = SecurityEventBuilder(
        subject={"user": {"id": "user-123", "type": "human"}},
        operation={
            "category": "llm_completion",
            "name": "chat_completion",
            "direction": "input",
            "model": {"name": "gpt-4o"},
        },
        resource={
            "llm": {
                "messages": [
                    {"role": "system", "content": "You are a helper."},
                    {"role": "user", "content": "Hi"},
                ]
            }
        },
    )
    builder.timestamp = datetime(2024, 1, 1, tzinfo=timezone.utc)
    builder.tenant_id = "tenant-a"
    builder.env = "dev"
    return builder.build()


def test_load_schema_contains_const():
    schema = load_schema()
    assert (
        schema["properties"]["schema_version"]["const"] == SCHEMA_VERSION
    ), "schema version mismatch"


def test_validate_event_accepts_valid_payload():
    event = _sample_event()
    validate_event(event)


def test_validate_event_rejects_missing_required_fields():
    event = _sample_event()
    event.pop("subject")
    with pytest.raises(ValidationError):
        validate_event(event)

