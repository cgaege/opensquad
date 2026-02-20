"""Tests for Pydantic models."""

import pytest

from opensquad.models import SubTask, TaskPlan


def test_subtask_creation():
    """Test SubTask model creation."""
    subtask = SubTask(
        id="task-1",
        title="Implement API",
        description="Create REST API endpoints",
        dependencies=["task-0"],
        estimated_complexity="medium"
    )
    assert subtask.id == "task-1"
    assert subtask.title == "Implement API"
    assert subtask.description == "Create REST API endpoints"
    assert subtask.dependencies == ["task-0"]
    assert subtask.estimated_complexity == "medium"


def test_subtask_defaults():
    """Test SubTask default values."""
    subtask = SubTask(
        id="task-1",
        title="Test",
        description="Test task"
    )
    assert subtask.dependencies == []
    assert subtask.estimated_complexity == "medium"


def test_task_plan_creation():
    """Test TaskPlan model creation."""
    subtasks = [
        SubTask(id="task-1", title="Setup", description="Initialize project"),
        SubTask(id="task-2", title="Implement", description="Build feature")
    ]
    plan = TaskPlan(
        summary="Build authentication system",
        subtasks=subtasks,
        architecture_decisions=["Use JWT tokens"],
        technologies=["FastAPI", "PostgreSQL"],
        considerations=["Security is critical"]
    )
    assert plan.summary == "Build authentication system"
    assert len(plan.subtasks) == 2
    assert plan.architecture_decisions == ["Use JWT tokens"]
    assert plan.technologies == ["FastAPI", "PostgreSQL"]
    assert plan.considerations == ["Security is critical"]


def test_task_plan_defaults():
    """Test TaskPlan default values."""
    plan = TaskPlan(
        summary="Test plan",
        subtasks=[]
    )
    assert plan.architecture_decisions == []
    assert plan.technologies == []
    assert plan.considerations == []


def test_task_plan_serialization():
    """Test TaskPlan serialization."""
    subtask = SubTask(id="task-1", title="Test", description="Test task")
    plan = TaskPlan(summary="Test", subtasks=[subtask])
    
    data = plan.model_dump()
    assert isinstance(data, dict)
    assert data["summary"] == "Test"
    assert len(data["subtasks"]) == 1
    assert data["subtasks"][0]["id"] == "task-1"


def test_task_plan_from_dict():
    """Test TaskPlan creation from dictionary."""
    data = {
        "summary": "Test plan",
        "subtasks": [
            {
                "id": "task-1",
                "title": "Test",
                "description": "Test description",
                "dependencies": [],
                "estimated_complexity": "low"
            }
        ],
        "architecture_decisions": ["Decision 1"],
        "technologies": ["Tech 1"],
        "considerations": ["Note 1"]
    }
    plan = TaskPlan(**data)
    assert plan.summary == "Test plan"
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].id == "task-1"
