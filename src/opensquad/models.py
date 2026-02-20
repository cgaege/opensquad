"""Pydantic models for structured agent outputs."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class SubTask(BaseModel):
    """Represents a single sub-task in a task plan."""

    id: str = Field(..., description="Unique identifier for the subtask")
    title: str = Field(..., description="Brief title of the subtask")
    description: str = Field(..., description="Detailed description of what needs to be done")
    dependencies: List[str] = Field(
        default_factory=list,
        description="List of subtask IDs that must be completed first"
    )
    estimated_complexity: str = Field(
        default="medium",
        description="Complexity estimate: low, medium, high"
    )


class TaskPlan(BaseModel):
    """Structured output for architectural task planning."""

    summary: str = Field(..., description="High-level summary of the task")
    subtasks: List[SubTask] = Field(..., description="List of subtasks to complete")
    architecture_decisions: List[str] = Field(
        default_factory=list,
        description="Key architectural decisions and rationale"
    )
    technologies: List[str] = Field(
        default_factory=list,
        description="Recommended technologies and tools"
    )
    considerations: List[str] = Field(
        default_factory=list,
        description="Important considerations, risks, or constraints"
    )
