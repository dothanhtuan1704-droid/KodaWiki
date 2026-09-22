import argparse
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

from kodawiki.wiki.ingester import WikiIngester
from kodawiki.sandbox.runner import SandboxRunner
from kodawiki.agents.state import KodaWikiState
from kodawiki.agents.planner import PlannerAgent
from kodawiki.agents.coder import CoderAgent
from kodawiki.agents.tester import TesterAgent
from kodawiki.agents.maintainer import WikiMaintainerAgent

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="KodaWiki CLI - Autonomous Software Engineer & Living Codebase Knowledge Agent"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command 1: init
    init_parser = subparsers.add_parser(
        "init", help="Initialize .kodawiki Living Knowledge Base"
    )
    init_parser.add_argument(
        "--target-dir", default=".", help="Target project directory"
    )

    # Command 2: run
    run_parser = subparsers.add_parser(
        "run", help="Run KodaWiki agent on a coding prompt"
    )
    run_parser.add_argument("prompt", type=str, help="Coding task instruction")
    run_parser.add_argument(
        "--target-dir", default=".", help="Target project directory"
    )
    run_parser.add_argument(
        "--provider", default="openai", help="LLM provider (openai|anthropic|ollama)"
    )
    run_parser.add_argument(
        "--model", default="gpt-4o", help="Model name (gpt-4o|claude-3-5-sonnet|deepseek-coder)"
    )

    # Command 3: sync
    sync_parser = subparsers.add_parser(
        "sync", help="Force sync .kodawiki Living Knowledge Base with current git diff"
    )
    sync_parser.add_argument(
        "--target-dir", default=".", help="Target project directory"
    )

    # Command 4: status
    status_parser = subparsers.add_parser(
        "status", help="Show KodaWiki knowledge base status and recent log history"
    )
    status_parser.add_argument(
        "--target-dir", default=".", help="Target project directory"
    )

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args.target_dir)
    elif args.command == "run":
        cmd_run(args.target_dir, args.prompt, args.provider, args.model)
    elif args.command == "sync":
        cmd_sync(args.target_dir)
    elif args.command == "status":
        cmd_status(args.target_dir)
    else:
        parser.print_help()


def cmd_init(target_dir: str):
    target_dir = os.path.abspath(target_dir)
    console.print(
        Panel.fit(
            f"[bold cyan]🧠 KodaWiki Living LLM Wiki Initializer[/bold cyan]\nTarget Repository: [green]{target_dir}[/green]",
            border_style="cyan"
        )
    )

    ingester = WikiIngester(target_dir)
    wiki_path = ingester.init_wiki()

    console.print(f"\n[bold green]✓ Living Wiki initialized successfully at:[/bold green] [yellow]{wiki_path}[/yellow]")
    console.print("  • Created [bold].kodawiki/index.md[/bold] (Catalog of code architecture)")
    console.print("  • Created [bold].kodawiki/log.md[/bold] (Compounding activity log)")


def cmd_run(target_dir: str, prompt: str, provider: str, model: str):
    target_dir = os.path.abspath(target_dir)
    console.print(
        Panel.fit(
            f"[bold cyan]🤖 KodaWiki End-to-End Agent Execution Flow[/bold cyan]\n"
            f"Prompt: [yellow]'{prompt}'[/yellow]\n"
            f"Provider: [magenta]{provider}[/magenta] | Model: [magenta]{model}[/magenta]\n"
            f"Repository: [green]{target_dir}[/green]",
            border_style="blue"
        )
    )

    # 1. Init state
    state = KodaWikiState(target_dir=target_dir, user_prompt=prompt)

    # 2. Planner Agent (Queries Wiki)
    console.print("\n[bold blue][Step 1/4] 📋 Planner Agent (Querying .kodawiki/index.md)...[/bold blue]")
    planner = PlannerAgent(target_dir)
    state = planner.plan(state)

    table = Table(title="Generated Execution Plan", show_header=True, header_style="bold magenta")
    table.add_column("Step", style="cyan", width=6)
    table.add_column("Instruction", style="white")

    for i, step in enumerate(state.plan_steps, 1):
        table.add_row(str(i), step)

    console.print(table)

    # 3. Coder Agent (Modifies Code)
    console.print("\n[bold blue][Step 2/4] 💻 Coder Agent (Writing code & test to disk)...[/bold blue]")
    coder = CoderAgent(target_dir)
    state = coder.apply_code(state)

    for rel_file, content in state.code_changes.items():
        console.print(f"  [bold green]+ Modified file:[/bold green] [yellow]{rel_file}[/yellow]")

    # 4. Tester Agent (Runs Sandbox Test)
    console.print("\n[bold blue][Step 3/4] 🐳 Tester Agent (Executing pytest in Sandbox)...[/bold blue]")
    tester = TesterAgent(target_dir, use_docker=False)
    state = tester.run(state)

    if state.test_result and state.test_result.get("exit_code") == 0:
        console.print("  [bold green]🟢 Sandbox Test Status: PASS 100%[/bold green]")
    else:
        console.print(f"  [bold red]🔴 Sandbox Test Status: FAIL ({state.error_message})[/bold red]")

    # 5. Wiki Maintainer Agent (Auto Updates Wiki)
    console.print("\n[bold blue][Step 4/4] 📝 Wiki Maintainer Agent (Updating .kodawiki/ & log.md)...[/bold blue]")
    maintainer = WikiMaintainerAgent(target_dir)
    state = maintainer.maintain(state)

    console.print(
        Panel.fit(
            "[bold green]✨ SUCCESS: Task Execution & Wiki Maintenance Completed![/bold green]\n"
            "  • Updated [bold].kodawiki/index.md[/bold]\n"
            "  • Logged activity event to [bold].kodawiki/log.md[/bold]",
            border_style="green"
        )
    )


def cmd_sync(target_dir: str):
    target_dir = os.path.abspath(target_dir)
    console.print(
        Panel.fit(
            f"[bold cyan]🔄 KodaWiki Knowledge Sync Engine[/bold cyan]\nTarget Repository: [green]{target_dir}[/green]",
            border_style="yellow"
        )
    )

    ingester = WikiIngester(target_dir)
    wiki_path = ingester.init_wiki()

    console.print(f"\n[bold green]✓ Re-synced .kodawiki/ index with current repository files![/bold green]")


def cmd_status(target_dir: str):
    target_dir = os.path.abspath(target_dir)
    wiki_dir = os.path.join(target_dir, ".kodawiki")
    log_path = os.path.join(wiki_dir, "log.md")

    console.print(
        Panel.fit(
            f"[bold cyan]📊 KodaWiki Status & Knowledge Summary[/bold cyan]\nTarget Repository: [green]{target_dir}[/green]",
            border_style="cyan"
        )
    )

    if not os.path.exists(wiki_dir):
        console.print("[bold red]❌ .kodawiki/ directory not found. Please run 'kodawiki init' first.[/bold red]")
        return

    console.print(f"  • Knowledge Base Location: [yellow]{wiki_dir}[/yellow]")
    
    if os.path.exists(log_path):
        console.print("\n[bold yellow]📜 Recent Activity Logs (.kodawiki/log.md):[/bold yellow]")
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            recent_logs = [line.strip() for line in lines if line.startswith("## [")][-5:]
            for log_entry in recent_logs:
                console.print(f"  {log_entry}")


if __name__ == "__main__":
    main()
