import re
import os

def parse_maven_errors(stdout):
    """
    Parses Maven output to find specific compilation errors.
    Returns a list of dicts: [{'file': ..., 'line': ..., 'message': ...}]
    """
    # Pattern for typical Java compiler errors:
    # [ERROR] /path/to/File.java:[line,col] error message
    error_pattern = r"\[ERROR\]\s+(.*?\.java):\[(\d+),\d+\]\s+(.*)"

    errors = []
    for line in stdout.splitlines():
        match = re.search(error_pattern, line)
        if match:
            errors.append({
                "file": match.group(1),
                "line": int(match.group(2)),
                "message": match.group(3).strip()
            })

    # Also look for POM/Dependency errors
    if "Non-resolvable parent POM" in stdout or "DependencyResolutionException" in stdout:
        errors.append({
            "file": "pom.xml",
            "line": 0,
            "message": "Dependency or Parent POM resolution error."
        })

    return errors
