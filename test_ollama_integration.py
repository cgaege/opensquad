#!/usr/bin/env python3
"""Manual test script for HelloAgent with real Ollama integration.

This script tests the HelloAgent with actual Ollama to verify the integration works.

Prerequisites:
- Ollama must be running: ollama serve
- llama3 model must be available: ollama pull llama3

Usage:
    python test_ollama_integration.py
"""

import asyncio

from rich.console import Console
from rich.panel import Panel

from opensquad.agents.hello import HelloAgent

console = Console()


async def test_hello_agent():
    """Test HelloAgent with real Ollama."""
    console.print(Panel.fit(
        "[bold cyan]Testing HelloAgent with Ollama[/bold cyan]",
        border_style="cyan"
    ))
    
    # Test 1: Simple greeting
    console.print("\n[yellow]Test 1: Simple greeting[/yellow]")
    from opensquad.agents.base import AgentConfig, AgentRole
    config = AgentConfig(name="HelloAgent", role=AgentRole.BACKEND, model="gemma3:12b")
    agent = HelloAgent(config)
    result = await agent.process("Hello! How are you?")
    
    if result["status"] == "completed":
        console.print(f"[green]✓ Success[/green]")
        console.print(f"Response: {result['result']['response']}\n")
    else:
        console.print(f"[red]✗ Failed: {result['error']}[/red]\n")
        return False
    
    # Test 2: Empty message error handling
    console.print("[yellow]Test 2: Error handling (empty message)[/yellow]")
    result = await agent.process("")
    
    if result["status"] == "failed" and "empty" in result["error"].lower():
        console.print("[green]✓ Error handling works[/green]\n")
    else:
        console.print("[red]✗ Error handling failed[/red]\n")
        return False
    
    # Test 3: Technical question
    console.print("[yellow]Test 3: Technical question[/yellow]")
    result = await agent.process("What is Python?")
    
    if result["status"] == "completed":
        console.print(f"[green]✓ Success[/green]")
        console.print(f"Response: {result['result']['response']}\n")
    else:
        console.print(f"[red]✗ Failed: {result['error']}[/red]\n")
        return False
    
    console.print(Panel.fit(
        "[bold green]All tests passed! ✓[/bold green]",
        border_style="green"
    ))
    return True


if __name__ == "__main__":
    try:
        success = asyncio.run(test_hello_agent())
        exit(0 if success else 1)
    except Exception as e:
        console.print(f"\n[bold red]Error: {e}[/bold red]")
        console.print("\n[yellow]Make sure:[/yellow]")
        console.print("1. Ollama is running: ollama serve")
        console.print("2. llama3 is installed: ollama pull llama3")
        exit(1)
