name: error-mapping
description: Map build errors to correct skill.

---

# Error Mapping

## Dependency Errors
- "package ... does not exist"
- "class not found"
- "cannot resolve symbol"
- "method not found"
- "cannot find symbol"

→ dependency-fix

---

## Compilation Errors
- "cannot find symbol"
- syntax issues
- missing symbols
- type mismatch
- compilation failure

→ java-migration

---

## Config Errors
- plugin issues
- compiler version mismatch

→ config-fix