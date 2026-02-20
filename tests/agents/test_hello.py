"""Tests for HelloAgent."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from opensquad.agents.base import AgentConfig, AgentRole
from opensquad.agents.hello import HelloAgent


def test_hello_agent_initialization():
    """Test HelloAgent initialization with defaults."""
    agent = HelloAgent()
    assert agent.config.name == "HelloAgent"
    assert agent.config.role == AgentRole.BACKEND
    assert agent.config.model == "llama3"
    assert agent.config.temperature == 0.7


def test_hello_agent_initialization_with_config():
    """Test HelloAgent initialization with custom config."""
    config = AgentConfig(
        name="CustomHello",
        role=AgentRole.QA,
        model="mistral",
        temperature=0.5
    )
    agent = HelloAgent(config)
    assert agent.config.name == "CustomHello"
    assert agent.config.role == AgentRole.QA
    assert agent.config.model == "mistral"
    assert agent.config.temperature == 0.5


def test_hello_agent_system_prompt():
    """Test HelloAgent system prompt."""
    agent = HelloAgent()
    prompt = agent.get_system_prompt()
    assert "HelloAgent" in prompt
    assert "OpenSquad" in prompt
    assert "friendly" in prompt.lower()


@pytest.mark.asyncio
async def test_hello_agent_process_empty_task():
    """Test HelloAgent with empty task."""
    agent = HelloAgent()
    result = await agent.process("")
    assert result["status"] == "failed"
    assert "empty" in result["error"].lower()


@pytest.mark.asyncio
async def test_hello_agent_process_whitespace_task():
    """Test HelloAgent with whitespace-only task."""
    agent = HelloAgent()
    result = await agent.process("   ")
    assert result["status"] == "failed"
    assert "empty" in result["error"].lower()


@pytest.mark.asyncio
@patch("opensquad.agents.hello.OllamaLLM")
async def test_hello_agent_process_success(mock_llm_class):
    """Test HelloAgent successful processing."""
    # Mock the LLM response
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "Hello! I'm doing great, thanks for asking!"
    mock_llm_class.return_value = mock_llm

    agent = HelloAgent()
    result = await agent.process("How are you?")

    assert result["status"] == "completed"
    assert "result" in result
    assert result["result"]["agent"] == "HelloAgent"
    assert result["result"]["role"] == "backend"
    assert result["result"]["response"] == "Hello! I'm doing great, thanks for asking!"
    assert result["result"]["model"] == "llama3"


@pytest.mark.asyncio
@patch("opensquad.agents.hello.OllamaLLM")
async def test_hello_agent_process_with_context(mock_llm_class):
    """Test HelloAgent processing with context."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "Response"
    mock_llm_class.return_value = mock_llm

    agent = HelloAgent()
    context = {"previous": "data"}
    result = await agent.process("Test", context)

    assert result["status"] == "completed"
    assert agent.state.context == context


@pytest.mark.asyncio
@patch("opensquad.agents.hello.OllamaLLM")
async def test_hello_agent_process_llm_error(mock_llm_class):
    """Test HelloAgent handling LLM errors."""
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("Connection error")
    mock_llm_class.return_value = mock_llm

    agent = HelloAgent()
    result = await agent.process("Test message")

    assert result["status"] == "failed"
    assert "error" in result
    assert "Connection error" in result["error"]


@pytest.mark.asyncio
@patch("opensquad.agents.hello.OllamaLLM")
async def test_hello_agent_state_management(mock_llm_class):
    """Test HelloAgent state management during processing."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "Response"
    mock_llm_class.return_value = mock_llm

    agent = HelloAgent()
    await agent.process("Test")

    assert agent.state is not None
    assert agent.state.task == "Test"
    assert agent.state.status == "completed"
    assert agent.state.result is not None
    assert agent.state.error is None


@pytest.mark.asyncio
@patch("opensquad.agents.hello.OllamaLLM")
async def test_hello_agent_state_on_error(mock_llm_class):
    """Test HelloAgent state management on error."""
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("Test error")
    mock_llm_class.return_value = mock_llm

    agent = HelloAgent()
    await agent.process("Test")

    assert agent.state is not None
    assert agent.state.status == "failed"
    assert agent.state.error is not None
    assert "Test error" in agent.state.error


@pytest.mark.asyncio
@patch("opensquad.agents.hello.OllamaLLM")
async def test_hello_agent_prompt_construction(mock_llm_class):
    """Test that HelloAgent constructs prompts correctly."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "Response"
    mock_llm_class.return_value = mock_llm

    agent = HelloAgent()
    await agent.process("Test message")

    # Verify invoke was called with proper prompt structure
    mock_llm.invoke.assert_called_once()
    call_args = mock_llm.invoke.call_args[0][0]
    assert "HelloAgent" in call_args
    assert "Test message" in call_args
    assert "User:" in call_args
    assert "Assistant:" in call_args


@pytest.mark.asyncio
@patch("opensquad.agents.hello.OllamaLLM")
async def test_hello_agent_multiple_calls(mock_llm_class):
    """Test HelloAgent can handle multiple calls."""
    mock_llm = MagicMock()
    mock_llm.invoke.return_value = "Response"
    mock_llm_class.return_value = mock_llm

    agent = HelloAgent()
    
    result1 = await agent.process("First message")
    assert result1["status"] == "completed"
    
    result2 = await agent.process("Second message")
    assert result2["status"] == "completed"
    
    assert mock_llm.invoke.call_count == 2
