# asb-security-schema

> A unified security event schema for LLM, RAG, and Agent applications.

`asb-security-schema` is a **specification repository** for describing security-relevant events in AI systems.

It defines:

- A common **ASB Security Schema** for:
  - LLM completions (chat / completion)
  - RAG (Retrieval-Augmented Generation) queries
  - Agent tool / action executions
- A set of **JSON examples** for typical events
- A few **OPA (Open Policy Agent) policy samples** that consume this schema

This repo does **not** implement a gateway itself.  
Runtime components such as `asb-secure-gateway` use this schema as the **canonical input** for:

- Policy decisions (allow / deny / mask / escalate)
- Audit logs and forensic analysis
- Compliance and reporting (e.g., EU AI Act, internal governance)

---

## 1. Goals

The ASB Security Schema aims to:

1. **Standardize** how AI security events are represented across LLM, RAG, and Agent use cases.
2. Enable **Policy-as-Code** using engines like OPA, by providing a consistent `input` shape.
3. Make it easier to export AI security events into **SIEM / observability / audit** systems.
4. Support both:
   - **Real-time enforcement** (pre- / post- decision events)
   - **Post-incident analysis** (rich context for investigations).

---

## 2. Conceptual Model

At the core of this schema is a single object:

> **SecurityEvent** – a JSON document that describes one security-relevant action or decision in an AI system.

Every `SecurityEvent` answers the questions:

- **Who** is doing something? → `subject`
- **What** are they doing? → `operation`
- **On what** resource? → `resource`
- In which **context**? → `context`
- With which **decision** and risk level? → `decision` (optional for pre-decision events)

---

## 3. Top-Level Structure (v0.1)

All events follow this envelope:

```jsonc
{
  "schema_version": "asb-sec-0.1",
  "event_id": "uuid-1234",
  "timestamp": "2025-01-01T12:00:00Z",

  "tenant_id": "tenant-a",
  "app_id": "kb-copilot",
  "env": "prod",  // dev | test | prod

  "subject":   { /* who */ },
  "operation": { /* what */ },
  "resource":  { /* on what */ },
  "context":   { /* extra context */ },
  "decision":  { /* policy result (optional) */ }
}
