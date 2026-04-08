import sys
import shutil
import subprocess
import os

# ==========================================
# Terminal Colors and Formatting
# ==========================================
BOLD = '\033[1m'
NC = '\033[0m' # No Color
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'

# ==========================================
# Helper Functions
# ==========================================
def log(msg): print(msg)
def pass_check(msg): print(f"{GREEN}✔ {msg}{NC}")
def fail_check(msg): print(f"{RED}✖ {msg}{NC}")
def hint(msg): print(f"{YELLOW}💡 Hint: {msg}{NC}")
def stop_at(step):
    print(f"\n{RED}{BOLD}Validation stopped at {step}. Please fix the errors above.{NC}")
    sys.exit(1)

# ==========================================
# Configuration Variables
# ==========================================
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DOCKER_BUILD_TIMEOUT = 300 # 5 minutes in seconds

def main():
    print(f"{BLUE}{BOLD}Starting Pre-Submission Validation...{NC}\n")

    # ==========================================
    # Step 1: Pre-flight checks
    # ==========================================
    log(f"{BOLD}Step 1/3: Checking requirements{NC} ...")
    
    if shutil.which("docker") is None:
        fail_check("Docker is not installed or not in PATH.")
        stop_at("Step 1")
    else:
        pass_check("Docker is available.")

    # ==========================================
    # Step 2: Docker Build
    # ==========================================
    log(f"\n{BOLD}Step 2/3: Building Docker environment{NC} ...")
    
    try:
        # Run docker build with a timeout
        result = subprocess.run(
            ["docker", "build", "-t", "submission-env", REPO_DIR],
            capture_output=True,
            text=True,
            timeout=DOCKER_BUILD_TIMEOUT
        )
        if result.returncode == 0:
            pass_check("Docker build succeeded")
        else:
            fail_check(f"Docker build failed with exit code {result.returncode}")
            # Print the last 20 lines of the error
            lines = result.stderr.strip().split('\n')
            print('\n'.join(lines[-20:]))
            stop_at("Step 2")
            
    except subprocess.TimeoutExpired as e:
        fail_check(f"Docker build failed (timeout={DOCKER_BUILD_TIMEOUT}s)")
        if e.stderr:
            print(e.stderr.decode('utf-8'))
        stop_at("Step 2")

    # ==========================================
    # Step 3: Run openenv validate
    # ==========================================
    log(f"\n{BOLD}Step 3/3: Running openenv validate{NC} ...")

    if shutil.which("openenv") is None:
        fail_check("openenv command not found")
        hint("Install it: pip install openenv-core")
        stop_at("Step 3")

    result = subprocess.run(
        ["openenv", "validate"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        pass_check("openenv validate passed")
        if result.stdout:
            log(f"  {result.stdout.strip()}")
    else:
        fail_check("openenv validate failed")
        print(result.stderr or result.stdout)
        stop_at("Step 3")

    print("\n" + "="*40)
    print(f"{GREEN}{BOLD}  All 3/3 checks passed!{NC}")
    print(f"{GREEN}{BOLD}  Your submission is ready to submit.{NC}")
    print("="*40 + "\n")
    sys.exit(0)

if __name__ == "__main__":
    main()