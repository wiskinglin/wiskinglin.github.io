import os
import subprocess
import sys

# Windows Absolute Path detected during installation
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

def get_soffice_env() -> dict:
    """Return the environment for running soffice."""
    return os.environ.copy()

def run_soffice(args: list[str], **kwargs) -> subprocess.CompletedProcess:
    """
    Run LibreOffice (soffice) on Windows using the absolute path.
    """
    executable = SOFFICE_PATH if os.path.exists(SOFFICE_PATH) else "soffice"
    
    # Ensure headless mode is preferred for automation
    if "--headless" not in args:
        args = ["--headless"] + args
        
    print(f"Running: {executable} {' '.join(args)}")
    return subprocess.run([executable] + args, **kwargs)

if __name__ == "__main__":
    result = run_soffice(sys.argv[1:])
    sys.exit(result.returncode)
