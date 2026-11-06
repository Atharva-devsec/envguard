from envguard.envfile import parse_env


def test_parse_env_returns_names_and_empty_flags(env_fixture: str) -> None:
    parsed = parse_env(env_fixture)

    assert parsed == {
        "EMPTY": True,
        "QUOTED_EMPTY": True,
        "NONEMPTY": False,
        "EXPORTED": False,
        "SPACED_EMPTY": True,
    }
    assert "sensitive-value" not in repr(parsed)


def test_comments_and_malformed_lines_are_ignored() -> None:
    assert parse_env("# comment\nnot an assignment\n\n") == {}
