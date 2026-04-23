from app.core.config import parse_bool_env, parse_csv_env


def test_parse_csv_env_splits_and_trims_values():
    value = " http://localhost:5173, https://example.com ,, "

    assert parse_csv_env(value) == [
        "http://localhost:5173",
        "https://example.com",
    ]


def test_parse_csv_env_returns_empty_list_for_blank_values():
    assert parse_csv_env("") == []
    assert parse_csv_env(None) == []


def test_parse_bool_env_uses_default_for_missing_values():
    assert parse_bool_env(None, default=True) is True
    assert parse_bool_env(None, default=False) is False


def test_parse_bool_env_recognizes_common_truthy_values():
    assert parse_bool_env("true", default=False) is True
    assert parse_bool_env("YES", default=False) is True
    assert parse_bool_env("1", default=False) is True


def test_parse_bool_env_treats_other_values_as_false():
    assert parse_bool_env("false", default=True) is False
    assert parse_bool_env("0", default=True) is False
    assert parse_bool_env("off", default=True) is False