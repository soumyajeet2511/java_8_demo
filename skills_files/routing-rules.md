# Routing Rules

## Purpose
Select correct skill based on context or error.

## Rules

### If no error
→ Use java-migration

### If pom.xml issue
→ Use config-fix

### If dependency error
→ Use dependency-fix

### If compilation error
→ Use java-migration

### If build requested
→ Use build-run

## Strict Rule
- Use only ONE skill at a time
- Do NOT mix skills