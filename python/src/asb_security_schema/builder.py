"""Convenience builder for assembling security events."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping, Optional

from .schema_loader import SCHEMA_VERSION
from .types import SecurityEvent
from .validator import validate_event


def _ts(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class SecurityEventBuilder:
    """Helper class for constructing schema-compliant security events."""

    subject: Mapping[str, Any]
    operation: Mapping[str, Any]
    resource: Mapping[str, Any]
    schema_version: str = SCHEMA_VERSION
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tenant_id: Optional[str] = None
    app_id: Optional[str] = None
    env: Optional[str] = None
    context: MutableMapping[str, Any] = field(default_factory=dict)
    decision: Optional[Mapping[str, Any]] = None
    extra: MutableMapping[str, Any] = field(default_factory=dict)

    def _base(self) -> SecurityEvent:
        event: SecurityEvent = {
            "schema_version": self.schema_version,
            "event_id": self.event_id,
            "timestamp": _ts(self.timestamp),
            "subject": dict(self.subject),
            "operation": dict(self.operation),
            "resource": dict(self.resource),
        }
        if self.tenant_id:
            event["tenant_id"] = self.tenant_id
        if self.app_id:
            event["app_id"] = self.app_id
        if self.env:
            event["env"] = self.env
        if self.context:
            event["context"] = dict(self.context)
        if self.decision:
            event["decision"] = dict(self.decision)
        if self.extra:
            event.update(self.extra)
        return event

    def build(self, *, validate: bool = True) -> SecurityEvent:
        """Return the assembled event. Optionally schema-validate before returning."""
        event = self._base()
        if validate:
            validate_event(event)
        return event

