package securityschema

import (
	"bytes"
	"encoding/json"
	"fmt"
	"sync"

	"github.com/santhosh-tekuri/jsonschema/v5"
)

var (
	schemaOnce sync.Once
	schemaErr  error
	compiled   *jsonschema.Schema
)

func validator() (*jsonschema.Schema, error) {
	schemaOnce.Do(func() {
		compiler := jsonschema.NewCompiler()
		if err := compiler.AddResource("schema.json", bytes.NewReader(schemaJSON)); err != nil {
			schemaErr = fmt.Errorf("add schema resource: %w", err)
			return
		}
		if compiledSchema, err := compiler.Compile("schema.json"); err != nil {
			schemaErr = fmt.Errorf("compile schema: %w", err)
		} else {
			compiled = compiledSchema
		}
	})
	return compiled, schemaErr
}

// Validate ensures the supplied event matches the ASB schema.
func Validate(event any) error {
	v, err := validator()
	if err != nil {
		return err
	}
	return v.Validate(event)
}

// ValidateBytes decodes JSON and validates it.
func ValidateBytes(payload []byte) error {
	var event any
	if err := json.Unmarshal(payload, &event); err != nil {
		return fmt.Errorf("decode json: %w", err)
	}
	return Validate(event)
}

// MustValidate panics when validation fails. Useful in tests.
func MustValidate(event any) {
	if err := Validate(event); err != nil {
		panic(err)
	}
}
