
# Java Migration Skill

## description
Execute migration from Java 8 to 21 using readiness plan.

## dependencies
- global-restrictions
- modernization

## Purpose
Execute migration using readiness checklist.

---

## Target
Java 21

---

## Input Requirement

- Read readiness from chat
- Treat checklist as mandatory

---

## Execution Rules

- Process ALL checklist items
- Do NOT stop after build success
- Do NOT skip files

---

## Strategy

Internally follow phases:
- 8 → 11
- 11 → 17
- 17 → 21

---

## Allowed

- Fix removed APIs
- Fix imports
- Minimal compatibility fixes

---

## Forbidden

- Do NOT change logic
- Do NOT modify queries
- Do NOT change API contracts

---

## NEXT ACTION

→ Trigger build-run