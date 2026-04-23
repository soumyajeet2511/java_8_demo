# Java 8 to 11 Migration Rules

## 1. Removed/Deprecated API Replacements
- **JAXB**: `javax.xml.bind.*` is removed from the JDK. If found, ensure imports are ready for `jakarta.xml.bind` or equivalent (coordinated with `dependency-fix`).
- **JAF**: `javax.activation.*` is removed.
- **Common Annotations**: `javax.annotation.Generated` etc. are removed. Update to `javax.annotation.processing.Generated` or use external dependency.
- **Corba & JTA**: Removed from JDK.

## 2. Syntax Compatibility
- **Underscore**: `_` is a keyword and cannot be used as an identifier. Rename to `_1` or a more descriptive name if encountered.
- **Var**: While `var` is available, avoid its use unless it significantly improves readability in complex generic types. Prioritize explicit types to minimize diff noise.

## 3. Collections and Streams
- Keep existing Stream logic. Do not "modernize" for the sake of using newer methods like `toList()` unless the original code used `Collectors.toList()`.

## 4. Module System
- Ensure code does not rely on `sun.*` internal packages. If found, identify the public API alternative.
- For most migrations, we treat the code as being on the "unnamed module" to simplify the transition.
