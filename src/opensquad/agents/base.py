"""Base agent class for OpenSquad agents."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel


class AgentRole(str, Enum):
    """Enum defining agent roles in the system."""

    ARCHITECT = "architect"
    BACKEND = "backend"
    FRONTEND = "frontend"
    QA = "qa"
    REVIEWER = "reviewer"


class AgentConfig(BaseModel):
    """Configuration for an agent."""

    name: str
    role: AgentRole
    model: str = "llama3"
    temperature: float = 0.7
    base_url: str = "http://localhost:11434"


class AgentState(BaseModel):
    """State maintained by an agent during processing."""

    task: str
    context: Dict[str, Any] = {}
    status: str = "not_started"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class BaseAgent(ABC):
    """Abstract base class for all OpenSquad agents.

    Each agent should:
    - Define its role and behavior via get_system_prompt()
    - Implement the process() method for task execution
    - Handle errors gracefully
    - Return structured results
    """

    def __init__(self, config: AgentConfig):
        """Initialize the agent with configuration.

        Args:
            config: Agent configuration including model settings
        """
        self.config = config
        self.state: Optional[AgentState] = None

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt defining the agent's role and behavior.

        Returns:
            System prompt string for the LLM
        """
        pass

    @abstractmethod
    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a task with optional context.

        Args:
            task: The task to process
            context: Optional context from previous steps or shared state

        Returns:
            Dictionary with processing results including:
            - status: "completed", "failed", or other status
            - result: Task-specific results
            - error: Error message if status is "failed"

        Raises:
            Exception: If critical error occurs during processing
        """
        pass

    def _initialize_state(self, task: str, context: Optional[Dict[str, Any]]) -> None:
        """Initialize agent state for a new task.

        Args:
            task: The task to process
            context: Optional context dictionary
        """
        self.state = AgentState(
            task=task,
            context=context or {},
            status="in_progress"
        )

    def _update_state(
        self,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> None:
        """Update the agent's state.

        Args:
            status: New status value
            result: Optional result dictionary
            error: Optional error message
        """
        if self.state:
            self.state.status = status
            self.state.result = result
            self.state.error = error
