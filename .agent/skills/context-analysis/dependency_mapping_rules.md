# Dependency Mapping Rules

To accurately identify the "ripple effect" of Java migration changes, follow these mapping rules:

## 1. Vertical Dependency Analysis
- **Top-Down**: If a Controller is modified, check the Services it uses.
- **Bottom-Up**: If a Repository or DTO is modified, check the Services and Controllers that consume it.

## 2. Horizontal Dependency Analysis
- **Interfaces**: If an Interface is modified (e.g., to resolve a Java 11 compatibility issue in a method signature), all implementing classes must be included in the analysis.
- **Inheritance**: If a Base Class is modified, all subclasses must be checked for compilation errors.

## 3. Search Heuristics
- Use `grep_search` to find string-based references to removed APIs across the entire project to estimate the total migration effort.
- Focus on `import` statements to quickly map high-level dependencies.

## 4. Token-Saving Inclusion Rules
- **Include**:
    - The file being modified.
    - Any direct implementation of an interface being modified.
    - Files that call a method whose signature is changing.
- **Exclude**:
    - Compiled `.class` files.
    - Test files (unless specifically fixing test failures).
    - Unrelated modules in a multi-module Maven project.
    - Third-party library source code.
