package securityschema

import "time"

// SecurityEvent represents the canonical ASB event envelope.
type SecurityEvent struct {
	SchemaVersion string    `json:"schema_version"`
	EventID       string    `json:"event_id"`
	Timestamp     time.Time `json:"timestamp"`
	TenantID      string    `json:"tenant_id,omitempty"`
	AppID         string    `json:"app_id,omitempty"`
	Env           string    `json:"env,omitempty"`
	Subject       Subject   `json:"subject"`
	Operation     Operation `json:"operation"`
	Resource      Resource  `json:"resource"`
	Context       *Context  `json:"context,omitempty"`
	Decision      *Decision `json:"decision,omitempty"`
}

type Subject struct {
	User   *User   `json:"user,omitempty"`
	Agent  *Agent  `json:"agent,omitempty"`
	Client *Client `json:"client,omitempty"`
}

type User struct {
	ID         string            `json:"id,omitempty"`
	Type       string            `json:"type,omitempty"`
	Roles      []string          `json:"roles,omitempty"`
	Groups     []string          `json:"groups,omitempty"`
	Attributes map[string]string `json:"attributes,omitempty"`
}

type Agent struct {
	ID      string `json:"id,omitempty"`
	Type    string `json:"type,omitempty"`
	Version string `json:"version,omitempty"`
}

type Client struct {
	IP        string `json:"ip,omitempty"`
	UserAgent string `json:"user_agent,omitempty"`
	Channel   string `json:"channel,omitempty"`
}

type Operation struct {
	Category  string `json:"category"`
	Name      string `json:"name"`
	Direction string `json:"direction"`
	RequestID string `json:"request_id,omitempty"`
	Stage     string `json:"stage,omitempty"`
	Model     *Model `json:"model,omitempty"`
}

type Model struct {
	Name     string `json:"name"`
	Provider string `json:"provider,omitempty"`
	Mode     string `json:"mode,omitempty"`
}

type Resource struct {
	LLM       *LLMResource       `json:"llm,omitempty"`
	RAG       *RAGResource       `json:"rag,omitempty"`
	AgentTool *AgentToolResource `json:"agent_tool,omitempty"`
}

type Message struct {
	Role    string `json:"role"`
	Content string `json:"content"`
}

type LLMResource struct {
	Messages        []Message      `json:"messages,omitempty"`
	InputTokens     float64        `json:"input_tokens,omitempty"`
	OutputTokens    float64        `json:"output_tokens,omitempty"`
	OutputTokensEst float64        `json:"output_tokens_estimate,omitempty"`
	Metadata        map[string]any `json:"metadata,omitempty"`
}

type RAGCandidate struct {
	DocID    string         `json:"doc_id"`
	Score    float64        `json:"score,omitempty"`
	Metadata map[string]any `json:"metadata,omitempty"`
}

type RAGResource struct {
	Query       string         `json:"query"`
	TopK        float64        `json:"top_k,omitempty"`
	VectorSpace string         `json:"vector_space,omitempty"`
	Filters     map[string]any `json:"filters,omitempty"`
	Candidates  []RAGCandidate `json:"candidates,omitempty"`
}

type AgentToolResource struct {
	ToolName     string         `json:"tool_name"`
	ToolCategory string         `json:"tool_category,omitempty"`
	TargetSystem string         `json:"target_system,omitempty"`
	Args         map[string]any `json:"args,omitempty"`
}

type Context struct {
	TraceID     string             `json:"trace_id,omitempty"`
	SpanID      string             `json:"span_id,omitempty"`
	RiskSignals map[string]float64 `json:"risk_signals,omitempty"`
	Labels      map[string]string  `json:"labels,omitempty"`
	Metadata    map[string]any     `json:"metadata,omitempty"`
}

type Decision struct {
	Result    string           `json:"result"`
	Reason    string           `json:"reason,omitempty"`
	PolicyID  string           `json:"policy_id,omitempty"`
	RiskLevel string           `json:"risk_level,omitempty"`
	Score     float64          `json:"score,omitempty"`
	Actions   []DecisionAction `json:"actions,omitempty"`
}

type DecisionAction struct {
	Type    string         `json:"type"`
	Details map[string]any `json:"details,omitempty"`
}
