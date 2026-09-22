import os
from kodawiki.agents.state import KodaWikiState


class CoderAgent:
    """Generates code changes and writes them to disk."""

    def __init__(self, target_dir: str):
        self.target_dir = target_dir

    def apply_code(self, state: KodaWikiState) -> KodaWikiState:
        # Simulate code generation logic based on user prompt
        if "multiply" in state.user_prompt.lower():
            calc_path = os.path.join(self.target_dir, "calculator.py")
            test_path = os.path.join(self.target_dir, "test_calculator.py")

            if os.path.exists(calc_path):
                with open(calc_path, "r", encoding="utf-8") as f:
                    calc_content = f.read()
                if "def multiply" not in calc_content:
                    calc_content += (
                        "\n\ndef multiply(a: float, b: float) -> float:\n"
                    )
                    calc_content += "    \"\"\"Multiplies two numbers.\"\"\"\n"
                    calc_content += "    return a * b\n"
                    state.code_changes["calculator.py"] = calc_content

            if os.path.exists(test_path):
                with open(test_path, "r", encoding="utf-8") as f:
                    test_content = f.read()
                if "from calculator import add, subtract, multiply" not in test_content:
                    test_content = test_content.replace(
                        "from calculator import add, subtract",
                        "from calculator import add, subtract, multiply",
                    )
                if "test_multiply" not in test_content:
                    test_content += "\n\ndef test_multiply():\n"
                    test_content += "    assert multiply(3, 4) == 12\n"
                state.code_changes["test_calculator.py"] = test_content

        # Write all code changes to disk
        for rel_path, content in state.code_changes.items():
            full_path = os.path.join(self.target_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)

        return state
