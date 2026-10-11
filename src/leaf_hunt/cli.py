"""Typer entry point. Commands land in later steps."""

from __future__ import annotations

import typer

from leaf_hunt import __version__
from leaf_hunt.config import load_config

app = typer.Typer(
    add_completion=False,
    help="Offline plant scavenger hunt. Designed to work with the screen off.",
)


@app.callback()
def main() -> None:
    """leaf-hunt — airplane-mode field companion."""


@app.command()
def version() -> None:
    """Print the package version."""
    typer.echo(__version__)


@app.command("config-path")
def config_path() -> None:
    """Print which config.toml would be used. Spoken later via TTS."""
    cfg = load_config()
    typer.echo(str(cfg.source_path))
