# Testing HelloAgent with Ollama

This document explains how to test the HelloAgent implementation with a real Ollama instance.

## Prerequisites

1. **Ollama installed**: [Install from ollama.ai](https://ollama.ai)
2. **llama3 model pulled**: 
   ```bash
   ollama pull llama3
   ```

## Quick Test

### 1. Start Ollama (in a separate terminal)

```bash
ollama serve
```

### 2. Activate virtual environment

```bash
source .venv/bin/activate
```

### 3. Run the integration test script

```bash
python test_ollama_integration.py
```

This will run 3 tests:
- Simple greeting
- Error handling with empty message
- Technical question

### 4. Or use the CLI directly

```bash
python -m opensquad.cli.main hello "How are you?"
```

Or install as command:

```bash
pip install -e .
opensquad hello "What is Python?"
opensquad version
```

## Expected Output

### Integration Test Script

```
╭─────────────────────────────────────────╮
│ Testing HelloAgent with Ollama          │
╰─────────────────────────────────────────╯

Test 1: Simple greeting
✓ Success
Response: Hello! I'm doing great, thanks for asking!

Test 2: Error handling (empty message)
✓ Error handling works

Test 3: Technical question
✓ Success
Response: Python is a high-level programming language...

╭─────────────────────────────────────────╮
│ All tests passed! ✓                      │
╰─────────────────────────────────────────╯
```

### CLI Output

```
╭──────────────────────────────────────────╮
│ OpenSquad HelloAgent                      │
│ Model: llama3                             │
╰──────────────────────────────────────────╯

User: How are you?

Agent: Hello! I'm doing great, thanks for asking!

Model: llama3
```

## Troubleshooting

### Error: Connection refused

```
Error: Error processing task: HTTPConnectionPool(host='localhost', port=11434)...
```

**Solution**: Make sure Ollama is running:
```bash
ollama serve
```

### Error: Model not found

```
Error: model 'llama3' not found
```

**Solution**: Pull the llama3 model:
```bash
ollama pull llama3
```

### Error: Model takes too long to respond

This is normal for the first request as the model needs to load into memory. Subsequent requests will be much faster.

## What Gets Tested

The tests validate:

1. ✅ **Ollama Integration**: Agent can connect to and communicate with Ollama
2. ✅ **Message Processing**: Agent correctly formats prompts and processes responses
3. ✅ **Error Handling**: Agent gracefully handles empty/invalid inputs
4. ✅ **State Management**: Agent maintains proper state throughout processing
5. ✅ **Response Structure**: Agent returns well-formatted results

## Unit Tests (No Ollama Required)

The unit tests use mocks and don't require Ollama:

```bash
pytest tests/ -v
```

These tests validate the agent logic without external dependencies.

## Next Steps

Once HelloAgent works with Ollama:

1. ✅ BaseAgent architecture validated
2. ✅ Ollama integration confirmed
3. ⏳ Ready to implement ArchitectAgent
4. ⏳ Ready to add LangGraph orchestration
5. ⏳ Ready to implement multi-agent collaboration

## Issue #5 Acceptance Criteria

- ✅ BaseAgent class with abstract methods
- ✅ HelloAgent with Ollama integration  
- ✅ Basic error handling
- ✅ Simple CLI for testing
- ✅ Unit tests with >90% coverage
- 🔄 Manual verification with real Ollama (pending user testing)

Close Issue #5 after successful manual testing with Ollama.
