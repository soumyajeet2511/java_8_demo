name: dependency-fix
description: Resolve build failures caused by missing or incompatible dependencies in pom.xml.
dependencies:
  - global-restrictions

---

# Dependency Fix Skill

## Purpose
Fix build failures related to dependencies.

## Allowed
- Add missing dependencies
- Upgrade incompatible dependencies
- Add JAXB if required

## Forbidden
- Do NOT modify Java code
- Do NOT remove dependencies blindly
- Do NOT change business logic

## Rule
Fix only dependency-related errors

## Output
Patch for pom.xml only