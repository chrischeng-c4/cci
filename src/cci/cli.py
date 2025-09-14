"""CCI Command Line Interface."""

from pathlib import Path
from typing import Optional, List

import typer
from rich import print
from rich.console import Console
from rich.table import Table

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


# Create a sub-application for worktree commands
worktree_app = typer.Typer(
    name="worktree",
    help="Manage git worktrees",
    add_completion=False,
)

app.add_typer(worktree_app, name="worktree")


@worktree_app.command(name="list")
def worktree_list(
    show_all: bool = typer.Option(False, "--all", "-a", help="Include main worktree"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed information"),
) -> None:
    """List all git worktrees for the current repository."""
    try:
        from cci.core.worktree import GitWorktree

        cwd = Path.cwd()
        worktree_manager = GitWorktree(cwd)

        worktrees = worktree_manager.list_worktrees(include_main=show_all)

        if not worktrees:
            console.print("[yellow]No worktrees found.[/yellow]")
            return

        if verbose:
            # Detailed table view
            table = Table(title="Git Worktrees", show_header=True, header_style="bold cyan")
            table.add_column("Path", style="green")
            table.add_column("Branch", style="yellow")
            table.add_column("Commit", style="dim")
            table.add_column("Status", style="cyan")
            table.add_column("Type", style="magenta")

            for wt in worktrees:
                wt_type = "main" if wt.is_main else "worktree"
                table.add_row(
                    str(wt.path),
                    wt.branch or "[detached]",
                    wt.commit[:8],
                    wt.status.value,
                    wt_type,
                )

            console.print(table)
        else:
            # Simple list view
            console.print("\n[bold cyan]Git Worktrees:[/bold cyan]\n")
            for wt in worktrees:
                icon = "🏠" if wt.is_main else "🌳"
                branch_info = f"({wt.branch})" if wt.branch else "[detached HEAD]"
                console.print(f"  {icon} {wt.path} {branch_info}")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to list worktrees: {e}")
        raise typer.Exit(1)


@worktree_app.command(name="create")
def worktree_create(
    path: Path = typer.Argument(..., help="Path where the worktree will be created"),
    branch: Optional[str] = typer.Option(None, "--branch", "-b", help="Existing branch to checkout"),
    new_branch: Optional[str] = typer.Option(None, "--new-branch", "-B", help="Create and checkout new branch"),
    force: bool = typer.Option(False, "--force", "-f", help="Force creation even if path exists"),
) -> None:
    """Create a new git worktree."""
    try:
        from cci.core.worktree import GitWorktree

        cwd = Path.cwd()
        worktree_manager = GitWorktree(cwd)

        console.print(f"[cyan]Creating worktree at:[/cyan] {path}")

        worktree_info = worktree_manager.create_worktree(
            path=path,
            branch=branch,
            new_branch=new_branch,
            force=force,
        )

        console.print(f"[green]✓[/green] Worktree created successfully!")
        console.print(f"  Path: {worktree_info.path}")
        if worktree_info.branch:
            console.print(f"  Branch: {worktree_info.branch}")
        console.print(f"  Commit: {worktree_info.commit[:8]}")

        console.print(f"\n[cyan]To work in this worktree:[/cyan]")
        console.print(f"  cd {worktree_info.path}")
        console.print(f"  cci")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to create worktree: {e}")
        raise typer.Exit(1)


@worktree_app.command(name="remove")
def worktree_remove(
    identifier: str = typer.Argument(..., help="Path or branch name of the worktree to remove"),
    force: bool = typer.Option(False, "--force", "-f", help="Force removal even with uncommitted changes"),
) -> None:
    """Remove a git worktree."""
    try:
        from cci.core.worktree import GitWorktree

        cwd = Path.cwd()
        worktree_manager = GitWorktree(cwd)

        # Get the worktree to confirm it exists
        worktree = worktree_manager.get_worktree(identifier)
        if not worktree:
            console.print(f"[red]Error:[/red] Worktree '{identifier}' not found")
            raise typer.Exit(1)

        # Confirm removal
        if not force:
            confirm = typer.confirm(f"Remove worktree at {worktree.path}?")
            if not confirm:
                console.print("[yellow]Cancelled[/yellow]")
                raise typer.Exit()

        worktree_manager.remove_worktree(identifier, force=force)
        console.print(f"[green]✓[/green] Worktree removed: {worktree.path}")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to remove worktree: {e}")
        raise typer.Exit(1)


@worktree_app.command(name="switch")
def worktree_switch(
    identifier: str = typer.Argument(..., help="Path or branch name of the worktree to switch to"),
) -> None:
    """Switch to a different worktree (shows path to cd to)."""
    try:
        from cci.core.worktree import GitWorktree

        cwd = Path.cwd()
        worktree_manager = GitWorktree(cwd)

        path = worktree_manager.switch_worktree(identifier)

        console.print(f"[green]Worktree found at:[/green] {path}")
        console.print(f"\n[cyan]To switch to this worktree, run:[/cyan]")
        console.print(f"  cd {path}")
        console.print(f"  cci")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to switch worktree: {e}")
        raise typer.Exit(1)


@worktree_app.command(name="prune")
def worktree_prune(
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Show what would be pruned without doing it"),
) -> None:
    """Prune worktrees that no longer exist on disk."""
    try:
        from cci.core.worktree import GitWorktree

        cwd = Path.cwd()
        worktree_manager = GitWorktree(cwd)

        pruned = worktree_manager.prune_worktrees(dry_run=dry_run)

        if not pruned:
            console.print("[green]No worktrees to prune.[/green]")
        else:
            action = "Would prune" if dry_run else "Pruned"
            console.print(f"[yellow]{action} {len(pruned)} worktree(s):[/yellow]")
            for path in pruned:
                console.print(f"  - {path}")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to prune worktrees: {e}")
        raise typer.Exit(1)


@worktree_app.command(name="lock")
def worktree_lock(
    identifier: str = typer.Argument(..., help="Path or branch name of the worktree to lock"),
    reason: Optional[str] = typer.Option(None, "--reason", "-r", help="Reason for locking"),
) -> None:
    """Lock a worktree to prevent automatic pruning."""
    try:
        from cci.core.worktree import GitWorktree

        cwd = Path.cwd()
        worktree_manager = GitWorktree(cwd)

        worktree_manager.lock_worktree(identifier, reason=reason)
        console.print(f"[green]✓[/green] Worktree locked: {identifier}")
        if reason:
            console.print(f"  Reason: {reason}")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to lock worktree: {e}")
        raise typer.Exit(1)


@worktree_app.command(name="unlock")
def worktree_unlock(
    identifier: str = typer.Argument(..., help="Path or branch name of the worktree to unlock"),
) -> None:
    """Unlock a previously locked worktree."""
    try:
        from cci.core.worktree import GitWorktree

        cwd = Path.cwd()
        worktree_manager = GitWorktree(cwd)

        worktree_manager.unlock_worktree(identifier)
        console.print(f"[green]✓[/green] Worktree unlocked: {identifier}")

    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] Failed to unlock worktree: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()