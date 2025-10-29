import datetime

LOGFILE = "dexa.log"

def log(msg):
    ts = datetime.datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    try:
        print(line, flush=True)
    except Exception:
        pass
    try:
        with open(LOGFILE, "a") as f:
            f.write(line + "\\n")
    except Exception:
        pass
