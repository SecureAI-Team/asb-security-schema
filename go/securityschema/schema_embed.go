package securityschema

import (
	_ "embed"
	"encoding/json"
	"fmt"
)

// SchemaVersion defines the currently bundled schema version.
const SchemaVersion = "asb-sec-0.1"

//go:embed schema/asb-security-schema-v0.1.json
var schemaJSON []byte

// SchemaBytes returns a copy of the raw JSON schema.
func SchemaBytes() []byte {
	out := make([]byte, len(schemaJSON))
	copy(out, schemaJSON)
	return out
}

// SchemaString returns the schema as a UTF-8 string.
func SchemaString() string {
	return string(schemaJSON)
}

// SchemaMap unmarshals the schema into a generic map.
func SchemaMap() (map[string]any, error) {
	var doc map[string]any
	if err := json.Unmarshal(schemaJSON, &doc); err != nil {
		return nil, fmt.Errorf("decode schema: %w", err)
	}
	return doc, nil
}
