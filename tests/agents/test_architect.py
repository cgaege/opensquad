"""Tests for ArchitectAgent."""

from unittest.mock import MagicMock, patch

import pytest

from opensquad.agents.architect import ArchitectAgent
from opensquad.agents.base import AgentConfig, AgentRole


def test_architect_agent_initialization():
    """Test ArchitectAgent initialization with defaults."""
    agent = ArchitectAgent()
    assert agent.config.name == "ArchitectAgent"
    assert agent.config.role == AgentRole.ARCHITECT
    assert agent.config.model == "gemma3:12b"
    assert agent.config.temperature == 0.3


def test_architect_agent_initialization_with_config():
    """Test ArchitectAgent initialization with custom config."""
    config = AgentConfig(
        name="CustomArchitect",
        role=AgentRole.ARCHITECT,
        model="llama3.1",
        temperature=0.5
    )
    agent = ArchitectAgent(config)
    assert agent.config.name == "CustomArchitect"
    assert agent.config.model == "llama3.1"
    assert agent.config.temperature == 0.5


def test_architect_agent_system_prompt():
    """Test ArchitectAgent system prompt."""
    agent = ArchitectAgent()
    prompt = agent.get_system_prompt()
    assert "Software Architect" in prompt
    assert "task plans" in prompt
    assert "JSON" in prompt
    assert "subtasks" in prompt


@pytest.mark.asyncio
async def test_architect_agent_process_empty_task():
    """Test ArchitectAgent with empty task."""
    agent = ArchitectAgent()
    result = await agent.process("")
    assert result["status"] == "failed"
    assert "empty" in result["error"].lower()


@pytest.mark.asyncio
async def test_architect_agent_process_whitespace_task():
    """Test ArchitectAgent with whitespace-only task."""
    agent = ArchitectAgent()
    result = await agent.process("   ")
    assert result["status"] == "failed"
    assert "empty" in result["error"].lower()


@pytest.mark.asyncio
@patch("opensquad.agents.architect.OllamaLLM")
async def test_architect_agent_process_success(mock_llm_class):
    """Test ArchitectAgent successful processing."""
    # Mock the LLM response
    mock_llm = MagicMock()
    mock_response = """{
        "summary": "Build REST API for user authentication",
        "subtasks": [
            {
                "id": "task-1",
                "title": "Setup project",
                "description": "Initialize FastAPI project",
                "dependencies": [],
                "estimated_complexity": "low"
            },
            {
                "id": "task-2",
                "title": "Implement auth",
                "description": "Create JWT authentication",
                "dependencies": ["task-1"],
                "estimated_complexity": "high"
            }
        ],
        "architecture_decisions": ["Use JWT for stateless auth", "REST API design"],
        "technologies": ["FastAPI", "PostgreSQL", "JWT"],
        "considerations": ["Security best practices", "Token expiration"]
    }"""
    mock_llm.invoke.return_value = mock_response
    mock_llm_class.return_value = mock_llm

    agent = ArchitectAgent()
    result = await agent.process("Build a REST API for user authentication")

    assert result["status"] == "completed"
    assert "result" in result
    assert result["result"]["agent"] == "ArchitectAgent"
    assert result["result"]["role"] == "architect"
    
    task_plan = result["result"]["task_plan"]
    assert task_plan["summary"] == "Build REST API for user authentication"
    assert len(task_plan["subtasks"]) == 2
    assert task_plan["subtasks"][0]["id"] == "task-1"
    assert len(task_plan["technologies"]) == 3


@pytest.mark.asyncio
@patch("opensquad.agents.architect.OllamaLLM")
async def test_architect_agent_process_with_markdown_json(mock_llm_class):
    """Test ArchitectAgent parsing JSON wrapped in markdown."""
    mock_llm = MagicMock()
    mock_response = """```json
    {
        "summary": "Test task",
        "subtasks": [],
        "architecture_decisions": [],
        "technologies": [],
        "considerations": []
    }
    ```"""
    mock_llm.invoke.return_value = mock_response
    mock_llm_class.return_value = mock_llm

    agent = ArchitectAgent()
    result = await agent.process("Test task")

    assert result["status"] == "completed"
    assert result["result"]["task_plan"]["summary"] == "Test task"


@pytest.mark.asyncio
@patch("opensquad.agents.architect.OllamaLLM")
async def test_architect_agent_process_invalid_json(mock_llm_class):
    """Test ArchitectAgent handling invalid JSON."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "This is not valid JSON"
    mock_llm_class.return_value = mock_llm

    agent = ArchitectAgent()
    result = await agent.process("Test task")

    assert result["status"] == "failed"
    assert "error" in result
    assert "JSON" in result["error"]


@pytest.mark.asyncio
@patch("opensquad.agents.architect.OllamaLLM")
async def test_architect_agent_process_llm_error(mock_llm_class):
    """Test ArchitectAgent handling LLM errors."""
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("Connection error")
    mock_llm_class.return_value = mock_llm

    agent = ArchitectAgent()
    result = await agent.process("Test task")

    assert result["status"] == "failed"
    assert "error" in result
    assert "Connection error" in result["error"]


@pytest.mark.asyncio
@patch("opensquad.agents.architect.OllamaLLM")
async def test_architect_agent_state_management(mock_llm_class):
    """Test ArchitectAgent state management during processing."""
    mock_llm = MagicMock()
    mock_response = '{"summary": "Test", "subtasks": []}'
    mock_llm.invoke.return_value = mock_response
    mock_llm_class.return_value = mock_llm

    agent = ArchitectAgent()
    await agent.process("Test task")

    assert agent.state is not None
    assert agent.state.task == "Test task"
    assert agent.state.status == "completed"
    assert agent.state.result is not None


def test_architect_agent_parse_response_clean_json():
    """Test parsing clean JSON response."""
    agent = ArchitectAgent()
    response = '{"summary": "Test", "subtasks": []}'
    result = agent._parse_response(response)
    assert result["summary"] == "Test"
    assert result["subtasks"] == []


def test_architect_agent_parse_response_markdown():
    """Test parsing JSON wrapped in markdown."""
    agent = ArchitectAgent()
    response = '```json\n{"summary": "Test", "subtasks": []}\n```'
    result = agent._parse_response(response)
    assert result["summary"] == "Test"


def test_architect_agent_parse_response_invalid():
    """Test parsing invalid JSON raises ValueError."""
    agent = ArchitectAgent()
    with pytest.raises(ValueError, match="Failed to parse response"):
        agent._parse_response("not valid json")


@pytest.mark.asyncio
@patch("opensquad.agents.architect.OllamaLLM")
async def test_architect_agent_with_context(mock_llm_class):
    """Test ArchitectAgent processing with context."""
    mock_llm = MagicMock()
    mock_response = '{"summary": "Test", "subtasks": []}'
    mock_llm.invoke.return_value = mock_response
    mock_llm_class.return_value = mock_llm

    agent = ArchitectAgent()
    context = {"previous_analysis": "data"}
    result = await agent.process("Test task", context)

    assert result["status"] == "completed"
    assert agent.state.context == context
