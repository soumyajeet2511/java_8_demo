name: global-restrictions
description: Global execution and safety rules for all skills.

---

# Global Restrictions (MANDATORY)

## Target Java Version
Java 21

All operations must align with migration from Java 8 → Java 21.

---

## Execution Policy

- Treat readiness plan as a CHECKLIST
- Do NOT stop after build success
- Continue until ALL readiness items are completed

---

## Coverage

- Process all relevant files
- Do NOT skip files silently

---

## Completion Criteria

Migration is complete ONLY when:
- All readiness checklist items are done
- Build is successful
- No pending steps remain

---

## Strict Prohibitions

### Business Logic
- Do NOT change logic
- Do NOT add validation

### API Contracts
- Do NOT change method signatures
- Do NOT change return types
- Do NOT add default methods

### Data Layer
- Do NOT modify queries (SQL/JPQL/HQL)
- Do NOT modify @Query

### Refactoring
- Do NOT refactor code
- Do NOT introduce var
- Do NOT convert loops to streams

---

## Type Safety

Forbidden:
- Collection → List
- List → ArrayList
- Map → HashMap

---

## Golden Rule

If code works → DO NOT TOUCH IT