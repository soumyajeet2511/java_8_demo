name: context-window
description: Select minimal and relevant code context for processing.
dependencies:
  - global-restrictions

---
# Context Window Skill

## Purpose
Prepare safe and minimal context for the agent.

## Rules
- Include only relevant files
- Limit context size
- Prefer:
  - failing files
  - related classes
  - pom.xml (if needed)

## Forbidden
- Do NOT include entire project blindly
- Do NOT include unrelated files

## Output
Provide only necessary code context for next step