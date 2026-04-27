name: java-modernization
description: Apply safe Java 11–21 code improvements without changing behavior.
dependencies:
  - global-restrictions

---

# Java Modernization Skill

## Purpose
Enhance code using modern Java features after compatibility migration.

---

## Target
Java 21

---

## Allowed Improvements (SAFE ONLY)

### String
- trim().isEmpty() → isBlank()

### Collections
- Arrays.asList() → List.of() (ONLY if immutable behavior matches)

### Optional
- Simplify Optional usage (no logic change)

### Date/Time (VERY LIMITED)
- Only replace if no behavior change

---

## Forbidden

- Do NOT change logic
- Do NOT change method signatures
- Do NOT change return types
- Do NOT modify queries
- Do NOT introduce behavior changes

---

## Rule

Only apply changes that:
- are 100% behavior-safe
- do not affect other classes

If unsure → SKIP

---

## Execution

- Scan all files (not only failing ones)
- Apply improvements where safe

---

## NEXT ACTION

→ STOP (no build required unless explicitly asked)