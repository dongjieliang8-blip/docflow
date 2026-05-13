"""DocFlow CLI — multi-agent documentation generation pipeline."""

import sys
import click
from rich.console import Console
from rich.panel import Panel

from src.pipeline import Pipeline
from src.llm.client import LLMConfig

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="docflow")
def cli():
    """DocFlow — AI-powered multi-agent documentation generation pipeline.

    Four specialized agents collaborate in sequence:
    Scanner → Planner → Writer → Reviewer
    """


@cli.command()
@click.argument("target", type=click.Path(exists=True))
@click.option("--output-dir", "-o", default="docs", help="Output directory for generated docs")
@click.option("--dry-run", is_flag=True, help="Run scanner only, skip generation")
@click.option("--report", default="docflow_report.json", help="Save report to JSON file")
@click.option("--model", envvar="DEEPSEEK_MODEL", default="deepseek-chat", help="Model name override")
@click.option("--temperature", default=0.3, help="LLM temperature (0.0-1.0)")
def run(target, output_dir, dry_run, report, model, temperature):
    """Run the full pipeline on TARGET directory."""
    config = LLMConfig.from_env()
    config.model = model
    config.temperature = temperature

    console.print(Panel.fit(
        "[bold]DocFlow Pipeline[/]\n"
        f"Target: {target}\n"
        f"Output: {output_dir}\n"
        f"Model: {config.model}\n"
        f"Mode: {'Dry Run (Scanner only)' if dry_run else 'Full Pipeline'}",
        border_style="blue"
    ))

    try:
        pipeline = Pipeline(config)
        result = pipeline.run(target, output_dir=output_dir, dry_run=dry_run)

        if report and result.success:
            pipeline.save_report(report)
        elif result.errors:
            console.print("[red]Pipeline errors:[/]")
            for err in result.errors:
                console.print(f"  • {err}")
            sys.exit(1)
    except ValueError as e:
        console.print(f"[red]Configuration Error:[/] {e}")
        console.print("[dim]Make sure DEEPSEEK_API_KEY is set in your .env file[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected Error:[/] {e}")
        sys.exit(1)


@cli.command()
@click.argument("target", type=click.Path(exists=True))
def scan(target):
    """Run only the Scanner agent on TARGET directory."""
    config = LLMConfig.from_env()
    try:
        pipeline = Pipeline(config)
        result = pipeline.run(target, dry_run=True)
        if result.success:
            pipeline.save_report("docflow_scan.json")
    except ValueError as e:
        console.print(f"[red]Error:[/] {e}")
        sys.exit(1)


@cli.command()
def config():
    """Show current configuration."""
    cfg = LLMConfig.from_env()
    console.print(f"API Base: {cfg.base_url}")
    console.print(f"Model: {cfg.model}")
    console.print(f"API Key: {'***' + cfg.api_key[-4:] if cfg.api_key else 'NOT SET'}")
    console.print(f"Temperature: {cfg.temperature}")


if __name__ == "__main__":
    cli()
