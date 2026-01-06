import tomllib
from pathlib import Path

import typer

_config_file = Path(__file__).parent.parent / "pyproject.toml"
with _config_file.open("rb") as f:
    _config = tomllib.load(f)

_project_config = _config["project"]
_tool_config = _config["tool"]["config"]

CALENDAR_FILE = _tool_config["calendar_file"]
GOOGLE_CREDS_FILE = _tool_config["google_creds_file"]


# fmt: off
def config_cli(
    # Show all
    all: bool = typer.Option(False, "--all", help="Show all configuration values"),
    # Project keys
    project_name: bool = typer.Option(False, "--project-name", help=_project_config['name']),
    project_version: bool = typer.Option(False, "--project-version", help=_project_config['version']),
    # Application settings
    calendar_file: bool = typer.Option(False, "--calendar-file", help=CALENDAR_FILE),
    google_creds_file: bool = typer.Option(False, "--google-creds-file", help=GOOGLE_CREDS_FILE),
) -> None:
# fmt: on
    """Get configuration values from pyproject.toml."""
    # Show all configuration
    if all:
        typer.echo(f"project_name={_project_config['name']}")
        typer.echo(f"project_version={_project_config['version']}")
        typer.echo(f"calendar_file={CALENDAR_FILE}")
        typer.echo(f"google_creds_file={GOOGLE_CREDS_FILE}")
        return

    # Map parameters to their actual values
    param_map = {
        project_name: _project_config["name"],
        project_version: _project_config["version"],
        calendar_file: CALENDAR_FILE,
        google_creds_file: GOOGLE_CREDS_FILE,
    }

    for is_set, value in param_map.items():
        if is_set:
            typer.echo(value)
            return

    typer.secho(
        "Error: No config key specified. Use --help to see available options.",
        fg=typer.colors.RED,
        err=True,
    )
    raise typer.Exit(1)


def main():
    typer.run(config_cli)


if __name__ == "__main__":
    main()
