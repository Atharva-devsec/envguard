from pathlib import Path

import pytest

from envguard.schema import SchemaError, load_schema


def test_load_schema_validates_and_returns_specs(schema_fixture: Path) -> None:
    schema = load_schema(schema_fixture)

    assert set(schema) == {"API_TOKEN", "DEBUG"}
    assert schema["API_TOKEN"].secret is True
    assert schema["API_TOKEN"].default is None
    assert schema["DEBUG"].default is False


def test_secret_default_is_rejected(secret_default_schema: Path) -> None:
    with pytest.raises(SchemaError, match="cannot define a default"):
        load_schema(secret_default_schema)


def test_invalid_schema_structure_is_rejected(tmp_path: Path) -> None:
    schema_path = tmp_path / "bad.yaml"
    schema_path.write_text("variables: []\n", encoding="utf-8")

    with pytest.raises(SchemaError, match="mapping"):
        load_schema(schema_path)


def test_parse_error_does_not_echo_schema_content(tmp_path: Path) -> None:
    schema_path = tmp_path / "bad.yaml"
    schema_path.write_text("private-value: [\n", encoding="utf-8")

    with pytest.raises(SchemaError) as error:
        load_schema(schema_path)
    assert "private-value" not in str(error.value)
