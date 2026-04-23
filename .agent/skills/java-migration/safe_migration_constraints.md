# Safe Migration Constraints

To ensure a high-quality, low-risk migration, the following constraints are MANDATORY:

1. **Functional Equivalence**: The behavior of the code after migration must be identical to the behavior before migration.
2. **No Refactoring**: Do not clean up "code smells" (e.g., long methods, unused variables) unless they directly cause a compilation error in Java 11.
3. **Signature Preservation**: Do not change method access levels (private/public), return types, or parameter lists.
4. **Minimal Diff**: Aim for the smallest possible change set. If a file can compile in Java 11 with zero changes, do not touch it.
5. **Architectural Integrity**: Do not introduce new design patterns, dependency injection changes, or architectural shifts.
6. **No Library Swaps**: Do not replace a library (e.g., Guava to Stream API) unless the library itself is incompatible with Java 11.
7. **Comment Preservation**: Keep all original comments, Javadocs, and licensing headers intact.
