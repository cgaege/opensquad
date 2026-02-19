# 🤖 OpenSquad Agents – Systemdokumentation

Diese Datei dokumentiert das Multi-Agent System von OpenSquad und dient als Leitfaden für die Entwicklung und Nutzung der AI Agents.

## 📋 Übersicht

OpenSquad ist ein **Multi-Agent AI System**, das ein virtuelles Software-Entwicklerteam simuliert. Verschiedene spezialisierte Agents arbeiten zusammen, um komplexe Software-Engineering-Aufgaben zu lösen.

### System-Architektur

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

## 🎭 Agent-Rollen

### 1. Architect Agent 🏗️

**Verantwortlichkeiten:**
- Analyse von User Requirements
- System-Design und Architektur-Entscheidungen
- Task-Dekomposition (Breaking down in Sub-Tasks)
- Technologie-Stack Empfehlungen
- Definition von Interfaces zwischen Komponenten

**Typische Aufgaben:**
- "Design a REST API for user management"
- "Create architecture for a microservices system"
- "Decompose this feature into implementable tasks"

**Beispiel:**
```python
architect = ArchitectAgent()
result = await architect.create_task_plan(
    "Build a task management system with user auth"
)
```

### 2. Backend Agent 💻

**Verantwortlichkeiten:**
- API Design und Implementierung (REST/GraphQL)
- Datenbank-Schema Design
- Business Logic Implementierung
- Authentication & Authorization
- Backend Testing

**Typische Aufgaben:**
- "Implement the user authentication API"
- "Create database schema for tasks"
- "Add validation and error handling"

**Beispiel:**
```python
backend = BackendAgent()
result = await backend.implement_feature(
    feature="User registration endpoint",
    architecture=architect_output
)
```

### 3. Frontend Agent 🎨

**Verantwortlichkeiten:**
- UI/UX Implementierung
- Component-Architektur
- State Management
- API Integration
- Frontend Testing

**Status:** 🚧 Geplant für Phase 2

### 4. QA Agent 🧪

**Verantwortlichkeiten:**
- Test Case Generierung
- Automatisierte Tests schreiben
- Code Validation
- Bug Detection
- Test Coverage Analysis

**Status:** 🚧 Geplant für Phase 2

### 5. Reviewer Agent 👁️

**Verantwortlichkeiten:**
- Code Review
- Best Practices prüfen
- Security Review
- Performance-Optimierungen vorschlagen
- Dokumentation prüfen

**Status:** 🚧 Geplant für Phase 3

## 🔄 Agent Collaboration Workflow

### Typischer Ablauf

1. **User Input**: Task oder Anforderung wird gestellt
2. **Orchestrator**: Analysiert Task und routet zu geeignetem Agent
3. **Architect Agent**: Erstellt High-Level Plan und Architektur
4. **Backend/Frontend Agents**: Implementieren basierend auf Architektur
5. **QA Agent**: Validiert Implementierung und erstellt Tests
6. **Reviewer Agent**: Final Review und Feedback
7. **Orchestrator**: Sammelt Ergebnisse und liefert Output

### Agent-zu-Agent Kommunikation

Agents kommunizieren über **Shared State** (LangGraph StateGraph):

```python
class TeamState:
    messages: List[Message]           # Conversation History
    current_task: str                 # Aktuelle Aufgabe
    artifacts: Dict[str, Any]         # Shared Outputs
    next_agent: str                   # Routing Information
```

## 🛠️ Für AI-Tools: Entwicklungsanweisungen

### Wenn du ein neuer Agent bist oder mit diesem System arbeitest:

#### 1. System verstehen
- Lies diese AGENTS.md vollständig
- Verstehe die Multi-Agent Architektur
- Beachte die Rollen-Trennung

#### 2. Entwicklungs-Workflow befolgen
- **Issue-First**: Erstelle immer zuerst ein GitHub Issue
- **Feature Branches**: Niemals direkt auf `main` committen
- Branch-Format: `feature/issue-nummer-beschreibung`
- **Akzeptanzkriterien**: Issues dürfen nur geschlossen werden, wenn ALLE Akzeptanzkriterien erfüllt sind
- **PR Merge**: Pull Requests nur mergen, wenn alle Akzeptanzkriterien des zugehörigen Issues abgehakt sind

#### 3. Agent-Implementierung
Wenn du einen neuen Agent implementierst:

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
Neue Agents müssen in den LangGraph Workflow integriert werden:

```python
# In orchestration/workflow.py
workflow.add_node("my_agent", self._my_agent_node)
workflow.add_edge("my_agent", "router")
```

#### 5. Testing
Jeder Agent braucht Tests:

```python
# tests/agents/test_my_agent.py
async def test_my_agent_basic():
    agent = MyNewAgent()
    result = await agent.process("test task", {})
    assert result["status"] == "completed"
```

## 🎯 Best Practices für Agent-Entwicklung

### DO ✅
- Klare Rollen-Trennung beachten
- Type Hints verwenden
- Docstrings schreiben
- Fehlerbehandlung implementieren
- Tests schreiben
- Context aus Shared State nutzen

### DON'T ❌
- Agents direkt auf andere Agents zugreifen
- Ohne Issue entwickeln
- Direkt auf `main` committen
- Agent-Rollen vermischen
- Ohne Tests deployen

## 🔧 Technische Details

### LLM Integration
Agents nutzen Ollama für lokale LLM-Inferenz:

```python
from langchain_ollama import OllamaLLM

llm = OllamaLLM(
    model="llama3",
    temperature=0.7,
    base_url="http://localhost:11434"
)
```

### Unterstützte Modelle
- **llama3** (Standard) - Gut für allgemeine Aufgaben
- **mistral** - Schnell, effizient
- **mixtral** - Für komplexere Reasoning-Tasks

### Memory & State
- Conversation History via LangGraph's `add_messages`
- Shared Artifacts für Code, Designs, etc.
- Agent-spezifischer State in `AgentState`

## 📚 Weiterführende Dokumentation

- [CONTRIBUTING.md](CONTRIBUTING.md) - Development Workflow
- [README.md](README.md) - Projekt-Übersicht
- `docs/architecture.md` - Detaillierte Architektur (geplant)
- `docs/langgraph.md` - LangGraph Integration (geplant)

## 🚀 Quick Start für neue Agents

```bash
# 1. Issue erstellen
gh issue create --title "Implement XYZ Agent" --label "feature"

# 2. Branch erstellen (z.B. Issue #10)
git checkout -b feature/10-implement-xyz-agent

# 3. Agent-Datei erstellen
touch src/agents/xyz_agent.py

# 4. Agent implementieren (siehe Template oben)

# 5. Tests schreiben
touch tests/agents/test_xyz_agent.py

# 6. Commit & Push
git add .
git commit -m "feat: Add XYZ agent implementation (#10)"
git push -u origin feature/10-implement-xyz-agent

# 7. PR erstellen
gh pr create --title "Implement XYZ Agent" --body "Closes #10"
```

## ❓ Fragen zum Agent System?

Bei Fragen zur Agent-Architektur:
- GitHub Issue mit Label `question` öffnen
- In der Issue-Beschreibung auf diese Datei referenzieren

---

**Diese Datei wird laufend aktualisiert mit neuen Agents und Patterns.**
