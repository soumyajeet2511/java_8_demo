name: build-run
description: Execute Maven build and return output only.
dependencies:
  - global-restrictions

---

# Build Run Skill

## Command
mvn clean install
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

## NEXT ACTION (MANDATORY)

If build fails:

- Do NOT stop
- Do NOT suggest manually

→ Automatically pass error logs to routing-rules
→ Continue execution as per error fix