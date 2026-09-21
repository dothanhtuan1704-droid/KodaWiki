import os
import ast
from datetime import datetime
from typing import Dict, List, Any


class WikiIngester:
    """Scans codebase files and compiles/maintains the persistent .kodawiki knowledge base."""

    def __init__(self, target_dir: str):
        self.target_dir = os.path.abspath(target_dir)
        self.wiki_dir = os.path.join(self.target_dir, ".kodawiki")
        self.modules_dir = os.path.join(self.wiki_dir, "modules")

    def init_wiki(self) -> str:
        """Initializes the .kodawiki directory structure and index.md file."""
        os.makedirs(self.wiki_dir, exist_ok=True)
        os.makedirs(self.modules_dir, exist_ok=True)

        index_path = os.path.join(self.wiki_dir, "index.md")
        log_path = os.path.join(self.wiki_dir, "log.md")

        # Scan code files
        code_structure = self._scan_repository()

        # Build index.md content
        index_content = self._generate_index_md(code_structure)
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(index_content)

        # Build initial log.md
        if not os.path.exists(log_path):
            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_content = f"# 📜 KodaWiki Activity Log\n\n## [{now_str}] INIT | Initialized Living Wiki Knowledge Base for {os.path.basename(self.target_dir)}\n- Scanned {len(code_structure)} files.\n"
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(log_content)

        return self.wiki_dir

    def _scan_repository(self) -> List[Dict[str, Any]]:
        """Scans python files and parses AST to discover classes, functions, and docstrings."""
        code_info = []
        ignore_dirs = {
            ".git",
            "venv",
            "__pycache__",
            ".kodawiki",
            "node_modules",
            "brain",
        }

        for root, dirs, files in os.walk(self.target_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.target_dir)
                    info = self._parse_python_file(full_path, rel_path)
                    code_info.append(info)

        return code_info

    def _parse_python_file(self, full_path: str, rel_path: str) -> Dict[str, Any]:
        """Parses a single Python file AST for structure analysis."""
        functions = []
        classes = []
        docstring = ""

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)
            docstring = ast.get_docstring(tree) or ""

            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)

        except Exception as e:
            docstring = f"Parse notice: {str(e)}"

        return {
            "rel_path": rel_path,
            "functions": functions,
            "classes": classes,
            "docstring": docstring,
        }

    def _generate_index_md(self, code_structure: List[Dict[str, Any]]) -> str:
        """Generates index.md Markdown catalog for Karpathy LLM Wiki."""
        lines = [
            "# 📚 KodaWiki Living Knowledge Catalog (`index.md`)\n",
            "> *Persistent knowledge base compiled by KodaWiki Agent based on Andrej Karpathy's LLM Wiki architecture.*\n",
            "## 📁 Repository Code Structure\n",
        ]

        for item in code_structure:
            lines.append(f"### 📄 `{item['rel_path']}`")
            if item["docstring"]:
                lines.append(f"> *{item['docstring'].strip()}*")
            if item["classes"]:
                lines.append(
                    f"- **Classes**: "
                    + ", ".join([f"`{c}`" for c in item["classes"]])
                )
            if item["functions"]:
                lines.append(
                    f"- **Functions**: "
                    + ", ".join([f"`{f}`" for f in item["functions"]])
                )
            lines.append("")

        return "\n".join(lines)
