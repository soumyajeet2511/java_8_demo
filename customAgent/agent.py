import os
import subprocess
import json
import re
from gemini_client import call_gemini

PROJECT_ROOT = "/Users/kushagra/IdeaProjects/spring-petclinic-rest"
MD_PATH = os.path.join(PROJECT_ROOT, ".gemini/v8tov11Migration.md")

def read_md():
    with open(MD_PATH, "r") as f:
        return f.read()

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def run_build():
    print("🏗️ Running Maven Build...")
    # Using 'mvn -version' first to check environment
    subprocess.run(["mvn", "-version"], cwd=PROJECT_ROOT)

    result = subprocess.run(
        ["mvn", "clean", "compile"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stdout + result.stderr

def parse_ai_response(response_text):
    """Parses JSON blocks from AI response for auto-applying changes."""
    json_pattern = r'```json\n(.*?)\n```'
    matches = re.findall(json_pattern, response_text, re.DOTALL)

    updates = []
    for match in matches:
        try:
            updates.append(json.loads(match.strip()))
        except Exception as e:
            print(f"Error parsing JSON block: {e}")
    return updates

def main():
    print("🚀 Starting Migration Agent...")

    instructions = read_md()
    pom_path = os.path.join(PROJECT_ROOT, "pom.xml")
    pom_content = read_file(pom_path)

    # We send the instructions + the current pom.xml
    prompt = f"""
{instructions}

### CURRENT POM.XML
{pom_content}

### TASK
Respond ONLY with a JSON list of file updates to migrate this project from Java 8 to Java 11.
If the project is already using Spring Boot 3+ or Java 17+, please note that and suggest a downgrade to Java 11 if possible, or explain why it is already modernized.

Format:
```json
[
  {{
    "file": "pom.xml",
    "content": "FULL NEW POM CONTENT"
  }}
]
```
"""

    response = call_gemini(prompt)
    print(f"\n🤖 AI RAW RESPONSE:\n{response[:1000]}")

    updates = parse_ai_response(response)

    if updates:
        for update in updates:
            full_path = os.path.join(PROJECT_ROOT, update['file'])
            print(f"📝 Applying change to {full_path}...")
            write_file(full_path, update['content'])

        success, output = run_build()
        if success:
            print("✅ Build Successful!")
        else:
            print("❌ Build Failed. See end of output for errors.")
            print(output[-1000:])
    else:
        print("❌ No valid updates suggested by AI. Check the API response above.")

if __name__ == "__main__":
    main()
