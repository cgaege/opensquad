"""CLI interface for OpenSquad."""

import asyncio

import typer
from rich.console import Console
from rich.panel import Panel

from opensquad.agents.hello import HelloAgent
from opensquad.agents.architect import ArchitectAgent

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
    from opensquad.agents.base import AgentConfig, AgentRole
    config = AgentConfig(
        name="HelloAgent",
        role=AgentRole.BACKEND,
        model=model
    )
    agent = HelloAgent(config)
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


@app.command()
def architect(
    task: str = typer.Argument(..., help="Task or requirement to analyze"),
    model: str = typer.Option("gemma3:12b", help="Ollama model to use")
) -> None:
    """Analyze task and create architectural plan.

    Example:
        opensquad architect "Build REST API for user authentication"
    """
    console.print(Panel.fit(
        f"[bold cyan]OpenSquad ArchitectAgent[/bold cyan]\n"
        f"Model: {model}",
        border_style="cyan"
    ))

    console.print(f"\n[yellow]Requirement:[/yellow] {task}\n")
    console.print("[dim]Analyzing and creating task plan...[/dim]\n")

    # Create and run agent
    from opensquad.agents.base import AgentConfig, AgentRole
    config = AgentConfig(
        name="ArchitectAgent",
        role=AgentRole.ARCHITECT,
        model=model,
        temperature=0.3
    )
    agent = ArchitectAgent(config)
    result = asyncio.run(agent.process(task))

    # Display result
    if result["status"] == "completed":
        task_plan = result["result"]["task_plan"]
        
        # Summary
        console.print(Panel(
            f"[bold]{task_plan['summary']}[/bold]",
            title="📋 Summary",
            border_style="green"
        ))
        
        # Subtasks
        console.print(f"\n[bold green]📝 Subtasks ({len(task_plan['subtasks'])}):[/bold green]")
        for subtask in task_plan["subtasks"]:
            deps = f" (depends on: {', '.join(subtask['dependencies'])})" if subtask['dependencies'] else ""
            console.print(f"\n  [cyan]{subtask['id']}[/cyan]: [bold]{subtask['title']}[/bold]{deps}")
            console.print(f"  {subtask['description']}")
            console.print(f"  [dim]Complexity: {subtask['estimated_complexity']}[/dim]")
        
        # Architecture Decisions
        if task_plan['architecture_decisions']:
            console.print(f"\n[bold blue]🏗️  Architecture Decisions:[/bold blue]")
            for decision in task_plan['architecture_decisions']:
                console.print(f"  • {decision}")
        
        # Technologies
        if task_plan['technologies']:
            console.print(f"\n[bold magenta]🔧 Technologies:[/bold magenta]")
            console.print(f"  {', '.join(task_plan['technologies'])}")
        
        # Considerations
        if task_plan['considerations']:
            console.print(f"\n[bold yellow]⚠️  Considerations:[/bold yellow]")
            for consideration in task_plan['considerations']:
                console.print(f"  • {consideration}")
        
        console.print(f"\n[dim]Model: {result['result']['model']}[/dim]")
    else:
        console.print(f"[red]Error:[/red] {result['error']}\n", style="bold red")


def main() -> None:
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()
