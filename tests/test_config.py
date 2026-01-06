"""Tests for the configuration module."""

import pytest
import typer
from typer.testing import CliRunner

from src.config import config_cli

app = typer.Typer()
app.command()(config_cli)

runner = CliRunner()


@pytest.mark.parametrize(
    "flag,expected_output",
    [
        ("--project-name", "certificate-expiration"),
        ("--project-version", "0.1.0"),
        ("--calendar-file", "app_calendar_events.json"),
    ],
)
def test_config_returns_single_value(flag: str, expected_output: str):
    """Test that individual flags return their correct values."""
    result = runner.invoke(app, [flag])

    assert result.exit_code == 0
    assert result.stdout.strip() == expected_output


def test_config_all_returns_all_values():
    """Test that --all flag returns all configuration values."""
    result = runner.invoke(app, ["--all"])

    assert result.exit_code == 0
    assert "project_name=certificate-expiration" in result.stdout
    assert "calendar_file=" in result.stdout


def test_config_without_flag_fails():
    """Test that calling config without any flag produces an error."""
    result = runner.invoke(app, [])

    assert result.exit_code == 1
    assert "Error: No config key specified" in result.output
