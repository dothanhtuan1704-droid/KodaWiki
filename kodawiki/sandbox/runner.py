import os
import subprocess
from typing import Dict, Any


class SandboxRunner:
    """Executes code tests inside an isolated Docker container or Subprocess environment."""

    def __init__(self, target_dir: str, use_docker: bool = False):
        self.target_dir = os.path.abspath(target_dir)
        self.use_docker = use_docker

    def run_tests(self, test_cmd: str = "pytest") -> Dict[str, Any]:
        """Runs test command and returns stdout, stderr, exit_code, and pass status."""
        if self.use_docker:
            return self._run_in_docker(test_cmd)
        else:
            return self._run_in_subprocess(test_cmd)

    def _run_in_subprocess(self, test_cmd: str) -> Dict[str, Any]:
        """Runs test command in isolated subprocess."""
        try:
            result = subprocess.run(
                test_cmd,
                shell=True,
                cwd=self.target_dir,
                capture_output=True,
                text=True,
                timeout=60,
            )

            passed = result.returncode == 0
            return {
                "success": passed,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "execution_mode": "subprocess",
            }
        except Exception as e:
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "",
                "stderr": str(e),
                "execution_mode": "subprocess",
            }

    def _run_in_docker(self, test_cmd: str) -> Dict[str, Any]:
        """Runs test command inside Docker Container."""
        try:
            import docker

            client = docker.from_env()
            container = client.containers.run(
                image="python:3.11-slim",
                command=f"bash -c 'pip install pytest && {test_cmd}'",
                volumes={self.target_dir: {"bind": "/app", "mode": "rw"}},
                working_dir="/app",
                detach=False,
                remove=True,
            )

            output = container.decode("utf-8")
            return {
                "success": True,
                "exit_code": 0,
                "stdout": output,
                "stderr": "",
                "execution_mode": "docker",
            }
        except Exception as e:
            # Fallback to subprocess if Docker is unavailable
            return self._run_in_subprocess(test_cmd)
