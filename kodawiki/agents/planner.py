import os
from kodawiki.agents.state import KodaWikiState


class PlannerAgent:
    """Reads .kodawiki/index.md and generates an action plan."""

    def __init__(self, target_dir: str):
        self.target_dir = target_dir

    def plan(self, state: KodaWikiState) -> KodaWikiState:
        index_path = os.path.join(self.target_dir, ".kodawiki", "index.md")
        wiki_text = ""
        if os.path.exists(index_path):
            with open(index_path, "r", encoding="utf-8") as f:
                wiki_text = f.read()

        state.wiki_context = wiki_text

        # Heuristic / Prompt planner logic
        state.plan_steps = [
            f"Analyze user request: '{state.user_prompt}'",
            "Generate/modify Python source file and corresponding test",
            "Run test suite in Sandbox",
            "Update .kodawiki knowledge base and log entry",
        ]

        return state
