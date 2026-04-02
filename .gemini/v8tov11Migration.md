# Java 8 to Java 11 Migration Rules

## Objective

Migrate Java 8 code to Java 11 while preserving existing functionality, ensuring successful compilation, and keeping changes minimal and safe.

---

## Core Principles

* Do not change business logic or business rules
* Do not remove or delete any existing code unless absolutely necessary to fix a compilation error
* Do not remove methods, classes, or logic even if they appear unused
* Fix only what is required for Java 11 compatibility
* Prefer minimal and safe changes
* Ensure code compiles successfully after changes
* Preserve existing behavior exactly as-is
* Keep code clean, readable, and production-ready


---

## General Rules

* Update Java version to 11 where required
* Fix broken imports and missing packages
* Replace deprecated or removed APIs
* Ensure all code compiles without errors
* Do not remove dependencies unless necessary

---

## Java 11 Language and API Updates

### Collections

* Replace `Arrays.asList(...)` with `List.of(...)` where safe
* Do not use `Stream.toList()` (not supported in Java 11)
* Use `.collect(Collectors.toList())` instead

---

### Strings

* Replace `str.trim().isEmpty()` with `str.isBlank()`
* Use `strip()`, `isBlank()`, and `lines()` where applicable

---

### Local Variables

* Use `var` only when the type is obvious and improves readability

Example:

```java
var list = new ArrayList<String>();
```

---

### HTTP Client

* Suggest Java 11 HttpClient only if an old or legacy client is detected

---

### Underscore Restriction

* Do not use `_` as a variable name (invalid in Java 11)

---

## POM.xml Rules

* Set Java version to 11
* Update `maven-compiler-plugin` to version 3.11.0 or higher
* Ensure compatibility with Java 11
* Do not remove dependencies unless required

---

## Common Java 11 Fixes

### JAXB Issue

If the following error appears:

```
javax.xml.bind not found
```

Then:

* Add JAXB dependencies in `pom.xml`

---

### Lombok / MapStruct Issue

If the following error appears:

```
NoSuchFieldError: JCTree
```

Then:

* Upgrade Lombok to version 1.18.30 or higher
* Upgrade MapStruct to version 1.5.5.Final or higher
* Ensure `annotationProcessorPaths` is configured in `pom.xml`

---

## Error Handling Rules

* Always fix the root cause of the error
* Prefer adding dependencies over removing code
* Keep fixes minimal and targeted

---

## Modification Strategy

For Java files:

* Apply small, precise changes
* Do not rewrite the entire file
* Do not delete existing logic unless required to fix a compilation issue
* Preserve structure and flow of the original code

For `pom.xml`:

* Full update is allowed if necessary

---

## Response Format (Mandatory)

Return only JSON in the following format:

```json
[
  {
    "file": "path/to/file.java",
    "edits": [
      {
        "search": "EXACT EXISTING CODE",
        "replace": "UPDATED CODE"
      }
    ]
  }
]
```

---

## Important Constraints

* The `search` value must match the exact code, including spacing
* Keep edits small to avoid token limitations
* Do not include explanations
* Do not return partial JSON

---

## Agent Behavior

* Fix only the current error
* Do not over-modify code
* Ensure the build passes after applying the fix
* Prefer safe and reversible changes

---

## Final Goal

The project should:

* Compile successfully on Java 11
* Maintain original functionality
* Follow modern Java practices where safe
