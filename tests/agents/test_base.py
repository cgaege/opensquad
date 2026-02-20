"""Tests for BaseAgent class."""

import pytest

from opensquad.agents.base import AgentConfig, AgentRole, AgentState, BaseAgent


class ConcreteAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing."""

    def get_system_prompt(self) -> str:
        return "Test system prompt"

    async def process(self, task: str, context: dict | None = None) -> dict:
        self._initialize_state(task, context)
        self._update_state("completed", result={"test": "result"})
        return {"status": "completed", "result": {"test": "result"}}


def test_agent_config_creation():
    """Test AgentConfig model creation."""
    config = AgentConfig(
        name="TestAgent",
        role=AgentRole.BACKEND,
        model="llama3",
        temperature=0.7
    )
    assert config.name == "TestAgent"
    assert config.role == AgentRole.BACKEND
    assert config.model == "llama3"
    assert config.temperature == 0.7
    assert config.base_url == "http://localhost:11434"


def test_agent_config_defaults():
    """Test AgentConfig default values."""
    config = AgentConfig(name="TestAgent", role=AgentRole.ARCHITECT)
    assert config.model == "llama3"
    assert config.temperature == 0.7
    assert config.base_url == "http://localhost:11434"


def test_agent_state_creation():
    """Test AgentState model creation."""
    state = AgentState(task="Test task", context={"key": "value"})
    assert state.task == "Test task"
    assert state.context == {"key": "value"}
    assert state.status == "not_started"
    assert state.result is None
    assert state.error is None


def test_agent_state_defaults():
    """Test AgentState default values."""
    state = AgentState(task="Test task")
    assert state.context == {}
    assert state.status == "not_started"


def test_agent_role_enum():
    """Test AgentRole enum values."""
    assert AgentRole.ARCHITECT.value == "architect"
    assert AgentRole.BACKEND.value == "backend"
    assert AgentRole.FRONTEND.value == "frontend"
    assert AgentRole.QA.value == "qa"
    assert AgentRole.REVIEWER.value == "reviewer"


def test_concrete_agent_initialization():
    """Test concrete agent initialization."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    agent = ConcreteAgent(config)
    assert agent.config == config
    assert agent.state is None


def test_concrete_agent_system_prompt():
    """Test concrete agent system prompt."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    agent = ConcreteAgent(config)
    assert agent.get_system_prompt() == "Test system prompt"


@pytest.mark.asyncio
async def test_concrete_agent_process():
    """Test concrete agent process method."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    agent = ConcreteAgent(config)
    result = await agent.process("Test task")
    assert result["status"] == "completed"
    assert result["result"] == {"test": "result"}


@pytest.mark.asyncio
async def test_concrete_agent_process_with_context():
    """Test concrete agent process with context."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    agent = ConcreteAgent(config)
    context = {"previous": "data"}
    result = await agent.process("Test task", context)
    assert result["status"] == "completed"
    assert agent.state.context == context


def test_agent_initialize_state():
    """Test _initialize_state method."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    agent = ConcreteAgent(config)
    agent._initialize_state("Test task", {"key": "value"})
    assert agent.state is not None
    assert agent.state.task == "Test task"
    assert agent.state.context == {"key": "value"}
    assert agent.state.status == "in_progress"


def test_agent_initialize_state_no_context():
    """Test _initialize_state with no context."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    agent = ConcreteAgent(config)
    agent._initialize_state("Test task", None)
    assert agent.state.context == {}


def test_agent_update_state():
    """Test _update_state method."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    agent = ConcreteAgent(config)
    agent._initialize_state("Test task", {})
    agent._update_state("completed", result={"test": "result"})
    assert agent.state.status == "completed"
    assert agent.state.result == {"test": "result"}
    assert agent.state.error is None


def test_agent_update_state_with_error():
    """Test _update_state with error."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    agent = ConcreteAgent(config)
    agent._initialize_state("Test task", {})
    agent._update_state("failed", error="Test error")
    assert agent.state.status == "failed"
    assert agent.state.error == "Test error"
    assert agent.state.result is None


def test_agent_cannot_instantiate_base_class():
    """Test that BaseAgent cannot be instantiated directly."""
    config = AgentConfig(name="TestAgent", role=AgentRole.BACKEND)
    with pytest.raises(TypeError):
        BaseAgent(config)
