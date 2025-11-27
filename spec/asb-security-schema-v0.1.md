
# ASB Security Event Schema v0.1 – Specification

> A unified security event schema for LLM, RAG, and Agent applications.

This document defines **ASB Security Schema v0.1** – a JSON-based event model
for describing security-relevant actions and decisions in AI systems.

It is intended to be used by:

- AI security gateways and proxies (e.g., `asb-secure-gateway`)
- Application frameworks (Dify, LangChain, AutoGen, CrewAI, etc.)
- Policy engines (OPA / Rego, in-house PDPs)
- SIEM / observability / audit pipelines

The corresponding machine-readable JSON Schema is available at:

- [`schema/asb-security-schema-v0.1.json`](../schema/asb-security-schema-v0.1.json)

---

## 1. Goals and Non-Goals

### 1.1 Goals

The ASB Security Schema aims to:

1. Provide a **unified event model** for security-relevant behavior across:
   - LLM completions (chat / completion / embedding)
   - RAG (retrieval-augmented generation) queries
   - Agent tool / action executions

2. Enable **Policy-as-Code**, especially with OPA / Rego, by giving policies a
   consistent `input` structure.

3. Facilitate **logging, audit, and forensics** by standardizing the event
   content that flows into SIEM / data lakes.

4. Support both:
   - **Pre-decision events** (used as PDP `input`, before a decision)
   - **Post-decision events** (used for audit, after a decision / action)

### 1.2 Non-Goals

The schema does **not**:

- Define how policy engines MUST behave or how decisions MUST be made.
- Mandate any particular logging / transport mechanism (Kafka, HTTP, files, etc.).
- Attempt to enumerate all possible risk models or regulatory requirements.

It is a **data model**, not a full architecture.

---

## 2. Terminology and Conventions

- **MUST / MUST NOT / SHOULD / MAY** are to be interpreted as described in RFC 2119.
- **SecurityEvent** – a single JSON object describing a security-relevant action
  or decision, conforming to this schema.
- **Pre-decision event** – an event emitted before a policy decision is made
  (`operation.stage = "pre"`), typically used as the `input` of a PDP.
- **Post-decision event** – an event emitted after a decision or action
  (`operation.stage = "post"`), typically containing a populated `decision` object.

Field names in this document correspond to those in the JSON Schema.

Examples in this document are informative, not normative.

---

## 3. Top-Level Event Envelope

Every `SecurityEvent` **MUST** be a JSON object with the following top-level
structure:

```jsonc
{
  "schema_version": "asb-sec-0.1",
  "event_id": "uuid-1234",
  "timestamp": "2025-01-01T12:00:00Z",

  "tenant_id": "tenant-a",
  "app_id": "kb-copilot",
  "env": "prod",

  "subject":   { ... },
  "operation": { ... },
  "resource":  { ... },
  "context":   { ... },
  "decision":  { ... }
}
