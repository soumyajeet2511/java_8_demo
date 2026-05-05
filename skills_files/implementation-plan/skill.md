
# Implementation Plan Skill

## description
Analyze project and generate Java 8 to Java 21 readiness plan.

## dependencies
- global-restrictions
- java-migration

---

## Skill References (MANDATORY)

This skill MUST read and align with:
- java-migration skill directory

---

## Rule

- Read java-migration rules before generating readiness
- Ensure readiness checklist matches what java-migration will execute

## Purpose
Analyze full codebase and generate readiness plan.

---

## Target
Java 21

---

## Output (MANDATORY)

Always generate readiness plan in markdown format, so that it can be generated as an artifact :

# Java 8 to Java 21 Migration Readiness Plan

---

## Required Sections

### Migration Checklist (MANDATORY)

- [ ] Update pom.xml to Java 21
- [ ] Verify dependencies compatibility
- [ ] Fix removed APIs
- [ ] Apply Java Modernization from java-migration/modernization(isBlank, List.of, etc.)
- [ ] Validate configuration
- [ ] Run build

---

### Strategy

- Follow phased compatibility:
  8 → 11 → 17 → 21
- Final target must remain Java 21

---

### Risks
List possible risks

---

## NEXT ACTION

STOP after readiness generation

Wait for user confirmation