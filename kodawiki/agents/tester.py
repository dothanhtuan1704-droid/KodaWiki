from kodawiki.agents.state import KodaWikiState
from kodawiki.sandbox.runner import SandboxRunner


class TesterAgent:
    """Executes tests using SandboxRunner."""

    def __init__(self, target_dir: str, use_docker: bool = False):
        self.runner = SandboxRunner(target_dir, use_docker=use_docker)

    def run(self, state: KodaWikiState) -> KodaWikiState:
        result = self.runner.run_tests("pytest")
        state.test_result = result
        if not result["success"]:
            state.retry_count += 1
            state.error_message = result["stderr"] or result["stdout"]
        else:
            state.is_complete = True
        return state
