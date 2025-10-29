import subprocess
from dexa.utils.logger import log

def run_scan(target):
    log(f"Starting scan on {target}")
    try:
        result = subprocess.run(
            ["nmap", "-sV", target],
            capture_output=True,
            text=True,
            check=False
        )
        log("Scan completed successfully.")
        return result.stdout
    except Exception as e:
        log(f"Error during scan: {e}")
        return None
