---
name: prompt-engineering
description: Optimize Claude API prompts for quality and token efficiency. Analyze system prompts, improve output format constraints, and tune Haiku vs Sonnet usage for cost efficiency.
origin: local
---

# Prompt Engineering

Analyze and optimize Claude API prompts for quality, consistency, and cost.

## When to Activate
- AI response quality issues (too long, wrong format, hallucination)
- Token cost reduction requests
- System prompt modification in service files
- Followup question quality improvement

## Model Selection Guide

| Model | Use Case | Max Tokens |
|-------|----------|------------|
| Haiku | Short answers, real-time streaming, simple classification | 100–300 |
| Sonnet | Complex structured output, reasoning, long content | 1000–8000 |
| Opus | Strategic decisions, high-stakes analysis | varies |

## Optimization Principles

### 1. Explicit Output Format
```python
# Vague — model decides format
system = "You are a career advisor."

# Explicit — format enforced
system = """You are a career advisor.
Rules:
- Answer in 1-2 sentences maximum
- No markdown headers (##, ###)
- Maximum 3 bullet points
- Do not end with a question"""
```

### 2. Token Efficiency
```python
# Remove unnecessary preamble
# BAD: "Of course! I'd be happy to help you with that question."
# GOOD: Start with the actual answer

# Use few-shot examples to teach format
examples = [
    {"role": "user", "content": "What is JWT?"},
    {"role": "assistant", "content": "A server-signed token for stateless auth. Structure: header.payload.signature."}
]
```

### 3. Hallucination Prevention
```python
system += "\nIf unsure about a specific technology or certification, say 'verify this' rather than guessing."
```

### 4. Structured JSON Output
```python
system = """Return valid JSON only, no markdown code blocks.
Schema: {"items": [{"name": str, "priority": 1-5, "reason": str}]}"""
```

### 5. Streaming Considerations
- For SSE streaming: keep chunks meaningful (not single chars)
- Set `stream=True` only when frontend expects streaming
- `max_tokens` for streaming: set conservatively to control costs

## Measurement
- Response length: before/after average token count
- Quality: user thumbs up/down ratio (if feedback system exists)
- Followup engagement: click-through rate on generated suggestions
