import os
from kodawiki.agents.state import KodaWikiState


class CoderAgent:
    """Generates code changes and writes them to disk."""

    def __init__(self, target_dir: str):
        self.target_dir = target_dir

    def apply_code(self, state: KodaWikiState) -> KodaWikiState:
        # Write modified/generated files
        for rel_path, content in state.code_changes.items():
            full_path = os.path.join(self.target_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        return state
