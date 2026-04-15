import ast
import csv
import difflib
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Sequence, Set

from maven_parser import parse_maven_errors
from openai_client import call_ai_cafe

# --- Configuration ---
PROJECT_ROOT = "/Users/kushagra/IdeaProjects/java_8_demo_10apr"
MIGRATION_RULES_PATH = os.path.join(PROJECT_ROOT, ".gemini/v8tov11Migration.md")
MAX_FIX_ITERATIONS = 40
MAX_ERRORS_PER_ITERATION = 5
MAX_FILES_PER_FIX = 5
DEBUG_DIR = os.path.join(PROJECT_ROOT, ".agent_debug")
LOG_FILE_PATH = os.path.join(PROJECT_ROOT, "migration_changes.csv")
SKIP_PROACTIVE_SCAN = os.getenv("SKIP_PROACTIVE_SCAN", "").strip().lower() in {"1", "true", "yes"}
FORCE_PROACTIVE_SCAN = os.getenv("FORCE_PROACTIVE_SCAN", "").strip().lower() in {"1", "true", "yes"}
APPLICATION_FAILURE_KEYWORDS = (
    "illegalstate",
    "nullpointer",
    "environment",
    "not set",
    "beancreation",
    "failed to load",
    "something went wrong",
    "exception",
)


def find_maven_executable():
    """
    Locates the Maven wrapper (mvnw) if available, otherwise defaults to mvn.
    """
    wrapper_path = os.path.join(PROJECT_ROOT, "mvnw")
    return wrapper_path if os.path.exists(wrapper_path) else "mvn"


MAVEN_COMMAND = find_maven_executable()


class JavaMigrationAgent:
    """
    Migrates a Java 8 codebase to Java 11 using a proactive modernization pass
    followed by an autonomous build-fix loop.
    """

    def __init__(self, project_root):
        self.project_root = project_root
        self.current_iteration = 0
        self.migration_rules = self._load_migration_rules()
        self.error_fingerprints: Dict[str, int] = {}
        self.primary_failure_counts: Dict[str, int] = {}
        self.pre_reactive_snapshots: Dict[str, str] = {}
        os.makedirs(DEBUG_DIR, exist_ok=True)
        self._initialize_csv_log()

    def _initialize_csv_log(self):
        """Initializes the CSV file with headers if it doesn't exist."""
        headers = ["Timestamp", "Iteration", "Modified File", "Action", "Change Type", "Triggered By Error In", "Reason", "Details", "Diff"]
        file_exists = os.path.isfile(LOG_FILE_PATH)
        with open(LOG_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(headers)

    def _log_change_to_csv(self, file_path: str, action: str, change_type: str, triggered_by: str, reason: str, details: str, diff: str = ""):
        """Appends a new change record to the CSV log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rel_path = os.path.relpath(file_path, self.project_root)
        with open(LOG_FILE_PATH, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, self.current_iteration, rel_path, action, change_type, triggered_by, reason, details, diff])

    def _generate_diff(self, file_path: str, old_content: str, new_content: str) -> str:
        """Generates a unified diff between old and new content."""
        rel_path = os.path.relpath(file_path, self.project_root)
        diff_lines = difflib.unified_diff(
            old_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{rel_path}",
            tofile=f"b/{rel_path}"
        )
        return "".join(diff_lines)

    def _load_migration_rules(self):
        """Loads migration guidelines from the Markdown file."""
        try:
            with open(MIGRATION_RULES_PATH, "r", encoding="utf-8") as file_handle:
                return file_handle.read()
        except FileNotFoundError:
            print(f"Error: Migration rules file not found at {MIGRATION_RULES_PATH}")
            raise SystemExit(1)

    def _run_maven_build(self):
        """Executes mvn clean test in the project root."""
        self.current_iteration += 1
        print(f"\n--- [Iteration {self.current_iteration}] Building Project ---")
        try:
            result = subprocess.run(
                [MAVEN_COMMAND, "clean", "test"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=False,
            )
            return result.returncode == 0, result.stdout + result.stderr
        except Exception as exc:
            print(f"Build execution error: {exc}")
            raise SystemExit(1)

    def _write_debug_artifact(self, name: str, content: str):
        debug_path = os.path.join(DEBUG_DIR, name)
        with open(debug_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(content)

    def _find_file_path(self, identifier):
        """Finds a file from an absolute path, relative path, or basename, prioritizing production code."""
        if not identifier:
            return None

        if os.path.isabs(identifier) and os.path.exists(identifier):
            return identifier

        normalized_identifier = identifier.lstrip(os.sep)
        full_path_candidate = os.path.join(self.project_root, normalized_identifier)
        if os.path.exists(full_path_candidate):
            return full_path_candidate

        filename_only = os.path.basename(identifier)
        all_matches = []
        for root, dirnames, files in os.walk(self.project_root):
            dirnames[:] = [name for name in dirnames if name not in {"target", ".git", ".idea", ".agent_debug"}]
            if filename_only in files:
                full_path = os.path.join(root, filename_only)
                if os.sep in normalized_identifier and normalized_identifier.replace(".", os.sep) in full_path:
                    all_matches.append(full_path)
                elif os.sep not in normalized_identifier:
                    all_matches.append(full_path)

        if not all_matches:
            return None

        # Prioritization: prefer src/main/java over src/test/java
        production_matches = [m for m in all_matches if "src/main/java" in m]
        if production_matches:
            return production_matches[0]
        return all_matches[0]

    def _display_file_reference(self, identifier: Optional[str]) -> str:
        """Formats a file identifier as a project-relative path when possible."""
        if not identifier:
            return "unknown"

        resolved = self._find_file_path(identifier)
        if resolved:
            return os.path.relpath(resolved, self.project_root)

        return identifier.replace("\\", "/")

    def _get_all_java_source_files(self):
        """Recursively finds all .java files in src/main/java."""
        java_files = []
        source_dir = os.path.join(self.project_root, "src/main/java")
        if not os.path.exists(source_dir):
            return []
        for root, _, files in os.walk(source_dir):
            for file_name in files:
                if file_name.endswith(".java"):
                    java_files.append(os.path.join(root, file_name))
        return java_files

    def _guess_related_java_files(self, java_file_path: str) -> List[str]:
        """
        Guesses related Java files based on naming conventions with a prioritized order.
        """
        related_files = []
        seen = {java_file_path}

        file_name_without_ext = os.path.basename(java_file_path).replace(".java", "")
        base_name = file_name_without_ext

        # Remove common suffixes to get the core name
        suffixes = ["Controller", "Service", "Repository", "DTO", "Model", "Util", "Exception"]
        for suffix in suffixes:
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
                break

        # Priority list for guessing related files (Model/Entity first)
        priority_suffixes = ["", "DTO", "Repository", "Service", "Controller", "Model", "Util", "Exception"]

        for suffix in priority_suffixes:
            name = f"{base_name}{suffix}.java"
            resolved = self._find_file_path(name)
            if resolved and resolved not in seen:
                seen.add(resolved)
                related_files.append(resolved)

        return related_files

    def _extract_code_fences(self, text: str) -> List[str]:
        matches = re.findall(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
        return [match.strip() for match in matches if match.strip()]

    def _extract_balanced_candidates(self, text: str) -> List[str]:
        candidates = []
        for opener, closer in (("[", "]"), ("{", "}")):
            start = text.find(opener)
            while start != -1:
                depth = 0
                for index in range(start, len(text)):
                    char = text[index]
                    if char == opener:
                        depth += 1
                    elif char == closer:
                        depth -= 1
                        if depth == 0:
                            candidates.append(text[start:index + 1])
                            break
                start = text.find(opener, start + 1)
        candidates.sort(key=len, reverse=True)
        return candidates

    def _parse_json_candidate(self, candidate: str):
        payload = candidate.strip()
        if not payload:
            return None

        parse_attempts = [
            payload,
            re.sub(r",\s*([}\]])", r"\1", payload),
        ]
        for attempt in parse_attempts:
            try:
                parsed = json.loads(attempt)
                return [parsed] if isinstance(parsed, dict) else parsed
            except Exception:
                continue

        try:
            parsed = ast.literal_eval(payload)
            if isinstance(parsed, dict):
                return [parsed]
            if isinstance(parsed, list):
                return parsed
        except Exception:
            return None
        return None

    def _extract_json_from_ai_response(self, text):
        """Extracts JSON updates from a free-form AI response."""
        if not text:
            return None

        candidates = []
        candidates.extend(self._extract_code_fences(text))
        candidates.extend(self._extract_balanced_candidates(text))
        candidates.append(text.strip())

        for candidate in candidates:
            parsed = self._parse_json_candidate(candidate)
            if parsed:
                return parsed
        return None

    def _normalize_text(self, text: str) -> str:
        return text.replace("\r\n", "\n")

    def _apply_edits(self, current_content: str, edits: Sequence[dict]) -> str:
        modified_content = current_content
        for edit in edits:
            search_text = edit.get("search")
            replace_text = edit.get("replace")
            if not search_text or replace_text is None:
                continue

            if search_text in modified_content:
                modified_content = modified_content.replace(search_text, replace_text)
                continue

            normalized_content = self._normalize_text(modified_content)
            normalized_search = self._normalize_text(search_text)
            if normalized_search in normalized_content:
                normalized_replace = self._normalize_text(replace_text)
                normalized_content = normalized_content.replace(normalized_search, normalized_replace)
                modified_content = normalized_content
                continue

            stripped_search = search_text.strip()
            if stripped_search and stripped_search in modified_content:
                modified_content = modified_content.replace(stripped_search, replace_text)

        return modified_content

    def _snapshot_file_for_recovery(self, file_path: str, current_content: str):
        if file_path not in self.pre_reactive_snapshots:
            self.pre_reactive_snapshots[file_path] = current_content

    def _restore_recovery_snapshot(self, file_path: str) -> bool:
        snapshot = self.pre_reactive_snapshots.get(file_path)
        if snapshot is None or not os.path.exists(file_path):
            return False

        with open(file_path, "r", encoding="utf-8") as file_handle:
            current_content = file_handle.read()

        if current_content == snapshot:
            return False

        diff = self._generate_diff(file_path, current_content, snapshot)
        with open(file_path, "w", encoding="utf-8") as file_handle:
            file_handle.write(snapshot)

        rel_path = os.path.relpath(file_path, self.project_root)
        print(f"Restored file from pre-reactive snapshot: {rel_path}")
        self._log_change_to_csv(file_path, "Restore", "Recovery", "Self", "Cyclic fix detected", "Restored to pre-reactive snapshot", diff)
        return True

    def _apply_code_updates(self, updates, capture_recovery_snapshot: bool = False, change_type: str = "Unknown", triggered_by: str = "Unknown", reason: str = "Unknown", details: str = ""):
        """Applies file overwrites or edits and returns the changed file paths."""
        if not updates:
            return set()

        if isinstance(updates, dict):
            updates = [updates]

        changed_files: Set[str] = set()
        for update_item in updates:
            if not isinstance(update_item, dict):
                continue

            file_identifier = update_item.get("file")
            if not file_identifier:
                continue

            full_file_path = self._find_file_path(file_identifier)
            if not full_file_path:
                print(f"Warning: File not found: {file_identifier}")
                continue

            with open(full_file_path, "r", encoding="utf-8") as file_handle:
                current_content = file_handle.read()

            new_content = update_item.get("content")
            edits = update_item.get("edits") or []
            modified_content = current_content

            if new_content is not None:
                modified_content = new_content
            elif edits:
                modified_content = self._apply_edits(current_content, edits)

            if modified_content != current_content:
                if capture_recovery_snapshot:
                    self._snapshot_file_for_recovery(full_file_path, current_content)

                diff = self._generate_diff(full_file_path, current_content, modified_content)

                os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
                with open(full_file_path, "w", encoding="utf-8") as file_handle:
                    file_handle.write(modified_content)

                rel_path = os.path.relpath(full_file_path, self.project_root)
                action = "Overwriting" if new_content is not None else "Patching"
                print(f"{action} file: {rel_path}")
                self._log_change_to_csv(full_file_path, action, change_type, triggered_by, reason, details, diff)
                changed_files.add(full_file_path)

        return changed_files

    def _perform_proactive_modernization(self):
        """Phase 1: Applies initial Java 11 modernizations and security fixes."""
        print("\nPhase 1: Proactive Modernization Scan")

        pom_path = os.path.join(self.project_root, "pom.xml")
        if os.path.exists(pom_path):
            print("Modernizing build configuration (pom.xml)...")
            with open(pom_path, "r", encoding="utf-8") as file_handle:
                content = file_handle.read()
            prompt = (
                f"{self.migration_rules}\n\nFILE: pom.xml\n{content}\n\n"
                "Task: Update to Java 11. Return JSON: [{'file': 'pom.xml', 'content': '...'}]"
            )
            self._apply_code_updates(
                self._extract_json_from_ai_response(call_ai_cafe(prompt)),
                change_type="Proactive Modernization",
                triggered_by="pom.xml",
                reason="Update to Java 11",
                details="Updating build properties and compiler settings"
            )

        for file_path in self._get_all_java_source_files():
            rel_path = os.path.relpath(file_path, self.project_root)
            print(f"Modernizing {rel_path}...")
            with open(file_path, "r", encoding="utf-8") as file_handle:
                content = file_handle.read()
            prompt = (
                f"{self.migration_rules}\n\nFILE: {rel_path}\n{content}\n\n"
                "Task: Migrate this file to Java 11 and apply security fixes for ALL occurrences. "
                "Return JSON edits."
            )
            self._apply_code_updates(
                self._extract_json_from_ai_response(call_ai_cafe(prompt)),
                change_type="Proactive Modernization",
                triggered_by=rel_path,
                reason="Java 11 + Security Fixes",
                details=f"Modernizing {rel_path}"
            )

    def _project_appears_already_migrated(self) -> bool:
        pom_path = os.path.join(self.project_root, "pom.xml")
        if not os.path.exists(pom_path):
            return False

        try:
            with open(pom_path, "r", encoding="utf-8") as file_handle:
                pom_content = file_handle.read()
        except OSError:
            return False

        normalized = pom_content.replace(" ", "").replace("\n", "").lower()
        return (
            "<java.version>11</java.version>" in normalized
            or "<maven.compiler.source>11</maven.compiler.source>" in normalized
            or "<release>11</release>" in normalized
        )

    def _format_error_summary(self, errors: Sequence[dict]) -> str:
        lines = []
        for error in errors[:MAX_ERRORS_PER_ITERATION]:
            file_name = error.get("file", "unknown")
            line_num = error.get("line", 0)
            column_num = error.get("column", 0)
            message = error.get("message", "")
            lines.append(f"- [{error.get('type', 'ERROR')}] {file_name}:{line_num}:{column_num} {message}")
        return "\n".join(lines)

    def _build_error_fingerprint(self, errors: Sequence[dict]) -> str:
        parts = [f"{error.get('type')}|{error.get('file')}|{error.get('message')}" for error in errors[:MAX_ERRORS_PER_ITERATION]]
        digest_input = "\n".join(parts)
        return hashlib.sha256(digest_input.encode("utf-8")).hexdigest()

    def _get_related_files(self, primary_file: str, errors: Sequence[dict]) -> List[str]:
        target_files = []
        seen = set()

        def add_candidate(file_path: Optional[str]):
            if file_path:
                resolved_path = self._find_file_path(file_path)
                if resolved_path and resolved_path not in seen:
                    seen.add(resolved_path)
                    target_files.append(resolved_path)

        # 1. ALWAYS add the primary file first
        add_candidate(primary_file)

        # 2. Add inferred files based on PRIORITY naming conventions
        if primary_file and primary_file.endswith(".java"):
            for guessed in self._guess_related_java_files(primary_file):
                add_candidate(guessed)

        # 3. Add files explicitly mentioned in other errors in this batch
        for error in errors:
            add_candidate(error.get("file"))

        return target_files[:MAX_FILES_PER_FIX]

    def _guess_production_files_for_test(self, test_file_identifier: Optional[str]) -> List[str]:
        if not test_file_identifier:
            return []

        test_name = os.path.basename(test_file_identifier)
        if not test_name.endswith("Test.java"):
            return []

        base_name = test_name.replace("Test.java", ".java")
        candidates: List[str] = []
        seen: Set[str] = set()

        def add_candidate(file_identifier: str):
            resolved = self._find_file_path(file_identifier)
            if resolved and resolved not in seen:
                seen.add(resolved)
                candidates.append(resolved)

        add_candidate(base_name)

        if base_name.endswith("Controller.java"):
            service_candidate = base_name.replace("Controller.java", "Service.java")
            add_candidate(service_candidate)
        elif base_name.endswith("Service.java"):
            repository_candidate = base_name.replace("Service.java", "Repository.java")
            add_candidate(repository_candidate)

        return candidates

    def _is_test_source(self, file_identifier: Optional[str]) -> bool:
        if not file_identifier:
            return False
        normalized = file_identifier.replace("\\", "/")
        return normalized.endswith("Test.java") or "/src/test/java/" in normalized or normalized.startswith("src/test/java/")

    def _is_application_side_test_failure(self, errors: Sequence[dict]) -> bool:
        for error in errors:
            if error.get("type") != "TEST_FAILURE":
                continue
            message = (error.get("message") or "").lower()
            if any(keyword in message for keyword in APPLICATION_FAILURE_KEYWORDS):
                return True
        return False

    def _compose_file_context(self, file_paths: Iterable[str]) -> str:
        context_chunks = []
        for file_path in file_paths:
            with open(file_path, "r", encoding="utf-8") as file_handle:
                content = file_handle.read()
            rel_path = os.path.relpath(file_path, self.project_root)
            context_chunks.append(f"FILE CONTENT ({rel_path}):\n```java\n{content}\n```")
        return "\n\n".join(context_chunks)

    def _build_fix_prompt(self, errors: Sequence[dict], build_logs: str, target_files: Sequence[str], repeated_error: bool) -> str:
        error_summary = self._format_error_summary(errors)
        file_context = self._compose_file_context(target_files)
        repeated_instruction = ""
        if repeated_error:
            repeated_instruction = (
                "\nThe last attempt did not change the build outcome. "
                "Do not return search/replace edits. Rewrite the full contents of every impacted file."
            )

        test_failure_instruction = ""
        if any(error.get("type") == "TEST_FAILURE" for error in errors):
            test_failure_instruction = (
                "\nTEST FAILURE RULES:\n"
                "1. Prefer fixing production code or test setup when the failure is caused by runtime/configuration behavior.\n"
                "2. Do not rewrite tests repeatedly if the same runtime exception is still present.\n"
                "3. Only change test expectations when the application behavior intentionally changed and is now correct.\n"
            )
        elif any(self._is_test_source(error.get("file")) for error in errors):
            test_failure_instruction = (
                "\nTEST COMPILE FAILURE RULES:\n"
                "1. Prefer fixing production classes, imports, or Spring test configuration over rewriting the test body.\n"
                "2. Do not invent new application entrypoints or package names.\n"
                "3. Only update the test when the failure is a direct import, annotation, or assertion mismatch visible in the provided context.\n"
            )

        return (
            f"{self.migration_rules}\n"
            "You are in the reactive build-fix phase of an autonomous migration agent.\n"
            "Fix the current build failures in one response.\n"
            f"{repeated_instruction}\n"
            "\nBUILD ERRORS:\n"
            f"{error_summary}\n"
            "\nRECENT BUILD LOG TAIL:\n"
            f"```text\n{build_logs[-4000:]}\n```\n"
            "\nRESPONSE RULES:\n"
            "1. Return ONLY a JSON array.\n"
            "2. Each item must contain 'file' and full replacement 'content'.\n"
            "3. Do not return search/replace edits for reactive fixes.\n"
            "4. If multiple files are required, include all of them in the same array.\n"
            "5. Preserve package names and imports unless the fix requires changing them.\n"
            "6. Do not invent fields, methods, constructors, or classes that are not present in the provided context.\n"
            "7. If a controller/service uses a DTO or model incorrectly, update the DTO/model/service in the same response instead of referencing nonexistent APIs.\n"
            f"{test_failure_instruction}"
            "\nTARGET FILES:\n"
            f"{file_context}\n"
        )

    def _request_fix_updates(self, errors: Sequence[dict], build_logs: str, target_files: Sequence[str], repeated_error: bool):
        prompt = self._build_fix_prompt(errors, build_logs, target_files, repeated_error)
        target_name = ", ".join(os.path.basename(path) for path in target_files)
        print(f"Requesting specialized AI fix for {target_name}...")
        ai_response = call_ai_cafe(prompt)

        iteration_label = f"iter_{self.current_iteration:02d}"
        self._write_debug_artifact(f"{iteration_label}_response.txt", ai_response)

        proposed_updates = self._extract_json_from_ai_response(ai_response)
        if proposed_updates is None:
            self._write_debug_artifact(f"{iteration_label}_unparsed_response.txt", ai_response)
            print("Warning: AI response did not contain parseable JSON updates.")
        return proposed_updates

    def _fallback_full_file_retry(self, errors: Sequence[dict], build_logs: str, target_files: Sequence[str]):
        retry_prompt = self._build_fix_prompt(errors, build_logs, target_files, repeated_error=True)
        retry_prompt += (
            "\nReturn the exact corrected file bodies for the files above. "
            "If one file is malformed, rewrite the entire file from scratch."
        )
        print("Retrying with strict full-file rewrite prompt...")
        ai_response = call_ai_cafe(retry_prompt)
        iteration_label = f"iter_{self.current_iteration:02d}_retry"
        self._write_debug_artifact(f"{iteration_label}_response.txt", ai_response)
        return self._extract_json_from_ai_response(ai_response)

    def _select_fix_batch(self, errors: Sequence[dict], build_logs: str):
        if not errors:
            fallback_file = os.path.join(self.project_root, "pom.xml")
            fallback_error = {
                "type": "GENERAL_FAILURE",
                "file": "pom.xml",
                "line": 0,
                "column": 0,
                "message": "General build failure. Inspect recent build logs.",
            }
            return [fallback_error], [fallback_file]

        selected_errors = list(errors[:MAX_ERRORS_PER_ITERATION])
        primary_identifier = selected_errors[0].get("file")
        primary_file = self._find_file_path(primary_identifier) if primary_identifier else None

        if not primary_file and primary_identifier:
            basename_match = self._find_file_path(os.path.basename(primary_identifier))
            primary_file = basename_match

        target_files: List[str] = []

        if any(error.get("type") == "TEST_FAILURE" for error in selected_errors):
            seen: Set[str] = set()

            def add_target(candidate: Optional[str]):
                if candidate and candidate not in seen:
                    seen.add(candidate)
                    target_files.append(candidate)

            app_side_failure = self._is_application_side_test_failure(selected_errors)
            for error in selected_errors:
                if error.get("type") != "TEST_FAILURE":
                    continue
                production_files = self._guess_production_files_for_test(error.get("file"))
                if app_side_failure:
                    for production_file in production_files:
                        add_target(production_file)
                resolved_test = self._find_file_path(error.get("file"))
                if not app_side_failure and resolved_test:
                    add_target(resolved_test)
                elif resolved_test:
                    add_target(resolved_test)
                if len(target_files) >= MAX_FILES_PER_FIX:
                    break

            if primary_file:
                add_target(primary_file)
        elif any(self._is_test_source(error.get("file")) for error in selected_errors):
            seen: Set[str] = set()

            def add_target(candidate: Optional[str]):
                if candidate and candidate not in seen:
                    seen.add(candidate)
                    target_files.append(candidate)

            for error in selected_errors:
                test_file = self._find_file_path(error.get("file"))
                production_files = self._guess_production_files_for_test(error.get("file"))
                for production_file in production_files:
                    add_target(production_file)
                if test_file and not production_files:
                    add_target(test_file)
                if len(target_files) >= MAX_FILES_PER_FIX:
                    break

            if primary_file and not target_files:
                add_target(primary_file)
        else:
            # Use the enhanced _get_related_files for non-test failures
            target_files = self._get_related_files(primary_file or primary_identifier, selected_errors)

        if not target_files and primary_file:
            target_files = [primary_file]
        if not target_files:
            target_files = [os.path.join(self.project_root, "pom.xml")]

        return selected_errors, target_files

    def start_migration(self):
        """Initiates the migration process and enters the reactive build-fix loop."""
        print("Starting Automated Java Migration Agent...")

        if SKIP_PROACTIVE_SCAN:
            print("\nPhase 1: Proactive Modernization Scan")
            print("Skipping proactive scan because SKIP_PROACTIVE_SCAN is enabled.")
        elif self._project_appears_already_migrated() and not FORCE_PROACTIVE_SCAN:
            print("\nPhase 1: Proactive Modernization Scan")
            print("Skipping proactive scan because the project already appears to target Java 11. Set FORCE_PROACTIVE_SCAN=1 to override.")
        else:
            self._perform_proactive_modernization()

        print("\nPhase 2: Reactive Build-Fix Loop")
        while self.current_iteration < MAX_FIX_ITERATIONS:
            is_build_successful, build_logs = self._run_maven_build()
            self._write_debug_artifact(f"iter_{self.current_iteration:02d}_build.log", build_logs)

            if is_build_successful:
                print("\nSUCCESS: Project successfully migrated and built.")
                break

            errors = parse_maven_errors(build_logs)
            selected_errors, target_files = self._select_fix_batch(errors, build_logs)
            fingerprint = self._build_error_fingerprint(selected_errors)
            self.error_fingerprints[fingerprint] = self.error_fingerprints.get(fingerprint, 0) + 1
            repeated_error = self.error_fingerprints[fingerprint] > 1

            primary_file = target_files[0]
            primary_failure_key = f"{primary_file}|{fingerprint}"
            self.primary_failure_counts[primary_failure_key] = self.primary_failure_counts.get(primary_failure_key, 0) + 1

            error_type = selected_errors[0]['type']
            error_msg = selected_errors[0]['message']
            triggered_by_path = self._display_file_reference(selected_errors[0].get("file"))
            target_rel_paths = [os.path.relpath(path, self.project_root) for path in target_files]

            print(f"Error Detected: {error_type} in {triggered_by_path}")
            print("Fix batch:")
            print(self._format_error_summary(selected_errors))
            print(f"Planned fix targets: {', '.join(target_rel_paths)}")

            if self.primary_failure_counts[primary_failure_key] >= 3:
                restored = self._restore_recovery_snapshot(primary_file)
                if restored:
                    print(
                        "Detected repeated non-progressing fixes for the same primary file. "
                        "Restored the last pre-reactive version before trying again."
                    )
                    continue

            proposed_updates = self._request_fix_updates(selected_errors, build_logs, target_files, repeated_error)
            changed_files = self._apply_code_updates(
                proposed_updates,
                capture_recovery_snapshot=True,
                change_type="Reactive Build Fix",
                triggered_by=triggered_by_path,
                reason=f"Fixing {error_type}",
                details=error_msg
            )

            if not changed_files:
                retry_updates = self._fallback_full_file_retry(selected_errors, build_logs, target_files)
                changed_files = self._apply_code_updates(
                    retry_updates,
                    capture_recovery_snapshot=True,
                    change_type="Retry Fallback",
                    triggered_by=triggered_by_path,
                    reason=f"Strict fix for {error_type}",
                    details="AI failed to provide valid JSON or no changes were detected initially."
                )

            if not changed_files:
                print(f"Warning: No changes applied for current error batch affecting {triggered_by_path}.")
                continue

            changed_rel_paths = [os.path.relpath(path, self.project_root) for path in sorted(changed_files)]
            print(f"Applied changes to: {', '.join(changed_rel_paths)}")
        else:
            print(f"\nWarning: Migration did not complete within {MAX_FIX_ITERATIONS} iterations. Manual intervention may be required.")


if __name__ == "__main__":
    agent = JavaMigrationAgent(PROJECT_ROOT)
    agent.start_migration()
