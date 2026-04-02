import os
import subprocess
import json
import re
import shutil
from openai_client import call_ai_cafe
from maven_parser import parse_maven_errors

# --- CONFIGURATION ---
PROJECT_ROOT = "/Users/kushagra/IdeaProjects/java_8_demo"
MD_PATH = os.path.join(PROJECT_ROOT, ".gemini/v8tov11Migration.md")
MAX_ITERATIONS = 20

def find_mvn():
    wrapper = os.path.join(PROJECT_ROOT, "mvnw")
    return wrapper if os.path.exists(wrapper) else "mvn"

MVN_COMMAND = find_mvn()

class MigrationAgent:
    def __init__(self, project_root):
        self.root = project_root
        self.iteration = 0
        self.instructions = self._read_instructions()

    def _read_instructions(self):
        with open(MD_PATH, "r") as f:
            return f.read()

    def run_build(self):
        print(f"\n--- [Iteration {self.iteration}] 🏗️ Building Project ---")
        result = subprocess.run(
            [MVN_COMMAND, "clean", "compile"],
            cwd=self.root, capture_output=True, text=True
        )
        return result.returncode == 0, result.stdout + result.stderr

    def get_all_java_files(self):
        java_files = []
        for root, dirs, files in os.walk(os.path.join(self.root, "src/main/java")):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
        return java_files

    def extract_json(self, text):
        """Robustly extracts JSON from AI response, even if malformed or surrounded by text."""
        try:
            # Look for the last json block (often the most complete one)
            matches = re.findall(r'```json\s*(.*?)\s*```', text, re.DOTALL)
            if matches:
                # Clean up common JSON errors from AI (like trailing commas)
                clean_json = re.sub(r',\s*([}\]])', r'\1', matches[-1].strip())
                return json.loads(clean_json)

            # Fallback: try to find anything between [ and ]
            match = re.search(r'\[\s*{.*}\s*\]', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))

            # Fallback for when AI returns a single object instead of a list
            match_obj = re.search(r'{\s*".*}\s*', text, re.DOTALL)
            if match_obj:
                obj = json.loads(match_obj.group(0))
                return [obj] if isinstance(obj, dict) else obj

        except Exception as e:
            print(f"   ⚠️ JSON extraction failed: {e}")
        return None

    def apply_updates(self, updates):
        if not updates: return False

        # Ensure updates is a list
        if isinstance(updates, dict):
            updates = [updates]

        applied = False
        for up in updates:
            if not isinstance(up, dict):
                print(f"   ⚠️ Skipping invalid update item: {up}")
                continue

            file_path = up.get('file')
            if not file_path: continue

            # Handle relative pathing
            if os.path.isabs(file_path):
                full_path = file_path
            else:
                full_path = os.path.join(self.root, file_path.lstrip("/"))

            content = up.get('content')
            edits = up.get('edits', [])

            if content:
                print(f"💾 OVERWRITING: {file_path}")
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)
                applied = True
            elif edits:
                if not os.path.exists(full_path): continue
                with open(full_path, "r") as f:
                    text = f.read()
                orig = text
                for edit in edits:
                    s, r = edit.get('search'), edit.get('replace')
                    if s and s in text:
                        text = text.replace(s, r)
                        print(f"💾 PATCHING: {file_path}")
                        applied = True
                if text != orig:
                    with open(full_path, "w") as f:
                        f.write(text)
        return applied

    def scan_and_improve(self):
        print("\n🔍 Phase 1: Identifying and applying Java 11 improvements...")

        # 1. First, check pom.xml to update Java version to 11
        pom_path = os.path.join(self.root, "pom.xml")
        if os.path.exists(pom_path):
            print("📦 Checking pom.xml for Java version update...")
            with open(pom_path, "r") as f:
                content = f.read()

            prompt = f"{self.instructions}\n\nFILE: pom.xml\n{content}\n\nTask: Update Java version from 1.8 to 11 and any other relevant dependencies. Return the full content in JSON format like this: [{{'file': 'pom.xml', 'content': '...'}}]"
            response = call_ai_cafe(prompt)
            updates = self.extract_json(response)
            if updates:
                self.apply_updates(updates)

        # 2. Scan all Java files
        java_files = self.get_all_java_files()
        for file_path in java_files:
            rel_path = os.path.relpath(file_path, self.root)
            print(f"👀 Scanning {rel_path} for modernizations...")
            with open(file_path, "r") as f:
                content = f.read()

            prompt = f"{self.instructions}\n\nFILE: {rel_path}\n{content}\n\nTask: Migrate this file to use Java 11 features (var, HttpClient, List.of, etc.) where appropriate. Return JSON edits like this: [{{'file': '{rel_path}', 'edits': [{{'search': '...', 'replace': '...'}}]}}]"
            response = call_ai_cafe(prompt)
            updates = self.extract_json(response)
            if updates:
                self.apply_updates(updates)

    def execute(self):
        print("🤖 Starting Autonomous Migration Agent...")

        # Step 1: Proactive Scan and Migration
        self.scan_and_improve()

        # Step 2: Reactive Fix Loop
        print("\n🔧 Phase 2: Reactive Build-Fix Loop...")
        while self.iteration < MAX_ITERATIONS:
            self.iteration += 1
            success, log = self.run_build()

            if success:
                print("\n✅ SUCCESS: Migration complete! Project built successfully.")
                break

            errors = parse_maven_errors(log)
            # Focus on the FIRST error only to ensure precision
            if errors:
                err = errors[0]
                target = os.path.relpath(err['file'], self.root) if os.path.isabs(err['file']) else err['file']
                msg = f"{err['message']} (Line {err['line']})"
            else:
                target = "pom.xml"
                msg = log[-1000:] # Last part of the log

            print(f"\n📍 CURRENT ERROR: {msg} in {target}")

            # Send file content and error to AI
            full_target_path = os.path.join(self.root, target)
            if not os.path.exists(full_target_path):
                print(f"❌ Error: File not found {full_target_path}")
                break

            with open(full_target_path, "r") as f:
                content = f.read()

            prompt = f"""
{self.instructions}

### ERROR:
{msg}

### FILE CONTENT ({target}):
{content}

### TASK:
Fix the error above for Java 11.
If it is pom.xml, you can return the full "content" or "edits".
If it is a Java file, prefer "edits" (search/replace).
Respond ONLY with JSON.
```json
[ {{ "file": "{target}", "edits": [ {{"search": "...", "replace": "..."}} ] }} ]
```
"""
            print("🧠 AI is analyzing fix...")
            response = call_ai_cafe(prompt)
            updates = self.extract_json(response)

            if not self.apply_updates(updates):
                print("❌ Failed to apply AI fix. Check the logs.")
                # We stop if we can't apply a fix to prevent infinite loops
                break

if __name__ == "__main__":
    MigrationAgent(PROJECT_ROOT).execute()
