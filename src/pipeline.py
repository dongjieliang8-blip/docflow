"""Pipeline orchestrator — wires 4 agents together with structured data passing."""

import json
import time
import os
from dataclasses import dataclass, field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.llm.client import LLMClient, LLMConfig
from src.agents import scanner, planner, writer, reviewer
from src.utils import collect_source_files, format_files_for_prompt

console = Console()


@dataclass
class PipelineResult:
    scanner_report: dict = field(default_factory=dict)
    planner_plan: dict = field(default_factory=dict)
    writer_outputs: list[dict] = field(default_factory=list)
    reviewer_reports: list[dict] = field(default_factory=list)
    token_usage: dict = field(default_factory=dict)
    elapsed_seconds: float = 0.0
    errors: list[str] = field(default_factory=list)
    docs_generated: list[str] = field(default_factory=list)

    @property
    def success(self) -> bool:
        return len(self.errors) == 0

    @property
    def verdict(self) -> str:
        if not self.reviewer_reports:
            return "unknown"
        verdicts = [r.get("overall_verdict", "unknown") for r in self.reviewer_reports]
        if all(v == "APPROVED" for v in verdicts):
            return "APPROVED"
        if any(v == "NEEDS_REVISION" for v in verdicts):
            return "NEEDS_REVISION"
        return "APPROVED_WITH_NOTES"


class Pipeline:
    """DocFlow pipeline: Scanner → Planner → Writer → Reviewer."""

    def __init__(self, config: LLMConfig | None = None):
        self.client = LLMClient(config)
        self.result = PipelineResult()

    def run(self, target_dir: str, output_dir: str = "docs", dry_run: bool = False) -> PipelineResult:
        """Execute the full 4-agent pipeline on a target directory."""
        t0 = time.time()
        os.makedirs(output_dir, exist_ok=True)

        # Stage 1: Scan
        console.print(Panel.fit("[bold blue]STAGE 1/4: Scanner Agent[/] — analyzing codebase", border_style="blue"))
        files = collect_source_files(target_dir)
        if not files:
            self.result.errors.append("No source files found in target directory")
            return self.result
        source_text = format_files_for_prompt(files)
        self.result.scanner_report = scanner.run(source_text, self.client)
        self._print_scanner_summary()

        if dry_run:
            self.result.elapsed_seconds = time.time() - t0
            return self.result

        # Stage 2: Plan
        console.print(Panel.fit("[bold yellow]STAGE 2/4: Planner Agent[/] — designing doc structure", border_style="yellow"))
        self.result.planner_plan = planner.run(self.result.scanner_report, self.client)
        self._print_planner_summary()

        # Stage 3: Write (per batch)
        batches = self.result.planner_plan.get("batches", [])
        for i, batch in enumerate(batches):
            console.print(Panel.fit(
                f"[bold green]STAGE 3/4: Writer Agent[/] — generating docs ({i+1}/{len(batches)})",
                border_style="green"
            ))
            out = writer.run(batch, source_text, self.client)
            self.result.writer_outputs.append(out)
            self._print_writer_summary(out, i + 1)

            # Stage 4: Review (per batch)
            console.print(Panel.fit(
                f"[bold red]STAGE 4/4: Reviewer Agent[/] — validating docs ({i+1}/{len(batches)})",
                border_style="red"
            ))
            rev = reviewer.run(out, self.result.scanner_report, self.client)
            self.result.reviewer_reports.append(rev)
            self._print_reviewer_summary(rev, i + 1)

            # Write approved docs to disk
            if rev.get("overall_verdict") in ("APPROVED", "APPROVED_WITH_NOTES"):
                fpath = os.path.join(output_dir, out.get("file_path", f"doc_{i}.md"))
                os.makedirs(os.path.dirname(fpath) if os.path.dirname(fpath) else output_dir, exist_ok=True)
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(out.get("content", ""))
                self.result.docs_generated.append(fpath)
                console.print(f"  [green]Saved:[/] {fpath}")

        self.result.elapsed_seconds = time.time() - t0
        self._print_final_summary()
        return self.result

    def _print_scanner_summary(self):
        r = self.result.scanner_report
        m = r.get("metrics", {})
        table = Table(title="Scanner Results")
        table.add_column("Metric", style="cyan")
        table.add_column("Count", style="magenta")
        for key in ["total_files", "total_lines", "total_apis", "public_apis"]:
            table.add_row(key.replace("_", " ").title(), str(m.get(key, "?")))
        console.print(table)
        if r.get("summary"):
            console.print(f"[dim]{r['summary']}[/dim]")

    def _print_planner_summary(self):
        p = self.result.planner_plan
        batches = p.get("batches", [])
        console.print(f"[yellow]Strategy:[/] {p.get('strategy', 'N/A')}")
        console.print(f"[yellow]Doc type:[/] {p.get('doc_type', 'N/A')}")
        console.print(f"[yellow]Batches planned:[/] {len(batches)}")
        for b in batches:
            console.print(f"  • [bold]{b.get('priority', '?')}[/] {b.get('title', 'Untitled')} → {b.get('target_file', '?')}")

    def _print_writer_summary(self, out: dict, idx: int):
        if "error" in out:
            console.print(f"[yellow]Writer JSON parse error:[/] {out.get('error')}")
        console.print(f"  [green]File:[/] {out.get('file_path', '?')}")
        console.print(f"  [green]Word count:[/] {out.get('word_count', '?')}")
        console.print(f"  [green]APIs documented:[/] {len(out.get('apis_documented', []))}")

    def _print_reviewer_summary(self, rev: dict, idx: int):
        verdict = rev.get("overall_verdict", "unknown")
        score = rev.get("score", "?")
        console.print(f"  [red]Verdict:[/] [bold]{verdict}[/] (score: {score})")
        issues = rev.get("issues", [])
        if issues:
            console.print(f"  [dim]Issues found: {len(issues)}[/]")
        if rev.get("final_recommendation"):
            console.print(f"  [dim]{rev['final_recommendation'][:200]}[/]")

    def _print_final_summary(self):
        console.print()
        console.print(Panel.fit(
            f"[bold]Pipeline Complete[/]\n"
            f"Time: {self.result.elapsed_seconds:.1f}s\n"
            f"Docs generated: {len(self.result.docs_generated)}\n"
            f"Verdict: {self.result.verdict.upper()}\n"
            f"Errors: {len(self.result.errors)}",
            border_style="green" if self.result.success else "red"
        ))

    def save_report(self, path: str):
        """Save the full pipeline result as JSON."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "scanner_report": self.result.scanner_report,
                "planner_plan": self.result.planner_plan,
                "writer_outputs": [{k: v for k, v in w.items() if k != "content"} for w in self.result.writer_outputs],
                "reviewer_reports": self.result.reviewer_reports,
                "docs_generated": self.result.docs_generated,
                "elapsed_seconds": self.result.elapsed_seconds,
                "errors": self.result.errors,
            }, f, ensure_ascii=False, indent=2)
        console.print(f"[green]Report saved to {path}[/]")
