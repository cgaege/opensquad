# 🤖 OpenSquad Agents – System Documentation

This file documents the multi-agent system of OpenSquad and serves as a guide for developing and using the AI agents.

## 📋 Overview

OpenSquad is a **multi-agent AI system** that simulates a virtual software development team. Various specialized agents work together to solve complex software engineering tasks.

### System Architecture

```
┌─────────────────────────────────────────────────┐
│           User / Task Input                      │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│        Multi-Agent Orchestrator                  │
│              (LangGraph)                         │
└────┬────────┬────────┬────────┬─────────────────┘
     │        │        │        │
     ▼        ▼        ▼        ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Architect│ │Backend  │ │Frontend │ │   QA    │
│  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
     │        │        │        │
     └────────┴────────┴────────┘
              │
              ▼
     ┌─────────────────┐
     │  Shared State   │
     │   & Memory      │
     └─────────────────┘
```

## 🎭 Agent Roles

### 1. Architect Agent 🏗️

**Responsibilities:**
- Analysis of user requirements
- System design and architecture decisions
- Task decomposition (breaking down into sub-tasks)
- Technology stack recommendations
- Definition of interfaces between components

**Typical Tasks:**
- "Design a REST API for user management"
- "Create architecture for a microservices system"
- "Decompose this feature into implementable tasks"

**Example:**
```python
architect = ArchitectAgent()
result = await architect.create_task_plan(
    "Build a task management system with user auth"
)
```

### 2. Backend Agent 💻

**Responsibilities:**
- API design and implementation (REST/GraphQL)
- Database schema design
- Business logic implementation
- Authentication & Authorization
- Backend testing

**Typical Tasks:**
- "Implement the user authentication API"
- "Create database schema for tasks"
- "Add validation and error handling"

**Example:**
```python
backend = BackendAgent()
result = await backend.implement_feature(
    feature="User registration endpoint",
    architecture=architect_output
)
```

### 3. Frontend Agent 🎨

**Responsibilities:**
- UI/UX implementation
- Component architecture
- State management
- API integration
- Frontend testing

**Status:** 🚧 Planned for Phase 2

### 4. QA Agent 🧪

**Responsibilities:**
- Test case generation
- Write automated tests
- Code validation
- Bug detection
- Test coverage analysis

**Status:** 🚧 Planned for Phase 2

### 5. Reviewer Agent 👁️

**Responsibilities:**
- Code review
- Check best practices
- Security review
- Suggest performance optimizations
- Review documentation

**Status:** 🚧 Planned for Phase 3

## 🔄 Agent Collaboration Workflow

### Typical Flow

1. **User Input**: Task or requirement is provided
2. **Orchestrator**: Analyzes task and routes to appropriate agent
3. **Architect Agent**: Creates high-level plan and architecture
4. **Backend/Frontend Agents**: Implement based on architecture
5. **QA Agent**: Validates implementation and creates tests
6. **Reviewer Agent**: Final review and feedback
7. **Orchestrator**: Collects results and delivers output

### Agent-to-Agent Communication

Agents communicate via **Shared State** (LangGraph StateGraph):

```python
class TeamState:
    messages: List[Message]           # Conversation History
    current_task: str                 # Current Task
    artifacts: Dict[str, Any]         # Shared Outputs
    next_agent: str                   # Routing Information
```

## 🛠️ For AI-Tools: Development Instructions

### If you are a new agent or working with this system:

#### 1. Understand the System
- Read this AGENTS.md completely
- Understand the multi-agent architecture
- Respect role separation

#### 2. Follow Development Workflow
- **Issue-First**: Always create a GitHub Issue first
- **Feature Branches**: Never commit directly to `main`
- Branch format: `feature/issue-number-description`
- **Acceptance Criteria**: Issues may only be closed when ALL acceptance criteria are met
- **PR Merge**: Pull requests may only be merged when all acceptance criteria of the associated issue are checked off

#### 3. Agent Implementation
If you implement a new agent:

```python
from opensquad.src.agents.base import BaseAgent, AgentConfig, AgentRole

class MyNewAgent(BaseAgent):
    def __init__(self, config: Optional[AgentConfig] = None):
        if config is None:
            config = AgentConfig(
                name="MyAgent",
                role=AgentRole.YOUR_ROLE,
                model="llama3",
                temperature=0.7
            )
        super().__init__(config)
    
    def get_system_prompt(self) -> str:
        """Define your agent's role and behavior"""
        return """You are a specialized agent for..."""
    
    async def process(self, task: str, context: Dict) -> Dict:
        """Implement your agent's logic"""
        # Your implementation here
        pass
```

#### 4. Integration in Orchestration
New agents must be integrated into the LangGraph workflow:

```python
# In orchestration/workflow.py
workflow.add_node("my_agent", self._my_agent_node)
workflow.add_edge("my_agent", "router")
```

#### 5. Testing
Every agent needs tests:

```python
# tests/agents/test_my_agent.py
async def test_my_agent_basic():
    agent = MyNewAgent()
    result = await agent.process("test task", {})
    assert result["status"] == "completed"
```

## 🎯 Best Practices for Agent Development

### DO ✅
- Respect clear role separation
- Use type hints
- Write docstrings
- Implement error handling
- Write tests
- Use context from shared state

### DON'T ❌
- Access other agents directly
- Develop without an issue
- Commit directly to `main`
- Mix agent roles
- Deploy without tests

## 🔧 Technical Details

### LLM Integration
Agents use Ollama for local LLM inference:

```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3",
    temperature=0.7,
    base_url="http://localhost:11434"
)
```

### Supported Models
- **llama3** (default) - Good for general tasks
- **mistral** - Fast, efficient
- **mixtral** - For more complex reasoning tasks

### Memory & State
- Conversation History via LangGraph's `add_messages`
- Shared Artifacts for code, designs, etc.
- Agent-specific State in `AgentState`

## 📚 Further Documentation

- [CONTRIBUTING.md](CONTRIBUTING.md) - Development Workflow
- [README.md](README.md) - Project Overview
- `docs/architecture.md` - Detailed Architecture (planned)
- `docs/langgraph.md` - LangGraph Integration (planned)

## 🚀 Quick Start for New Agents

```bash
# 1. Create issue
gh issue create --title "Implement XYZ Agent" --label "feature"

# 2. Create branch (e.g., Issue #10)
git checkout -b feature/10-implement-xyz-agent

# 3. Create agent file
touch src/agents/xyz_agent.py

# 4. Implement agent (see template above)

# 5. Write tests
touch tests/agents/test_xyz_agent.py

# 6. Commit & Push
git add .
git commit -m "feat: Add XYZ agent implementation (#10)"
git push -u origin feature/10-implement-xyz-agent

# 7. Create PR
gh pr create --title "Implement XYZ Agent" --body "Closes #10"
```

## ❓ Questions about the Agent System?

If you have questions about agent architecture:
- Open a GitHub Issue with label `question`
- Reference this file in the issue description

---

**This file is continuously updated with new agents and patterns.**
