import subprocess
import os
import shutil

PROJECT_ROOT = "/Users/kushagra/IdeaProjects/spring-petclinic-rest"

def find_mvn():
    # Try the path that was in the user's original script first
    user_path = "/opt/maven/bin/mvn"
    if os.path.exists(user_path):
        return user_path

    # Then try shutil
    mvn_path = shutil.which("mvn")
    if mvn_path:
        return mvn_path

    # Then try other common locations
    common_locations = ["/usr/local/bin/mvn", "/opt/homebrew/bin/mvn", "/usr/bin/mvn"]
    for loc in common_locations:
        if os.path.exists(loc):
            return loc
    return "mvn"

def run_build():
    mvn = find_mvn()
    print(f"🏗️ Running Build using: {mvn}...")
    try:
        result = subprocess.run(
            [mvn, "clean", "compile"],
            cwd=PROJECT_ROOT, capture_output=True, text=True
        )

        # Combined output to search for errors
        combined_output = result.stdout + result.stderr

        print("\n--- MAVEN ERROR LOGS ---")
        error_found = False
        for line in combined_output.splitlines():
            if "[ERROR]" in line:
                print(line)
                error_found = True

        if not error_found:
            print("No [ERROR] lines found in output.")
            if result.returncode != 0:
                print(f"Build failed with exit code {result.returncode} but no [ERROR] tags were found.")
                print("Showing last 20 lines of output:")
                print("\n".join(combined_output.splitlines()[-20:]))
    except Exception as e:
        print(f"Failed to run subprocess: {e}")

if __name__ == "__main__":
    run_build()
