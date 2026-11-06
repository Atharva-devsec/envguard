"""Parse dotenv files without retaining or returning their values."""

from __future__ import annotations

import re
from typing import Dict

_ASSIGNMENT = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")


def _value_is_empty(raw_value: str) -> bool:
    """Determine emptiness without exposing the value to callers."""
    value = raw_value.strip()
    if not value:
        return True

    quote: str | None = None
    escaped = False
    value_end = len(value)
    for index, character in enumerate(value):
        if escaped:
            escaped = False
            continue
        if character == "\\" and quote != "'":
            escaped = True
            continue
        if quote:
            if character == quote:
                quote = None
        elif character in ("'", '"'):
            quote = character
        elif character == "#" and index > 0 and value[index - 1].isspace():
            value_end = index
            break

    value = value[:value_end].strip()
    if len(value) >= 2 and value[0] in ("'", '"') and value[-1] == value[0]:
        value = value[1:-1]
    return value == ""


def parse_env(content: str) -> Dict[str, bool]:
    """Return ``{variable_name: is_empty}`` for assignments in dotenv content.

    Comments, blank lines, and malformed lines are ignored. Values are used only
    transiently to determine emptiness and are never included in the result.
    """
    variables: Dict[str, bool] = {}
    for line in content.splitlines():
        match = _ASSIGNMENT.match(line.strip())
        if match is None:
            continue
        name, raw_value = match.groups()
        variables[name] = _value_is_empty(raw_value)
    return variables
