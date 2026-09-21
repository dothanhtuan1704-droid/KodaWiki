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

from kodawiki.wiki.ingester import WikiIngester
from kodawiki.sandbox.runner import SandboxRunner
from kodawiki.agents.state import KodaWikiState
from kodawiki.agents.planner import PlannerAgent
from kodawiki.agents.coder import CoderAgent
from kodawiki.agents.tester import TesterAgent
from kodawiki.agents.maintainer import WikiMaintainerAgent


def main():
    parser = argparse.ArgumentParser(
        description="KodaWiki - Autonomous Software Engineer & Living Codebase Knowledge Agent"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command: init
    init_parser = subparsers.add_parser(
        "init", help="Initialize .kodawiki Living Knowledge Base"
    )
    init_parser.add_argument(
        "--target-dir", default=".", help="Target project directory"
    )

    # Command: run
    run_parser = subparsers.add_parser(
        "run", help="Run KodaWiki agent on a coding prompt"
    )
    run_parser.add_argument("prompt", type=str, help="Coding task instruction")
    run_parser.add_argument(
        "--target-dir", default=".", help="Target project directory"
    )

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args.target_dir)
    elif args.command == "run":
        cmd_run(args.target_dir, args.prompt)
    else:
        parser.print_help()


def cmd_init(target_dir: str):
    target_dir = os.path.abspath(target_dir)
    print("=" * 60)
    print(" KodaWiki Living LLM Wiki Initializer")
    print(f" Target Repository: {target_dir}")
    print("=" * 60)

    ingester = WikiIngester(target_dir)
    wiki_path = ingester.init_wiki()

    print(f"\n[SUCCESS] Living Wiki initialized successfully at: {wiki_path}")
    print(
        f"  - Created .kodawiki/index.md (Catalog of codebase architecture)"
    )
    print(f"  - Created .kodawiki/log.md (Compounding activity log)")


def cmd_run(target_dir: str, prompt: str):
    target_dir = os.path.abspath(target_dir)
    print("=" * 60)
    print(" KodaWiki Agent Execution Flow")
    print(f" Prompt: '{prompt}'")
    print(f" Target Repository: {target_dir}")
    print("=" * 60)

    # 1. Init state
    state = KodaWikiState(target_dir=target_dir, user_prompt=prompt)

    # 2. Planner Step
    print("\n[Step 1] Planning Agent (Querying .kodawiki/index.md)...")
    planner = PlannerAgent(target_dir)
    state = planner.plan(state)

    print("\nGenerated Execution Plan:")
    for i, step in enumerate(state.plan_steps, 1):
        print(f"  {i}. {step}")

    # 3. Maintainer step
    maintainer = WikiMaintainerAgent(target_dir)
    state = maintainer.maintain(state)

    print("\n[SUCCESS] Task Execution & Wiki Maintenance Completed!")
    print(
        "  - Updated .kodawiki/index.md and logged event to .kodawiki/log.md"
    )


if __name__ == "__main__":
    main()
