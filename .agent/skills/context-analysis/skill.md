# Context Analysis Skill

## Name
context-analysis

## Description
Analyzes the codebase to understand the impact of changes before they are applied. It identifies related files, dependency chains, and potential "ripple effects" of a Java 8 to 11 migration.

## When to use
- Before starting a migration on a specific class or module.
- When a change in one file (e.g., updating an interface or DTO) might affect others.
- To determine which files need to be loaded into context for a successful fix.

## When NOT to use
- When applying trivial, isolated fixes that have no impact on other files.
- During the final stages of a migration where analysis has already been performed.

## Inputs
- Target file(s) for migration.
- Directory structure of the project.
- Search queries for usage of specific classes or methods.

## Outputs
- List of "Impacted Files" (files that call or are called by the target).
- Dependency map of the target component.
- Recommended context list (which files the agent should load).

## Strict Constraints
- **Token Optimization**: Only suggest loading *relevant* files. Avoid large, unrelated directories.
- **Accuracy**: Base the analysis on actual code references (imports, method calls).
- **No Modifications**: This skill only *analyzes*; it never modifies files.

## Execution Workflow
1. **Identify Target**: Start with the file(s) designated for migration.
2. **Scan Imports**: Identify what the target depends on.
3. **Find Usages**: Identify what depends on the target (using grep or IDE-like search).
4. **Map Chain**: Determine the depth of the dependency chain (usually 1-2 levels for migration).
5. **Report**: Output the recommended context and potential risks. 

### Response Format
Output must be structured clearly, detailing:
- Target File(s)
- Impacted Files
- Dependency Map
- Recommended Context List

## Decision Tree: Context Selection
1. Is the target file a DTO or Shared Utility?
    - Yes: Perform a wider search for usages, as changes here have high ripple effects.
2. Is the target file a Service or Controller?
    - Yes: Focus on the interfaces it implements and the repositories it calls.
3. Does the change involve an API signature update?
    - Yes: Load all files that call the modified methods.
    - No: Load only the target file and its immediate interface.
