package securityschema

import (
	"testing"
	"time"
)

func sampleEvent() map[string]any {
	return map[string]any{
		"schema_version": SchemaVersion,
		"event_id":       "event-123",
		"timestamp":      time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC).Format(time.RFC3339),
		"subject": map[string]any{
			"user": map[string]any{
				"id":   "user-123",
				"type": "human",
			},
		},
		"operation": map[string]any{
			"category":  "llm_completion",
			"name":      "chat_completion",
			"direction": "input",
			"model": map[string]any{
				"name": "gpt-4o",
			},
		},
		"resource": map[string]any{
			"llm": map[string]any{
				"messages": []any{
					map[string]any{"role": "user", "content": "hi"},
				},
			},
		},
	}
}

func TestValidateAcceptsValidPayload(t *testing.T) {
	if err := Validate(sampleEvent()); err != nil {
		t.Fatalf("expected valid payload: %v", err)
	}
}

func TestValidateRejectsInvalidPayload(t *testing.T) {
	evt := sampleEvent()
	delete(evt, "subject")
	if err := Validate(evt); err == nil {
		t.Fatalf("expected validation error")
	}
}
