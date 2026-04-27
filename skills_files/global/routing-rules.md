name: routing
description: Select next skill based on error.
dependencies:
  - error-mapping

---

# Routing Rules

## After Build Failure

Use error-mapping:

- dependency error → dependency-fix
- config error → config-fix
- code error → java-migration

---

## Loop

Fix → Build → Fix → Build

Until success