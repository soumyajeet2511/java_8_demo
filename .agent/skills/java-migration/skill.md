# Java Migration Skill

## Name
java-migration

## Description
Safely migrates Java 8 source code to Java 11 by addressing deprecated APIs, updating syntax where necessary for compatibility, and ensuring safe import updates without altering business logic.

## When to use
- Migrating individual Java source files from Java 8 to Java 11.
- Replacing deprecated APIs that were removed or changed in Java 9, 10, or 11.
- Updating syntax to comply with Java 11 standards (e.g., handling internal API access changes).

## When NOT to use
- Performing large-scale architectural refactoring.
- Renaming classes or changing public method signatures (unless required by an interface change in a library).
- Upgrading build tools or `pom.xml` (use `dependency-fix` instead).
- Adding new features or changing business logic.

## Inputs
- Java 8 source file(s) content.
- Migration context (e.g., target Java version, specific library versions).
- Compilation error logs (optional, if migrating as a fix).

## Outputs
- Migrated Java 11 source file(s).
- Summary of changes made (APIs replaced, imports updated).

## Strict Constraints
- **Preserve Business Logic**: Never modify the logic or flow of the application.
- **Minimal Modernization**: Do not use "newer" features (like `var`) unless they solve a specific compatibility issue or are clearly obvious from right-hand side (e.g. `var list = new ArrayList<String>();`). Focus on *compatibility* and *security*, not just style.
- **No Renaming**: Keep all class, method, and variable names identical.
- **Safe Imports**: Only update imports for moved or renamed standard library classes (e.g., `javax.xml.bind` packages). Auto-resolve missing imports (e.g., `java.util.List`).
- **No Hallucinated APIs**: Only use verified Java 11+ or library-equivalent APIs.
- **Security Modernization (Mandatory)**: Must address SQL Injection, Hardcoded Credentials, XSS, Path Traversal, and Sensitive Data Leakage.

## Execution Workflow
1. **Analyze File**: Read the source code and identify Java 8 specific patterns, deprecated APIs, or security vulnerabilities.
2. **Consult Rules**: Refer to `migration_rules.md` and Java 11 Standards (e.g. `List.of`, `String.isBlank()`, `java.time` API, JAXB alternatives like `java.util.Base64`) for specific replacement patterns.
3. **Apply Changes**: Perform replacements in a single pass to maintain consistency.
4. **Verify Constraints**: Cross-check against `safe_migration_constraints.md` and ensure zero regressions.
5. **Output**: Return the modified code with a concise change log using the JSON response schema.

### Response Schema
All responses must strictly follow the JSON schema for automated processing:
```json
[
  {
    "file": "path/to/target/file.java",
    "edits": [
      {
        "search": "EXACT_ORIGINAL_CODE_BLOCK",
        "replace": "MODERNIZED_CODE_BLOCK"
      }
    ]
  }
]
```

## Decision Tree: API Replacement
1. Is the API deprecated/removed in Java 11?
    - Yes: Is there a direct standard library replacement?
        - Yes: Use the standard replacement.
        - No: Is there a common external library replacement (e.g., Jakarta EE)?
            - Yes: Suggest the replacement and notify the user (requires `dependency-fix`).
            - No: Flag as a manual migration requirement.
    - No: Keep existing code.
