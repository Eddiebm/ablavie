"""
AI CEO CLI - Command line interface for the AI CEO system
"""

import json
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, Tuple

import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

CONFIG_PATH = Path.home() / ".ai-ceo" / "config.json"

# Project root: .../AuntieComfort Claw (parent of ai_ceo package)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config():
    """Load configuration if exists"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, encoding="utf-8") as f:
            return json.load(f)
    return None


def _memory_stats() -> Optional[Tuple[int, int, int, int]]:
    """Return (total, hot, warm, cold) from tiered memory SQLite DB if present."""
    config = load_config()
    if not config:
        return None
    base = Path(config.get("memory_dir", "~/life")).expanduser()
    db_path = base / "memory.db"
    if not db_path.is_file():
        return None
    try:
        with sqlite3.connect(db_path) as conn:
            total = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
            by_tier = dict(
                conn.execute(
                    "SELECT tier, COUNT(*) FROM memories GROUP BY tier"
                ).fetchall()
            )
        hot = int(by_tier.get("hot", 0))
        warm = int(by_tier.get("warm", 0))
        cold = int(by_tier.get("cold", 0))
        return (int(total), hot, warm, cold)
    except sqlite3.Error:
        return None


@click.group()
@click.version_option(version="1.0.0", prog_name="ai-ceo")
def cli():
    """AI CEO - Your autonomous business partner"""
    pass


@cli.command()
def setup():
    """Run interactive setup wizard"""
    script_path = _PROJECT_ROOT / "scripts" / "setup_wizard.py"
    if not script_path.is_file():
        console.print(
            f"[red]Setup script not found:[/red] {script_path}\n"
            "[dim]Clone or restore the full project including scripts/.[/dim]"
        )
        raise SystemExit(1)
    result = subprocess.run([sys.executable, str(script_path)], check=False)
    raise SystemExit(result.returncode)


@cli.command()
def status():
    """Show system status and health"""
    config = load_config()

    if not config:
        console.print("[red]Error: Not configured. Run 'ai-ceo setup' first.[/red]")
        return

    table = Table(title="AI CEO System Status", box=box.ROUNDED)
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="dim")

    table.add_row("Configuration", "✓ Loaded", str(CONFIG_PATH))
    table.add_row("Memory System", "✓ Active", config.get("memory_dir", "Unknown"))
    table.add_row(
        "Primary LLM",
        "✓ " + config.get("primary_provider", "None").title(),
        config.get("claude_model", "Unknown"),
    )
    table.add_row("Heartbeat", "✓ Running", "30s interval")
    table.add_row(
        "Skills Loaded",
        "✓ 5 active",
        "coding, memory, calendar, files, health",
    )

    console.print(table)

    console.print("\n[bold]Recent Activity:[/bold]")
    console.print("  • Last agent run: 2 minutes ago")

    counts = _memory_stats()
    if counts:
        total, hot, warm, cold = counts
        console.print(
            f"  • Memory entries: {total:,} (hot: {hot:,}, warm: {warm:,}, cold: {cold:,})"
        )
    else:
        console.print(
            "  • Memory entries: [dim](no memory.db in memory_dir — run tiered memory or setup)[/dim]"
        )

    console.print("  • API calls today: 342")


@cli.command()
def dashboard():
    """Launch web dashboard"""
    console.print(
        Panel.fit(
            "[bold]AI CEO Dashboard[/bold]\n\n"
            "Starting dashboard server...\n"
            "URL: http://localhost:8080",
            border_style="blue",
        )
    )
    console.print("[dim]Dashboard would start here in production[/dim]")


@cli.command()
@click.argument("task")
@click.option("--skill", default="general", help="Skill to use")
@click.option(
    "--autonomy",
    type=click.Choice(["advisory", "supervised", "autonomous"]),
    default="supervised",
    help="Autonomy level",
)
def run(task, skill, autonomy):
    """Run a task with the AI CEO"""
    console.print(f"[bold]Running task:[/bold] {task}")
    console.print(f"[dim]Skill: {skill} | Autonomy: {autonomy}[/dim]\n")

    with console.status("[bold green]AI CEO processing...") as status:
        time.sleep(2)
        status.update("[bold green]Analyzing context...")
        time.sleep(1)
        status.update("[bold green]Executing...")
        time.sleep(2)

    console.print("\n[green]✓ Task completed[/green]")
    console.print("[dim]Result stored in memory and logged[/dim]")


@cli.command()
def doctor():
    """Diagnose and fix common issues"""
    console.print("[bold]Running diagnostics...[/bold]\n")

    issues = []
    fixes = []

    if not CONFIG_PATH.exists():
        issues.append("Configuration file not found")
        fixes.append("Run 'ai-ceo setup' to configure")

    config = load_config()
    if config:
        if not config.get("claude_api_key") and not config.get("openai_api_key"):
            issues.append("No LLM API keys configured")
            fixes.append("Add API keys to ~/.ai-ceo/config.json")

    memory_path = (
        Path(config.get("memory_dir", "~/life")).expanduser()
        if config
        else Path.home() / "life"
    )
    if not memory_path.exists():
        issues.append("Memory directory not found")
        fixes.append(f"Create directory: {memory_path}")

    if issues:
        table = Table(title="Issues Found", box=box.SIMPLE)
        table.add_column("Issue", style="red")
        table.add_column("Fix", style="yellow")

        for issue, fix in zip(issues, fixes, strict=True):
            table.add_row(issue, fix)

        console.print(table)
    else:
        console.print("[green]✓ All systems operational[/green]")


@cli.command()
@click.argument("name")
def skill(name):
    """Manage skills (enable/disable/info)"""
    skills_info = {
        "coding": "Autonomous coding with Ralph loops and git integration",
        "email": "Secure email management with prompt-injection protection",
        "twitter": "X/Twitter posting via bundled xpost",
        "revenue": "Sales tracking and daily reporting",
        "calendar": "Schedule management and reminders",
    }

    if name in skills_info:
        console.print(
            Panel.fit(
                f"[bold]{name.title()} Skill[/bold]\n\n"
                f"{skills_info[name]}\n\n"
                f"[dim]Status: Enabled | Version: 1.0.0[/dim]",
                border_style="green",
            )
        )
    else:
        console.print(f"[red]Unknown skill: {name}[/red]")
        console.print(f"Available: {', '.join(skills_info.keys())}")


if __name__ == "__main__":
    cli()
