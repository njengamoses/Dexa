from datetime import datetime
from dexa.utils.logger import log
import os

def save_report(data, target):
    log("Generating report...")
    safe_target = str(target).replace("/", "_")
    filename = f"report_{safe_target}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(data if isinstance(data, str) else str(data))
    log(f"Report saved as {filename}")
    return os.path.abspath(filename)
