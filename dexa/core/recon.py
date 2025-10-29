import subprocess
from dexa.utils.logger import log

def passive_recon(domain):
    log(f"Running passive reconnaissance on {domain}")
    try:
        result = subprocess.run(
            ["whois", domain],
            capture_output=True,
            text=True,
            check=False
        )
        log("Reconnaissance completed.")
        return result.stdout
    except Exception as e:
        log(f"Error during recon: {e}")
        return None
