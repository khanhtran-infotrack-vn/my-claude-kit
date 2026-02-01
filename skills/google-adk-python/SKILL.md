---
name: google-adk-python
description: Build AI agents with Google's Agent Development Kit (ADK) Python - an open-source, code-first toolkit for building, evaluating, and deploying AI agents. Capabilities include LlmAgent (dynamic routing, adaptive behavior), workflow agents (SequentialAgent, ParallelAgent, LoopAgent), tool integration (google_search, code_execution, custom functions, OpenAPI), multi-agent systems with hierarchical coordination, and human-in-the-loop approval flows. Use when building AI agents with tool integration, creating multi-agent systems, implementing workflow pipelines, integrating with Google Search or code execution, deploying agents to Vertex AI or Cloud Run, or implementing agent evaluation and testing.
---

# Google ADK Python

Build AI agents with Google's Agent Development Kit - code-first toolkit for agent orchestration.

## Installation

```bash
pip install google-adk
```

## Quick Start

```python
from google.adk.agents import LlmAgent
from google.adk.tools import google_search

# Single agent with tools
agent = LlmAgent(
    name="search_assistant",
    model="gemini-2.5-flash",
    instruction="Search the web for information.",
    tools=[google_search]
)

# Multi-agent system
researcher = LlmAgent(name="Researcher", model="gemini-2.5-flash", tools=[google_search])
writer = LlmAgent(name="Writer", model="gemini-2.5-flash")
coordinator = LlmAgent(name="Coordinator", model="gemini-2.5-flash", sub_agents=[researcher, writer])
```

## Agent Types

| Type | Use Case |
|------|----------|
| `LlmAgent` | Dynamic routing, adaptive behavior, tool use |
| `SequentialAgent` | Execute agents in order |
| `ParallelAgent` | Run agents concurrently |
| `LoopAgent` | Repeat with iteration logic |

## Key Patterns

```python
# Custom tool
from google.adk.tools import Tool
def calculate(a: int, b: int) -> int:
    """Calculate sum."""
    return a + b
tool = Tool.from_function(calculate)

# Workflow
from google.adk.agents import SequentialAgent, ParallelAgent
workflow = SequentialAgent(name="pipeline", agents=[researcher, summarizer, writer])
parallel = ParallelAgent(name="parallel", agents=[agent1, agent2, agent3])

# Human approval
agent = LlmAgent(name="careful", tools=[google_search], tool_confirmation=True)
```

## Deployment

```bash
# Cloud Run
docker build -t my-agent . && gcloud run deploy my-agent --image my-agent

# Or deploy to Vertex AI Agent Engine
```

## Model Support

- Gemini 2.5 (flash/pro), Gemini 1.5 (flash/pro)
- Model-agnostic: supports other LLM providers via standard APIs

## Best Practices

1. Code-first: Define agents in Python for version control and testing
2. Modular design: Create specialized agents, compose into systems
3. Use workflow agents for predictable pipelines, LlmAgent for dynamic routing
4. Implement confirmation flows for sensitive operations
5. Test locally with development UI before deployment

## Resources

- GitHub: https://github.com/google/adk-python
- Docs: https://google.github.io/adk-docs/
- llms.txt: https://raw.githubusercontent.com/google/adk-python/refs/heads/main/llms.txt
