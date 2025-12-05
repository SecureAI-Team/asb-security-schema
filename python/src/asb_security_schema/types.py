"""TypedDict helpers describing the schema structure."""

from __future__ import annotations

from typing import Dict, List, Literal, TypedDict


class User(TypedDict, total=False):
    id: str
    type: Literal["human", "service"]
    roles: List[str]
    groups: List[str]
    attributes: Dict[str, str]


class Agent(TypedDict, total=False):
    id: str
    type: str
    version: str


class Client(TypedDict, total=False):
    ip: str
    user_agent: str
    channel: Literal["web", "api", "cli", "batch", "other"]


class Subject(TypedDict, total=False):
    user: User
    agent: Agent
    client: Client


class Model(TypedDict, total=False):
    name: str
    provider: str
    mode: Literal["chat", "completion", "embedding", "other"]


class Operation(TypedDict, total=False):
    category: Literal["llm_completion", "rag_search", "agent_tool", "admin", "other"]
    name: str
    direction: Literal["input", "output", "both"]
    request_id: str
    stage: Literal["pre", "post"]
    model: Model


class Message(TypedDict, total=False):
    role: Literal["system", "user", "assistant", "tool", "other"]
    content: str


class LLMResource(TypedDict, total=False):
    messages: List[Message]
    input_tokens: float
    output_tokens_estimate: float
    output_tokens: float


class RAGCandidate(TypedDict, total=False):
    doc_id: str
    score: float
    metadata: Dict[str, object]


class RAGResource(TypedDict, total=False):
    query: str
    top_k: float
    vector_space: str
    filters: Dict[str, object]
    candidates: List[RAGCandidate]


class AgentToolResource(TypedDict, total=False):
    tool_name: str
    tool_category: str
    target_system: str
    args: Dict[str, object]


class Resource(TypedDict, total=False):
    llm: LLMResource
    rag: RAGResource
    agent_tool: AgentToolResource


class Context(TypedDict, total=False):
    trace_id: str
    span_id: str
    risk_signals: Dict[str, float]
    labels: Dict[str, str]
    metadata: Dict[str, object]


class DecisionAction(TypedDict, total=False):
    type: Literal["allow", "deny", "mask", "escalate", "log", "other"]
    details: Dict[str, object]


class Decision(TypedDict, total=False):
    result: Literal["allow", "deny", "mask", "escalate", "log", "other"]
    reason: str
    policy_id: str
    risk_level: Literal["low", "medium", "high", "critical"]
    score: float
    actions: List[DecisionAction]


class SecurityEvent(TypedDict, total=False):
    schema_version: str
    event_id: str
    timestamp: str
    tenant_id: str
    app_id: str
    env: str
    subject: Subject
    operation: Operation
    resource: Resource
    context: Context
    decision: Decision

