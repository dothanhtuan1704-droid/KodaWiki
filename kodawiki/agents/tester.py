from kodawiki.agents.state import KodaWikiState
from kodawiki.sandbox.runner import SandboxRunner


class TesterAgent:
    """Executes tests using SandboxRunner."""

    def __init__(self, target_dir: str, use_docker: bool = False):
        self.runner = SandboxRunner(target_dir, use_docker=use_docker)

    def run(self, state: KodaWikiState) -> KodaWikiState:
        result = self.runner.run_tests("pytest")
        state.test_result = result
        
        # Check exit_code 0 for clean test execution pass
        if result.get("exit_code") == 0:
            state.is_complete = True
        else:
            state.retry_count += 1
            state.error_message = result.get("stderr") or result.get("stdout") or "Test failed"
            
        return state
