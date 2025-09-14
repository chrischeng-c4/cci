"""CCI Command Line Interface."""

from pathlib import Path
from typing import Optional

import typer
from rich import print
from rich.console import Console

from cci import __version__

console = Console()
app = typer.Typer(
    name="cci",
    help="Claude Code IDE - Git worktree-first IDE with prompt-driven patch workflow",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        print(f"[cyan]CCI (Claude Code IDE)[/cyan] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """CCI - Claude Code IDE.

    A universal file and directory tool with AI-powered features.

    Usage:
        cci                 # Open current directory
        cci open file.txt   # Open a specific file
        cci open ~/project  # Open a directory
        cci open .          # Open current directory explicitly
        cci list            # List registered projects
        cci new <path>      # Create new project
    """
    pass


@app.command(name="open", context_settings={"allow_extra_args": False})
def open_command(
    path: Optional[Path] = typer.Argument(
        None,
        help="Path to open. Can be a file or directory. Defaults to current directory.",
    ),
) -> None:
    """Open a file or directory in CCI."""
    if path:
        if not path.exists():
            console.print(f"[red]Error:[/red] Path '{path}' does not exist")
            raise typer.Exit(1)

        target_path = path.resolve()

        if target_path.is_file():
            console.print(f"[green]Opening file:[/green] {target_path}")
            from cci.tui.app import CCIApp
            app = CCIApp(file_path=target_path)
            app.run()
        else:
            console.print(f"[green]Opening directory:[/green] {target_path}")
            from cci.tui.app import CCIApp
            app = CCIApp(directory_path=target_path)
            app.run()
    else:
        # No path provided, open current directory
        console.print(f"[green]Opening current directory:[/green] {Path.cwd()}")
        from cci.tui.app import CCIApp
        app = CCIApp(directory_path=Path.cwd())
        app.run()


@app.command()
def new(
    path: Path = typer.Argument(..., help="Path where the new project will be created"),
    name: Optional[str] = typer.Option(None, "--name", "-n", help="Project name"),
) -> None:
    """Create a new project."""
    project_name = name or path.name

    if path.exists():
        console.print(f"[red]Error:[/red] Path '{path}' already exists")
        raise typer.Exit(1)

    console.print(f"[green]Creating new project:[/green] {project_name} at {path.resolve()}")

    # Create project directory
    path.mkdir(parents=True, exist_ok=True)

    # Initialize git repository
    import subprocess
    try:
        subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
        console.print("[green]✓[/green] Git repository initialized")
    except subprocess.CalledProcessError as e:
        console.print(f"[yellow]Warning:[/yellow] Failed to initialize git: {e}")

    # Create .cci directory for project-specific configuration
    cci_dir = path / ".cci"
    cci_dir.mkdir(exist_ok=True)

    # Create project config
    config_file = cci_dir / "config.toml"
    config_content = f"""[project]
name = "{project_name}"
description = ""
worktree_path = ".cci/worktrees"

[prompt]
max_context_files = 20
include_patterns = ["*.py", "*.md"]
exclude_patterns = ["__pycache__", "*.pyc"]

[workflow]
auto_commit = false
require_tests = true
require_review = true
"""
    config_file.write_text(config_content)
    console.print("[green]✓[/green] Project configuration created")

    # Register project
    from cci.core.registry import ProjectRegistry
    registry = ProjectRegistry()
    registry.add_project(project_name, path)
    console.print("[green]✓[/green] Project registered")

    console.print(f"\n[green]Project '{project_name}' created successfully![/green]")
    console.print(f"Run [cyan]cci open {path}[/cyan] to start working on it.")


@app.command()
def list() -> None:
    """List all registered projects (optional feature)."""
    try:
        from cci.core.registry import ProjectRegistry

        registry = ProjectRegistry()
        projects = registry.list_projects()

        if not projects:
            console.print("[yellow]No projects registered yet.[/yellow]")
            console.print("Tip: CCI can open any file or directory directly:")
            console.print("  [cyan]cci ~/Documents[/cyan] - Open a directory")
            console.print("  [cyan]cci file.txt[/cyan] - Open a file")
            return

        console.print("\n[bold cyan]Registered Projects:[/bold cyan]\n")

        for project in projects:
            console.print(f"  📁 [green]{project.name}[/green]")
            console.print(f"     Path: {project.path}")
            console.print(f"     Last opened: {project.last_opened.strftime('%Y-%m-%d %H:%M')}")
            if project.description:
                console.print(f"     Description: {project.description}")
            console.print()
    except Exception as e:
        console.print(f"[yellow]Project registry not available:[/yellow] {e}")
        console.print("\nCCI works with any file or directory:")
        console.print("  [cyan]cci[/cyan] - Open current directory")
        console.print("  [cyan]cci file.txt[/cyan] - Open a file")
        console.print("  [cyan]cci ~/folder[/cyan] - Open a folder")


@app.command()
def remove(
    name: str = typer.Argument(..., help="Name of the project to remove from registry"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Remove a project from the registry (does not delete files)."""
    from cci.core.registry import ProjectRegistry

    registry = ProjectRegistry()

    if not force:
        confirm = typer.confirm(f"Remove project '{name}' from registry?")
        if not confirm:
            console.print("[yellow]Cancelled[/yellow]")
            raise typer.Exit()

    if registry.remove_project(name):
        console.print(f"[green]✓[/green] Project '{name}' removed from registry")
    else:
        console.print(f"[red]Error:[/red] Project '{name}' not found")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()