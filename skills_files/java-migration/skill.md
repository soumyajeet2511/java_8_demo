name: java-migration
description: Fix Java 11 compatibility issues without modifying logic, APIs, or queries.
dependencies:
  - global-restrictions

---

# Java Migration Skill

## Purpose
Migrate Java 8 code to Java 11 compatibility.

## Allowed
- Fix removed APIs
- Fix imports
- Replace incompatible Java 8 usages
- Apply minimal syntax fixes required for Java 11

## Strict Prohibitions

### Business Logic
- Do NOT change logic
- Do NOT add validation
- Do NOT add new conditions

### API Contracts
- Do NOT change method signatures
- Do NOT change return types (Collection → List ❌)
- Do NOT change parameters
- Do NOT add default methods

### Data Layer
- Do NOT modify queries (SQL/JPQL/HQL)
- Do NOT modify @Query

### Refactoring
- Do NOT refactor code
- Do NOT introduce var
- Do NOT rewrite loops to streams

## Rule
If code works → DO NOT CHANGE

## Output
Patch JSON only