name: build-run
description: Execute Maven build and return success or error logs without modifying code.
dependencies:
  - global-restrictions

---
# Build Run Skill

## Purpose
Compile project and return result.

## Command
mvn clean compile

## Output

### Success
BUILD SUCCESS

### Failure
Return full error logs

## Rules
- Do NOT modify code
- Only execute build