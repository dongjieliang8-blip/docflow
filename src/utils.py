"""Shared utilities for code analysis."""

import os
from pathlib import Path

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
    ".c", ".cpp", ".h", ".hpp", ".rb", ".php", ".swift", ".kt",
    ".cs", ".scala", ".sh", ".bash", ".sql",
}

IGNORE_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    "dist", "build", ".next", ".nuxt", "vendor", "target",
}


def collect_source_files(root: str, max_size_kb: int = 200) -> list[dict]:
    """Walk a directory and collect source files with metadata."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for fname in filenames:
            ext = Path(fname).suffix.lower()
            if ext not in CODE_EXTENSIONS:
                continue
            full_path = os.path.join(dirpath, fname)
            try:
                size = os.path.getsize(full_path)
                if size > max_size_kb * 1024:
                    continue
                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                rel_path = os.path.relpath(full_path, root)
                files.append({
                    "path": rel_path,
                    "lines": content.count("\n") + 1,
                    "size_bytes": size,
                    "content": content,
                })
            except (OSError, UnicodeDecodeError):
                continue
    return files


def format_files_for_prompt(files: list[dict], max_chars: int = 60000) -> str:
    """Format collected files into a prompt-friendly string."""
    parts = []
    total = 0
    for f in files:
        block = f"\n### {f['path']} ({f['lines']} lines)\n```\n{f['content']}\n```\n"
        if total + len(block) > max_chars:
            block = f"\n### {f['path']} ({f['lines']} lines) [TRUNCATED]\n```\n{f['content'][:2000]}\n...\n```\n"
        parts.append(block)
        total += len(block)
        if total > max_chars:
            break
    return "\n".join(parts)
