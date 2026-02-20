"""CLI interface for OpenSquad."""

import asyncio

import typer
from rich.console import Console
from rich.panel import Panel

from opensquad.agents.hello import HelloAgent

app = typer.Typer(
    name="opensquad",
    help="OpenSquad - Multi-Agent AI Coding System",
    add_completion=False
)
console = Console()


@app.command()
def hello(
    message: str = typer.Argument(..., help="Message to send to HelloAgent"),
    model: str = typer.Option("llama3", help="Ollama model to use")
) -> None:
    """Test the HelloAgent with a message.

    Example:
        opensquad hello "How are you?"
    """
    console.print(Panel.fit(
        f"[bold cyan]OpenSquad HelloAgent[/bold cyan]\n"
        f"Model: {model}",
        border_style="cyan"
    ))

    console.print(f"\n[yellow]User:[/yellow] {message}\n")

    # Create and run agent
    agent = HelloAgent()
    result = asyncio.run(agent.process(message))

    # Display result
    if result["status"] == "completed":
        response = result["result"]["response"]
        console.print(f"[green]Agent:[/green] {response}\n")
        console.print(f"[dim]Model: {result['result']['model']}[/dim]")
    else:
        console.print(f"[red]Error:[/red] {result['error']}\n", style="bold red")


@app.command()
def version() -> None:
    """Show OpenSquad version."""
    from opensquad import __version__
    console.print(f"OpenSquad version: [bold cyan]{__version__}[/bold cyan]")


def main() -> None:
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
