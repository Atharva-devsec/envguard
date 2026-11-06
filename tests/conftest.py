import pytest


@pytest.fixture

def env_fixture() -> str:
    return """# comment
EMPTY=
QUOTED_EMPTY=""
NONEMPTY='sensitive-value'
export EXPORTED=value # trailing comment
SPACED_EMPTY=   # empty after whitespace
"""
