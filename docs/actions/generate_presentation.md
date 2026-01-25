# Action Spec: generate_presentation(content_json)

## Overview
The `generate_presentation` action produces presentation artifacts (PPTX and/or PDF) from a structured content payload. It is intended to build investor/product decks with standardized mandatory slides.

## OpenAPI Manifest Reference
This action must be registered in the platform OpenAPI manifest (the unified spec used for Custom GPT Actions). Add/verify the `generate_presentation` operation under the `Analytics` tag with:

- **Operation ID**: `generate_presentation`
- **Request body schema**: `GeneratePresentationRequest` (defined below)
- **Response schema**: `GeneratePresentationResponse` (defined below)
- **Endpoint**: `POST /actions/generate_presentation`

If you are using the VASYA Gateway OpenAPI manifest, link the operation in that manifest so the action is discoverable in Custom GPT tooling. The manifest endpoint is commonly exposed as `http://unified-home-core:8080/openapi.json`.

## Input Schema (GeneratePresentationRequest)
The action accepts a single JSON object `content_json` that describes the deck structure, required slide types, and output options.

### JSON Schema (OpenAPI-compatible)
```json
{
  "type": "object",
  "required": ["content_json"],
  "properties": {
    "content_json": {
      "type": "object",
      "required": ["meta", "slides", "outputs"],
      "properties": {
        "meta": {
          "type": "object",
          "required": ["project", "language", "created_by"],
          "properties": {
            "project": {"type": "string"},
            "language": {"type": "string", "description": "IETF BCP-47 code, e.g. en, ru"},
            "created_by": {"type": "string"},
            "version": {"type": "string"}
          }
        },
        "brand": {
          "type": "object",
          "properties": {
            "theme": {"type": "string"},
            "logo_url": {"type": "string", "format": "uri"},
            "primary_color": {"type": "string"}
          }
        },
        "outputs": {
          "type": "object",
          "required": ["formats", "naming"],
          "properties": {
            "formats": {
              "type": "array",
              "items": {"type": "string", "enum": ["pptx", "pdf"]},
              "minItems": 1
            },
            "naming": {
              "type": "object",
              "required": ["pattern"],
              "properties": {
                "pattern": {"type": "string"},
                "timestamp": {"type": "string", "enum": ["utc", "local"]}
              }
            }
          }
        },
        "slides": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "object",
            "required": ["type", "title"],
            "properties": {
              "type": {
                "type": "string",
                "enum": [
                  "title",
                  "architecture",
                  "roadmap",
                  "financial_model",
                  "problem",
                  "solution",
                  "market",
                  "product",
                  "traction",
                  "team",
                  "appendix"
                ]
              },
              "title": {"type": "string"},
              "subtitle": {"type": "string"},
              "bullets": {"type": "array", "items": {"type": "string"}},
              "diagram": {
                "type": "object",
                "properties": {
                  "kind": {"type": "string", "enum": ["block", "flow", "timeline", "chart"]},
                  "data": {"type": "object"}
                }
              },
              "notes": {"type": "string"}
            }
          }
        }
      }
    }
  }
}
```

## Output Formats & Naming Convention
The action returns one or more files in the requested formats:

- **PPTX**: Editable PowerPoint deck.
- **PDF**: Print-ready export of the same deck.

### Naming Pattern
Use a deterministic filename that matches the `outputs.naming.pattern` template, with placeholders:

- `{project_slug}`: slugified project name (lowercase, hyphenated).
- `{date}`: `YYYY-MM-DD`.
- `{lang}`: language code (e.g., `en`, `ru`).
- `{format}`: `pptx` or `pdf`.

**Recommended pattern**:
```
{project_slug}_deck_{date}_{lang}.{format}
```

## Mandatory Slide Types
Every generated deck **must include** the following slide types at least once:

1. `title` — Title slide with project name and tagline.
2. `architecture` — System architecture diagram or block diagram.
3. `roadmap` — Timeline with milestones and quarters.
4. `financial_model` — Revenue/cost/GMV/Unit economics summary.

If any required type is missing, the action should return a validation error.

## Response Schema (GeneratePresentationResponse)
```json
{
  "type": "object",
  "required": ["status", "files"],
  "properties": {
    "status": {"type": "string", "enum": ["ok", "error"]},
    "files": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["format", "filename", "url"],
        "properties": {
          "format": {"type": "string", "enum": ["pptx", "pdf"]},
          "filename": {"type": "string"},
          "url": {"type": "string", "format": "uri"},
          "sha256": {"type": "string"}
        }
      }
    },
    "warnings": {"type": "array", "items": {"type": "string"}},
    "errors": {"type": "array", "items": {"type": "string"}}
  }
}
```

## Example Payloads

### Example 1: Full deck (PPTX + PDF)
```json
{
  "content_json": {
    "meta": {
      "project": "VASER Control Hub",
      "language": "ru",
      "created_by": "gpt-admin",
      "version": "1.0"
    },
    "brand": {
      "theme": "vaser-dark",
      "logo_url": "https://cdn.vaser.ai/brand/logo.png",
      "primary_color": "#3B82F6"
    },
    "outputs": {
      "formats": ["pptx", "pdf"],
      "naming": {
        "pattern": "{project_slug}_deck_{date}_{lang}.{format}",
        "timestamp": "utc"
      }
    },
    "slides": [
      {
        "type": "title",
        "title": "VASER Control Hub",
        "subtitle": "Unified infrastructure control plane"
      },
      {
        "type": "architecture",
        "title": "Architecture",
        "diagram": {
          "kind": "block",
          "data": {
            "nodes": ["GPT", "VASER Hub", "Devices", "Cloud APIs"],
            "edges": [["GPT", "VASER Hub"], ["VASER Hub", "Devices"], ["VASER Hub", "Cloud APIs"]]
          }
        }
      },
      {
        "type": "roadmap",
        "title": "Roadmap",
        "diagram": {
          "kind": "timeline",
          "data": {
            "milestones": [
              {"quarter": "Q1", "label": "MVP actions"},
              {"quarter": "Q2", "label": "Enterprise onboarding"}
            ]
          }
        }
      },
      {
        "type": "financial_model",
        "title": "Financial Model",
        "bullets": [
          "ARR target: $1.2M in year 2",
          "Gross margin: 72%",
          "CAC payback: 7 months"
        ]
      }
    ]
  }
}
```

### Example 2: Minimal required deck (PPTX only)
```json
{
  "content_json": {
    "meta": {
      "project": "VASER Router",
      "language": "en",
      "created_by": "gpt-admin"
    },
    "outputs": {
      "formats": ["pptx"],
      "naming": {
        "pattern": "{project_slug}_deck_{date}_{lang}.{format}",
        "timestamp": "local"
      }
    },
    "slides": [
      {"type": "title", "title": "VASER Router"},
      {"type": "architecture", "title": "Architecture"},
      {"type": "roadmap", "title": "Roadmap"},
      {"type": "financial_model", "title": "Financial Model"}
    ]
  }
}
```
