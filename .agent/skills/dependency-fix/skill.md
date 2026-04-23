# Dependency Fix Skill

## Name
dependency-fix

## Description
Manages and repairs `pom.xml` configurations to support Java 11. It handles version upgrades, plugin updates, and adding dependencies for modules removed from the standard JDK.

## When to use
- Updating the Java version in Maven properties.
- Adding dependencies for removed JDK modules (JAXB, JAF, etc.).
- Resolving plugin incompatibilities (e.g., updating `maven-compiler-plugin`).
- Fixing dependency conflicts arising from migration.

## When NOT to use
- Changing source code (use `java-migration` or `build-fix`).
- Upgrading dependencies to their "latest" version just for the sake of it.
- Adding new libraries that are not required for migration.

## Inputs
- `pom.xml` file(s).
- Build error logs related to dependencies or plugins.
- Current Java version and target Java version.

## Outputs
- Updated `pom.xml` with minimal necessary changes.
- Explanation of why each dependency or plugin was added/updated.

## Strict Constraints
- **Minimal Upgrades**: Only upgrade dependencies that are incompatible with Java 11.
- **Avoid Over-upgrading**: If version 1.2.3 works on Java 11, do not upgrade to 2.0.0.
- **Preserve Structure**: Keep the existing order and formatting of `pom.xml` as much as possible.
- **No Unnecessary Dependencies**: Do not add libraries that aren't solving a migration-specific issue.

## Execution Workflow
1. **Target Java Version**: Update `<maven.compiler.source>` and `<maven.compiler.target>` (or `<release>`) to 11.
2. **Scan for Missing Modules**: Check for references to removed JDK modules (JAXB, etc.) and add appropriate dependencies.
3. **Plugin Audit**: Update `maven-compiler-plugin` to version 3.11.0 or higher. Update `surefire`, `failsafe` to versions that support Java 11.
4. **Conflict Resolution**: Check for transitive dependency conflicts introduced by new versions. If `NoSuchFieldError: JCTree` appears, upgrade Lombok to >= 1.18.30 and MapStruct to >= 1.5.5.Final.
5. **Output**: Return the modified `pom.xml`.

## Decision Tree: Dependency Upgrade
1. Does the build fail due to a dependency being incompatible with Java 11?
    - Yes: Is there a minor/patch version that supports Java 11?
        - Yes: Upgrade to that version.
        - No: Is a major version upgrade required?
            - Yes: Perform upgrade and alert user about potential API changes (trigger `build-fix`).
    - No: Keep existing version.
