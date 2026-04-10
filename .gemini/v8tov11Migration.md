# Java 8 to Java 11 Migration: Strategic Guidelines and Rules

## 1. Primary Objective
The goal is to migrate Java 8 applications to Java 11 (LTS) while ensuring zero regressions in business logic. The migration must result in a codebase that is secure, follows modern Java 11 patterns, and passes all Maven lifecycle stages (clean, compile, test).

---

## 2. Core Development Principles
* **Preserve Logic**: Do not modify business rules, algorithms, or functional behavior.
* **Minimal Intervention**: Only modify code that is strictly required for Java 11 compatibility or specifically requested for modernization.
* **Code Integrity**: Do not delete methods, classes, or configuration blocks unless they are deprecated/removed in Java 11 and have a direct replacement.
* **Production Ready**: Maintain existing code formatting and ensure the result is clean and readable.

---

## 3. General Migration Requirements
* **Compiler Target**: Ensure the Java version in configuration files is set to 11.
* **Import Management**: Automatically resolve and add missing imports (e.g., `java.util.List`, `java.util.Optional`, `java.util.stream.Collectors`).
* **API Compatibility**: Replace deprecated or removed APIs with their supported Java 11 equivalents.
* **Dependency Safety**: Do not remove existing dependencies from `pom.xml` unless they are explicitly incompatible with Java 11.

---

## 4. Java 11 Language & API Standards

### 4.1 Collections and Streams
* Replace `Arrays.asList(...)` with the immutable `List.of(...)` where appropriate and safe.
* **Constraint**: `Stream.toList()` is not available in Java 11. Use `.collect(Collectors.toList())` instead.

### 4.2 String Utilities
* Use `String.isBlank()` instead of checking `trim().isEmpty()`.
* Utilize `strip()`, `stripLeading()`, `stripTrailing()`, and `lines()` for cleaner string handling.

### 4.3 IO Improvements
* Prefer `Files.readString(Path)` for reading entire files into strings where applicable.

### 4.4 Date and Time API
* Transition from legacy `java.util.Date` and `java.util.Calendar` to the modern `java.time` package (e.g., `LocalDate`, `LocalDateTime`, `ZonedDateTime`).

### 4.5 DatatypeConverter (JAXB Removal)
* `javax.xml.bind.DatatypeConverter` was removed from the JDK 11.
* **Replacement for Hex**: Use `new java.math.BigInteger(hex, 16).toByteArray()` or a dedicated utility class.
* **Replacement for Base64**: Use the native `java.util.Base64` class.

### 4.6 Local Variable Type Inference
* Use the `var` keyword only when the type is clearly obvious from the right-hand side of the assignment (e.g., `var list = new ArrayList<String>();`).

---

## 5. Security Modernization (Mandatory)

### 5.1 SQL Injection Prevention
* **Rule**: Eliminate string concatenation in SQL queries.
* **Action**: Convert unsafe queries to use `PreparedStatement` with parameterized placeholders (`?`).

### 5.2 Hardcoded Credentials
* **Rule**: Do not store passwords, secrets, or API keys in source code.
* **Action**: Retrieve sensitive data from environment variables (`System.getenv`) or via Spring's `@Value` annotation.

### 5.3 Cross-Site Scripting (XSS)
* **Rule**: Sanitize user-provided input before including it in HTML or web responses.
* **Action**: Use standard sanitization libraries or escape functions (e.g., `HtmlUtils.htmlEscape`).

### 5.4 Path Traversal
* **Rule**: Validate all user-controlled file paths.
* **Action**: Use `Path.normalize()` and verify that the resulting path remains within the intended base directory.

### 5.5 Sensitive Data Leakage
* **Rule**: Prevent the exposure of sensitive fields (e.g., `password`, `ssn`) in logs or API responses.
* **Action**: Remove these fields from `toString()` methods and ensure they are not serialized to JSON.

---

## 6. Build Configuration (pom.xml)
* Update `maven-compiler-plugin` to version 3.11.0 or higher.
* Ensure `<release>11</release>` or `<source>11</source>` and `<target>11</target>` properties are correctly set.
* **JAXB Support**: If `javax.xml.bind` errors occur, add the necessary JAXB dependencies to the `pom.xml`.
* **Lombok/MapStruct**: If compilation errors like `NoSuchFieldError: JCTree` appear, upgrade Lombok to >= 1.18.30 and MapStruct to >= 1.5.5.Final.

---

## 7. Operational Guidelines for the Agent
* **Iterative Fixes**: Focus on resolving the immediate compilation error reported by the build.
* **Precision Edits**: When updating Java files, use the "search and replace" format to provide surgical changes rather than rewriting the full file.
* **JSON Protocol**: All responses must strictly follow the JSON schema provided below for automated processing.

### Response Schema
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

---

## 8. Final Success Criteria
1. The application compiles successfully using Java 11.
2. All business functionality remains intact.
3. Code adopts safe Java 11 syntax and passes basic security checks.
