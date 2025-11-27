# ASB Security Schema

> A unified security event model for securing LLM, RAG, and Agent applications.  
> （面向 LLM / RAG / Agent 应用的统一安全事件模型）

ASB Security Schema defines a **canonical JSON structure** for AI security events:

- 🔒 Make AI security policies easier with **one standard `input`** for OPA / Policy-as-Code  
- 🧾 Standardize **logs & audit trails** for EU AI Act, ISO 27001, ISO 42001 and internal governance  
- 🧩 Works with **any LLM / RAG / Agent stack** – LangChain, Dify, AutoGen, CrewAI, custom apps…

This repo is a **specification repository**: it contains the **specification, JSON Schema, examples, and OPA policy samples**.  
Runtime components (such as `asb-secure-gateway`) use this schema as their **canonical event format**.

---

## Quick Links

- 📄 Spec: **[ASB Security Event Schema v0.1](spec/asb-security-schema-v0.1.md)**
- 🧬 JSON Schema: **[asb-security-schema-v0.1.json](schema/asb-security-schema-v0.1.json)**
- 🧪 Examples: **[examples/](examples/)** – LLM / RAG / Agent events  
- 🧯 Policies: **[policies/](policies/)** – OPA / Rego samples

For a Chinese overview, see **[README_zh.md](README_zh.md)**.

---

## What is this?

`asb-security-schema` is a **data model** for describing security-relevant actions in AI systems.

It defines:

- A common **ASB Security Schema** for:
  - LLM completions (chat / completion / embedding)
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
   - **Real-time enforcement** (pre- / post-decision events)
   - **Post-incident analysis** (rich context for investigations).

It is a **data model**, not a full security product or WAF / SIEM replacement.

---

## 2. Conceptual Model

At the core of this schema is a single object:

> **SecurityEvent** – a JSON document that describes one security-relevant action or decision in an AI system.

Every `SecurityEvent` answers the questions:

- **Who** did something? → `subject`
- **What** did they do? → `operation`
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
