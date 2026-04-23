# Build Fix Skill

## Name
build-fix

## Description
Analyzes and fixes Maven compilation and runtime build failures following a Java migration. It identifies the root cause of errors (missing symbols, type mismatches, etc.) and applies minimal changes to restore build stability.

## When to use
- Fixing compilation errors reported by `mvn clean install`.
- Resolving runtime failures during tests (`mvn test`).
- Handling cascading compilation failures where one fix reveals more errors.

## When NOT to use
- Upgrading `pom.xml` dependencies (use `dependency-fix` for manifest changes).
- Initial source code migration (use `java-migration` first).
- Debugging complex logical bugs unrelated to the Java 11 transition.

## Inputs
- Compilation error logs from Maven.
- Source code of the failing file(s).
- Build context (`pom.xml` for reference).

## Outputs
- Fixed source code file(s).
- Analysis of the fix strategy applied.
- List of remaining or new errors (if any).

## Strict Constraints
- **Minimal Fix**: Only change code that is directly responsible for the build failure.
- **No Refactoring**: Do not clean up unrelated code.
- **Maintain Semantics**: Ensure the fix doesn't change the underlying logic.
- **Check for Cascades**: After applying a fix, verify if it resolves multiple errors or creates new ones.

## Execution Workflow (Autonomous Loop)
This skill operates as an autonomous loop until the build succeeds.
1. **Run Build**: Execute `mvn clean install` using the terminal tool.
2. **Analyze Output**: If the build succeeds, terminate the loop. If it fails, capture the error logs, file paths, and line numbers.
3. **Classify Errors**: Identify the type of error (Missing Class, Type Mismatch, Removed API) using `error_patterns.md`.
4. **Apply Fix**: Modify the source code using precision edits (search and replace format) to resolve the error.
5. **Verify and Repeat**: Immediately loop back to step 1 to re-run the build. Continue this cycle until `mvn clean install` completes without any errors.

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

## Decision Tree: Fix Strategy
1. Is it a "Symbol Not Found" error?
    - Yes: Is it a Java standard library class?
        - Yes: It might be removed from JDK (e.g., JAXB). Coordinate with `dependency-fix` or update imports if moved.
        - No: Is it a project class?
            - Yes: Check if the dependency class was renamed or moved.
    - No: Is it a "Type Mismatch"?
        - Yes: Check for API return type changes in Java 11 (e.g., generic changes).
    - No: Is it a "Cannot access" error?
        - Yes: Likely an internal API access issue. Use `java-migration` rules to find alternative.
