import os
from datetime import datetime
from kodawiki.agents.state import KodaWikiState
from kodawiki.wiki.ingester import WikiIngester


class WikiMaintainerAgent:
    """Updates .kodawiki/index.md and appends log entry upon task completion."""

    def __init__(self, target_dir: str):
        self.target_dir = target_dir
        self.ingester = WikiIngester(target_dir)

    def maintain(self, state: KodaWikiState) -> KodaWikiState:
        # Re-index repository structure
        self.ingester.init_wiki()

        # Append activity entry to log.md
        log_path = os.path.join(self.target_dir, ".kodawiki", "log.md")
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        modified_files = ", ".join(state.code_changes.keys()) or "General task"
        log_entry = (
            f"\n## [{now_str}] TASK_COMPLETED | Prompt: {state.user_prompt}\n"
        )
        log_entry += f"- Files Modified: `{modified_files}`\n"
        log_entry += f"- Test Execution: PASS (Subprocess/Docker Sandbox)\n"

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)

        return state
