"""ArchitectAgent - Task decomposition and architectural planning."""

import json
from typing import Any, Dict, Optional

from langchain_ollama import OllamaLLM

from opensquad.agents.base import AgentConfig, AgentRole, BaseAgent
from opensquad.models import SubTask, TaskPlan


class ArchitectAgent(BaseAgent):
    """Agent specialized in analyzing requirements and creating task plans.

    The ArchitectAgent:
    - Analyzes user requirements
    - Breaks down complex tasks into subtasks
    - Makes architectural decisions
    - Recommends technologies
    - Identifies dependencies between tasks
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize ArchitectAgent with optional configuration.

        Args:
            config: Agent configuration. If None, uses defaults.
        """
        if config is None:
            config = AgentConfig(
                name="ArchitectAgent",
                role=AgentRole.ARCHITECT,
                model="gemma3:12b",
                temperature=0.3  # Lower temperature for more consistent planning
            )
        super().__init__(config)
        self.llm = OllamaLLM(
            model=self.config.model,
            temperature=self.config.temperature,
            base_url=self.config.base_url
        )

    def get_system_prompt(self) -> str:
        """Return system prompt for architectural planning.

        Returns:
            System prompt defining the agent's architectural role
        """
        return """You are an expert Software Architect and Technical Lead.

Your role is to analyze requirements and create clear, actionable task plans.

When given a requirement, you must:
1. Understand the core problem and goals
2. Break it down into logical, sequential subtasks
3. Make key architectural decisions
4. Recommend appropriate technologies
5. Identify dependencies between tasks
6. Consider risks and constraints

Output your response as a JSON object with this structure:
{
  "summary": "Brief overview of what needs to be built",
  "subtasks": [
    {
      "id": "task-1",
      "title": "Short title",
      "description": "Detailed description of the task",
      "dependencies": [],
      "estimated_complexity": "low|medium|high"
    }
  ],
  "architecture_decisions": ["Decision 1", "Decision 2"],
  "technologies": ["Tech 1", "Tech 2"],
  "considerations": ["Risk 1", "Constraint 1"]
}

Be specific, practical, and focus on implementation-ready tasks."""

    async def process(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze task and create structured task plan.

        Args:
            task: The requirement or task to analyze
            context: Optional context from previous steps

        Returns:
            Dictionary with status and TaskPlan result:
            - status: "completed" or "failed"
            - result: TaskPlan object (if successful)
            - error: Error message (if failed)
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

            # Create prompt with system context
            full_prompt = f"{self.get_system_prompt()}\n\nRequirement: {task}\n\nTask Plan:"

            # Call Ollama LLM
            response = self.llm.invoke(full_prompt)

            # Parse JSON response
            task_plan_data = self._parse_response(response)

            # Validate with Pydantic
            task_plan = TaskPlan(**task_plan_data)

            # Update state and return success
            result = {
                "agent": self.config.name,
                "role": self.config.role.value,
                "task_plan": task_plan.model_dump(),
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

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured data.

        Args:
            response: Raw response from LLM

        Returns:
            Parsed dictionary

        Raises:
            ValueError: If response cannot be parsed as JSON
        """
        # Try to extract JSON from response
        # LLMs sometimes wrap JSON in markdown code blocks
        response = response.strip()

        # Remove markdown code blocks if present
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse response as JSON: {e}") from e
