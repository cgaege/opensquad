"""HelloAgent - Simple test agent for validating Ollama integration."""

from typing import Any, Dict, Optional

from langchain_ollama import OllamaLLM

from .base import AgentConfig, AgentRole, BaseAgent


class HelloAgent(BaseAgent):
    """A minimal agent that validates Ollama integration.

    This agent:
    - Tests basic LLM communication
    - Returns formatted responses
    - Serves as a template for other agents
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize HelloAgent with optional configuration.

        Args:
            config: Agent configuration. If None, uses defaults.
        """
        if config is None:
            config = AgentConfig(
                name="HelloAgent",
                role=AgentRole.BACKEND,  # Placeholder role
                model="llama3",
                temperature=0.7
            )
        super().__init__(config)
        self.llm = OllamaLLM(
            model=self.config.model,
            temperature=self.config.temperature,
            base_url=self.config.base_url
        )

    def get_system_prompt(self) -> str:
        """Return system prompt for HelloAgent.

        Returns:
            System prompt defining the agent's behavior
        """
        return """You are HelloAgent, a friendly AI assistant testing the OpenSquad system.
Your role is to respond concisely and helpfully to greetings and test queries.
Keep your responses brief (1-2 sentences) and friendly."""

    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a task by sending it to Ollama.

        Args:
            task: The task or message to process
            context: Optional context (not used in this simple agent)

        Returns:
            Dictionary with status and result:
            - status: "completed" or "failed"
            - result: Response from LLM
            - error: Error message if failed
        """
        self._initialize_state(task, context)

        try:
            # Validate input
            if not task or not task.strip():
                self._update_state("failed", error="Task cannot be empty")
                return {
                    "status": "failed",
                    "error": "Task cannot be empty"
                }

            # Create full prompt with system context
            full_prompt = f"{self.get_system_prompt()}\n\nUser: {task}\n\nAssistant:"

            # Call Ollama LLM
            response = self.llm.invoke(full_prompt)

            # Update state and return success
            result = {
                "agent": self.config.name,
                "role": self.config.role.value,
                "response": response,
                "model": self.config.model
            }
            self._update_state("completed", result=result)

            return {
                "status": "completed",
                "result": result
            }

        except Exception as e:
            # Handle errors gracefully
            error_msg = f"Error processing task: {str(e)}"
            self._update_state("failed", error=error_msg)
            return {
                "status": "failed",
                "error": error_msg
            }
