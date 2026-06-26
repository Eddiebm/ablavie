#!/usr/bin/env python3
"""Interactive setup for AI CEO — writes ~/.ai-ceo/config.json"""

import json
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm, Prompt

console = Console()

DEFAULT_DIR = Path.home() / "life"


def main() -> None:
    console.print("[bold]AI CEO setup[/bold]\n")

    config_dir = Path.home() / ".ai-ceo"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"

    memory_dir = Prompt.ask(
        "Memory directory (tiered memory DB lives here)",
        default=str(DEFAULT_DIR),
    )
    memory_path = Path(memory_dir).expanduser()
    memory_path.mkdir(parents=True, exist_ok=True)

    primary = Prompt.ask(
        "Primary LLM provider",
        choices=["claude", "openai"],
        default="claude",
    )

    claude_model = "claude-sonnet-4-20250514"
    openai_model = "gpt-4.1"
    if primary == "claude":
        claude_model = Prompt.ask("Claude model id", default=claude_model)
        claude_key = Prompt.ask("Anthropic API key", password=True)
        openai_key = ""
    else:
        openai_model = Prompt.ask("OpenAI model id", default=openai_model)
        openai_key = Prompt.ask("OpenAI API key", password=True)
        claude_key = ""

    config = {
        "memory_dir": str(memory_path),
        "primary_provider": primary,
        "claude_model": claude_model,
        "openai_model": openai_model,
        "claude_api_key": claude_key,
        "openai_api_key": openai_key,
        "created_at": datetime.now().isoformat(),
    }

    if config_path.exists() and not Confirm.ask(f"Overwrite {config_path}?", default=False):
        console.print("[yellow]Aborted.[/yellow]")
        return

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    # Restrict permissions on Unix (best-effort)
    try:
        config_path.chmod(0o600)
    except OSError:
        pass

    console.print(f"\n[green]Wrote[/green] {config_path}")
    console.print("[dim]Run: ai-ceo status[/dim]")


if __name__ == "__main__":
    main()
