# Contributing to OpenSquad

Vielen Dank für dein Interesse an OpenSquad! Dieses Dokument beschreibt unsere Entwicklungsrichtlinien und Best Practices.

## 🔄 Development Workflow

### 1. Issue-First Ansatz

**Jede Änderung beginnt mit einem GitHub Issue.**

- Erstelle ein Issue für jedes neue Feature, jeden Bugfix oder jede Verbesserung
- Beschreibe das Problem oder die Anforderung klar
- Definiere Akzeptanzkriterien
- Label hinzufügen (`feature`, `bug`, `documentation`, etc.)

**Beispiel Issue:**
```
Title: Implement QA Agent
Body:
## Ziel
QA Agent implementieren für automatisierte Testing und Validation

## Aufgaben
- [ ] Agent-Klasse erstellen
- [ ] Test-Framework Integration
- [ ] Unit Tests schreiben

## Akzeptanzkriterien
- [ ] QA Agent kann Test Cases generieren
- [ ] Tests werden ausgeführt und Ergebnisse zurückgegeben
```

### 2. Feature Branch Strategie

**Niemals direkt auf `main` committen.**

#### Branch Naming Convention
```
feature/issue-nummer-kurze-beschreibung
bugfix/issue-nummer-kurze-beschreibung
docs/issue-nummer-kurze-beschreibung
```

**Beispiele:**
- `feature/5-implement-qa-agent`
- `bugfix/12-fix-ollama-connection`
- `docs/8-update-api-documentation`

#### Workflow
```bash
# 1. Issue erstellen (z.B. Issue #5)
gh issue create --title "Implement QA Agent" --label "feature"

# 2. Feature Branch erstellen
git checkout -b feature/5-implement-qa-agent

# 3. Entwicklung durchführen
# ... code changes ...

# 4. Commits mit Issue-Referenz
git commit -m "feat: Add QA agent base class (#5)"

# 5. Branch pushen
git push -u origin feature/5-implement-qa-agent

# 6. Pull Request erstellen
gh pr create --title "Implement QA Agent" --body "Closes #5"

# 7. Nach Review: Merge auf main
# 8. Branch löschen
git branch -d feature/5-implement-qa-agent
```

### 3. Commit Message Convention

Wir folgen [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description> (#issue-nummer)

[optional body]

[optional footer]
```

**Types:**
- `feat:` - Neues Feature
- `fix:` - Bugfix
- `docs:` - Dokumentation
- `refactor:` - Code-Refactoring
- `test:` - Tests hinzufügen/ändern
- `chore:` - Build, Dependencies, etc.

**Beispiele:**
```bash
git commit -m "feat: Add architect agent implementation (#3)"
git commit -m "fix: Correct ollama connection timeout (#7)"
git commit -m "docs: Update AGENTS.md with workflow examples (#2)"
```

## 🤖 Entwicklung mit AI-Tools

### Für GitHub Copilot / VS Code Nutzer

Bei der Nutzung von AI-Tools (GitHub Copilot, Claude, ChatGPT) für die Entwicklung:

1. **Kontext bereitstellen**: Verweise auf AGENTS.md und relevante Dokumentation
2. **Issue-Nummer erwähnen**: "Implementiere Feature für Issue #5"
3. **Workflow einhalten**: AI soll Issue-first und Feature Branches respektieren
4. **Code Review**: AI-generierter Code muss reviewed werden

### Beispiel-Prompt für AI
```
Ich arbeite an Issue #5 (QA Agent implementieren).
Bitte erstelle die QA Agent Klasse entsprechend der 
Architektur in AGENTS.md. Der Code soll auf dem Branch 
feature/5-implement-qa-agent erstellt werden.
```

## 📋 Pull Request Guidelines

### Vor dem PR
- [ ] Code läuft lokal ohne Fehler
- [ ] Tests geschrieben und bestehen
- [ ] Dokumentation aktualisiert
- [ ] Issue-Referenz im PR

### PR Template
```markdown
## Änderungen
Kurze Beschreibung der Änderungen

## Issue
Closes #issue-nummer

## Testing
Wie wurde getestet?

## Checklist
- [ ] Tests hinzugefügt
- [ ] Dokumentation aktualisiert
- [ ] Code reviewed
```

## 🏗️ Projektstruktur

```
opensquad/
├── src/                # Source Code
│   ├── agents/         # Agent-Implementierungen
│   ├── orchestration/  # LangGraph Workflows
│   ├── memory/         # State Management
│   └── tools/          # Agent Tools
├── tests/              # Tests
├── docs/               # Dokumentation
├── examples/           # Beispiele
└── config/             # Konfiguration
```

## 🧪 Testing

```bash
# Tests ausführen
pytest tests/

# Mit Coverage
pytest --cov=src tests/

# Spezifische Tests
pytest tests/agents/test_architect_agent.py
```

## 📝 Code Style

- Python 3.11+
- Type Hints verwenden
- Docstrings für Klassen und Funktionen
- Max. Line Length: 100 Zeichen

## ❓ Fragen?

Bei Fragen oder Unklarheiten:
- GitHub Issue öffnen mit Label `question`
- Diskussion starten in GitHub Discussions

## 🙏 Danke!

Vielen Dank für deine Contribution zu OpenSquad!
