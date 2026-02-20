# Contributing to OpenSquad

Thank you for your interest in OpenSquad! This document describes our development guidelines and best practices.

## 🔄 Development Workflow

### Core Principles

1. **Issue-First**: Every change starts with a GitHub Issue
2. **Feature Branches**: Never commit directly to `main`
3. **Conventional Commits**: Always use Conventional Commit Messages

### 1. Issue-First Approach

**Every change starts with a GitHub Issue.**

- Create an issue for every new feature, bugfix, or improvement
- Describe the problem or requirement clearly
- Define acceptance criteria
- Add labels (`feature`, `bug`, `documentation`, etc.)

**Example Issue:**
```
Title: Implement QA Agent
Body:
## Goal
Implement QA Agent for automated testing and validation

## Tasks
- [ ] Create agent class
- [ ] Test framework integration
- [ ] Write unit tests

## Acceptance Criteria
- [ ] QA Agent can generate test cases
- [ ] Tests are executed and results returned
```

### 2. Feature Branch Strategy

**Never commit directly to `main`.**

#### Branch Naming Convention
```
feature/issue-number-short-description
bugfix/issue-number-short-description
docs/issue-number-short-description
```

**Examples:**
- `feature/5-implement-qa-agent`
- `bugfix/12-fix-ollama-connection`
- `docs/8-update-api-documentation`

#### Workflow
```bash
# 1. Create issue (e.g., Issue #5)
gh issue create --title "Implement QA Agent" --label "feature"

# 2. Create feature branch
git checkout -b feature/5-implement-qa-agent

# 3. Develop
# ... code changes ...

# 4. Commit with issue reference
git commit -m "feat: Add QA agent base class (#5)"

# 5. Push branch
git push -u origin feature/5-implement-qa-agent

# 6. Create pull request
gh pr create --title "Implement QA Agent" --body "Closes #5"

# 7. After review: Merge to main
# 8. Delete branch
git branch -d feature/5-implement-qa-agent
```

### 3. Commit Message Convention

**⚠️ IMPORTANT: Always use Conventional Commit Messages!**

We strictly follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```
<type>: <description> (#issue-number)

[optional body]

[optional footer]
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring
- `test:` - Add/modify tests
- `chore:` - Build, dependencies, etc.

**Examples:**
```bash
git commit -m "feat: Add architect agent implementation (#3)"
git commit -m "fix: Correct ollama connection timeout (#7)"
git commit -m "docs: Update AGENTS.md with workflow examples (#2)"
```

**Why Conventional Commits?**
- Automatic changelog generation
- Semantic versioning
- Better traceability of changes
- Standard for modern projects

## 🤖 Development with AI Tools

### For GitHub Copilot / VS Code Users

When using AI tools (GitHub Copilot, Claude, ChatGPT) for development:

1. **Provide context**: Reference AGENTS.md and relevant documentation
2. **Mention issue number**: "Implement feature for Issue #5"
3. **Follow workflow**: AI should respect issue-first and feature branches
4. **Code review**: AI-generated code must be reviewed

### Example Prompt for AI
```
I'm working on Issue #5 (implement QA Agent).
Please create the QA Agent class according to the 
architecture in AGENTS.md. The code should be created on the 
feature/5-implement-qa-agent branch.
```

## 📋 Pull Request Guidelines

### Before PR
- [ ] Code runs locally without errors
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Issue reference in PR

### PR Template
```markdown
## Changes
Brief description of changes

## Issue
Closes #issue-number

## Testing
How was this tested?

## Checklist
- [ ] Tests added
- [ ] Documentation updated
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
├── docs/               # Documentation
├── examples/           # Examples
└── config/             # Configuration
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=src tests/

# Specific tests
pytest tests/agents/test_architect_agent.py
```

## 📝 Code Style

- Python 3.11+
- Use type hints
- Docstrings for classes and functions
- Max. line length: 100 characters

## ❓ Questions?

If you have questions or need clarification:
- Open a GitHub Issue with label `question`
- Start a discussion in GitHub Discussions

## 🙏 Thank You!

Thank you for your contribution to OpenSquad!
