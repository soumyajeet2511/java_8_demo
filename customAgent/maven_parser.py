import os
import re


JAVA_ERROR_REGEX = re.compile(r"\[ERROR\]\s+(.*?\.java):\[(\d+),(\d+)\]\s+(.*)")
TEST_FAILURE_REGEX = re.compile(r"\[ERROR\]\s+([A-Za-z0-9_$.]+Test)\.([A-Za-z0-9_]+):(\d+)\s+(.*)")
SUREFIRE_REPORT_REGEX = re.compile(r"\[ERROR\]\s+([A-Za-z0-9_$.]+Test)")
POM_ERROR_REGEX = re.compile(r"\[ERROR\]\s+.*?pom\.xml(?:,\s*line\s*(\d+))?.*")


def _categorize_java_error(message):
    lowered = message.lower()
    if "constructor" in lowered and "cannot be applied" in lowered:
        return "CONSTRUCTOR_MISMATCH"
    if "cannot find symbol" in lowered:
        return "MISSING_SYMBOL"
    if "is already defined" in lowered:
        return "DUPLICATE_SYMBOL"
    if "expected" in lowered or "';' expected" in lowered or "reached end of file while parsing" in lowered:
        return "SYNTAX_ERROR"
    return "COMPILATION_ERROR"


def _normalize_file_reference(file_path):
    if not file_path:
        return None
    if file_path.endswith(".java"):
        return file_path
    return os.path.basename(file_path)


def parse_maven_errors(build_output):
    """
    Parses Maven output to identify compilation errors, test failures, and POM issues.
    Returns the errors in the order they appear so the agent can batch related fixes.
    """
    errors = []
    seen = set()
    lines = build_output.splitlines()

    for line in lines:
        compile_match = JAVA_ERROR_REGEX.search(line)
        if compile_match:
            file_path = compile_match.group(1)
            line_num = int(compile_match.group(2))
            column_num = int(compile_match.group(3))
            message = compile_match.group(4).strip()
            error = {
                "type": _categorize_java_error(message),
                "file": _normalize_file_reference(file_path),
                "line": line_num,
                "column": column_num,
                "message": message,
                "raw": line.strip(),
            }
            signature = (error["type"], error["file"], error["line"], error["message"])
            if signature not in seen:
                errors.append(error)
                seen.add(signature)
            continue

        test_match = TEST_FAILURE_REGEX.search(line)
        if test_match:
            class_name = test_match.group(1)
            error = {
                "type": "TEST_FAILURE",
                "class": class_name,
                "method": test_match.group(2),
                "line": int(test_match.group(3)),
                "message": test_match.group(4).strip(),
                "file": f"{class_name.split('.')[-1]}.java",
                "raw": line.strip(),
            }
            signature = (error["type"], error["file"], error["line"], error["message"])
            if signature not in seen:
                errors.append(error)
                seen.add(signature)
            continue

        pom_match = POM_ERROR_REGEX.search(line)
        if pom_match:
            error = {
                "type": "BUILD_PLUGIN_ERROR",
                "file": "pom.xml",
                "line": int(pom_match.group(1) or 0),
                "column": 0,
                "message": line.strip(),
                "raw": line.strip(),
            }
            signature = (error["type"], error["file"], error["line"], error["message"])
            if signature not in seen:
                errors.append(error)
                seen.add(signature)

    if not errors:
        for line in lines:
            report_match = SUREFIRE_REPORT_REGEX.search(line)
            if report_match:
                class_name = report_match.group(1)
                error = {
                    "type": "TEST_FAILURE",
                    "class": class_name,
                    "method": "unknown",
                    "line": 0,
                    "column": 0,
                    "message": "Surefire reported a failing test.",
                    "file": f"{class_name.split('.')[-1]}.java",
                    "raw": line.strip(),
                }
                errors.append(error)
                break

    if not errors and "Failed to execute goal" in build_output:
        errors.append({
            "type": "BUILD_PLUGIN_ERROR",
            "file": "pom.xml",
            "line": 0,
            "column": 0,
            "message": "Maven plugin or dependency error.",
            "raw": "Failed to execute goal",
        })

    return errors
