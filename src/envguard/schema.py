"""Load and validate env.schema.yaml files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

_ALLOWED_TYPES = {"string", "integer", "number", "boolean"}
_REQUIRED_FIELDS = {"type", "required", "secret", "description"}
_ALLOWED_FIELDS = _REQUIRED_FIELDS | {"default"}


class SchemaError(ValueError):
    """A schema is malformed or contains an unsupported definition."""


@dataclass(frozen=True)
class VariableSpec:
    name: str
    type: str
    required: bool
    default: Any
    secret: bool
    description: str


def load_schema(path: str | Path) -> Dict[str, VariableSpec]:
    """Load a schema, returning validated variable specs keyed by name.

    Errors intentionally avoid including YAML parser details or scalar values,
    so malformed schemas cannot accidentally expose secrets in diagnostics.
    """
    schema_path = Path(path)
    try:
        with schema_path.open("r", encoding="utf-8") as schema_file:
            document = yaml.safe_load(schema_file)
    except (OSError, UnicodeError, yaml.YAMLError):
        raise SchemaError("Unable to read or parse env schema.") from None

    if not isinstance(document, dict) or set(document) != {"variables"}:
        raise SchemaError("Schema must contain only a top-level 'variables' mapping.")
    definitions = document["variables"]
    if not isinstance(definitions, dict):
        raise SchemaError("Schema 'variables' must be a mapping.")

    result: Dict[str, VariableSpec] = {}
    for name, definition in definitions.items():
        if not isinstance(name, str) or not name or not name.replace("_", "a").isalnum() or name[0].isdigit():
            raise SchemaError("Variable names must be valid identifiers.")
        if not isinstance(definition, dict):
            raise SchemaError(f"Definition for {name} must be a mapping.")
        keys = set(definition)
        if not _REQUIRED_FIELDS.issubset(keys) or not keys.issubset(_ALLOWED_FIELDS):
            raise SchemaError(f"Definition for {name} has missing or unknown fields.")

        variable_type = definition["type"]
        required = definition["required"]
        secret = definition["secret"]
        description = definition["description"]
        default = definition.get("default")
        if variable_type not in _ALLOWED_TYPES:
            raise SchemaError(f"Definition for {name} has an unsupported type.")
        if not isinstance(required, bool) or not isinstance(secret, bool):
            raise SchemaError(f"Definition for {name} requires boolean required and secret fields.")
        if not isinstance(description, str):
            raise SchemaError(f"Definition for {name} requires a string description.")
        if secret and default is not None:
            raise SchemaError(f"Secret variable {name} cannot define a default.")
        if default is not None and not _matches_type(default, variable_type):
            raise SchemaError(f"Default for {name} does not match its declared type.")

        result[name] = VariableSpec(
            name=name,
            type=variable_type,
            required=required,
            default=default,
            secret=secret,
            description=description,
        )
    return result


def _matches_type(value: Any, variable_type: str) -> bool:
    if variable_type == "string":
        return isinstance(value, str)
    if variable_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if variable_type == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if variable_type == "boolean":
        return isinstance(value, bool)
    return False
