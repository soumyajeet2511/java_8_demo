name: build-run
description: Execute Maven build and return output only.
dependencies:
  - global-restrictions

---

# Build Run Skill

## Command
mvn clean compile
---

## Output

### Success
BUILD SUCCESS

### Failure
Return raw error logs only

---

## STRICT RULES

- Do NOT analyze
- Do NOT fix
- Do NOT suggest

---

## NEXT ACTION

If success → STOP

If failure →
→ Pass logs to routing-rules