from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import asyncio
from dexa.core import scanner, recon, report
import shutil
from dexa.utils.logger import log
import os

app = FastAPI(title="Dexa API", version="1.0")

class ScanRequest(BaseModel):
    target: str
    timeout: int = 60   # seconds

class ReconRequest(BaseModel):
    domain: str
    timeout: int = 30

@app.get("/")
async def root():
    return {"service": "Dexa API", "status": "ok"}

@app.post("/api/scan")
async def api_scan(req: ScanRequest):
    target = req.target
    timeout = req.timeout
    log(f"API: scan requested for {target} with timeout {timeout}s")

    # Run blocking nmap in thread to avoid blocking the event loop
    try:
        out = await asyncio.to_thread(scanner.run_scan, target)
        if out is None:
            raise HTTPException(status_code=500, detail="Scan failed or returned no output.")
        # Save report and return path
        path = await asyncio.to_thread(report.save_report, out, target)
        return {"target": target, "report": path, "output_preview": out[:800]}
    except asyncio.CancelledError:
        raise HTTPException(status_code=500, detail="Scan cancelled")
    except Exception as e:
        log(f"API scan error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/recon")
async def api_recon(req: ReconRequest):
    domain = req.domain
    timeout = req.timeout
    log(f"API: recon requested for {domain} with timeout {timeout}s")
    try:
        out = await asyncio.to_thread(recon.passive_recon, domain)
        if out is None:
            raise HTTPException(status_code=500, detail="Recon failed or returned no output.")
        path = await asyncio.to_thread(report.save_report, out, domain)
        return {"domain": domain, "report": path, "output_preview": out[:800]}
    except Exception as e:
        log(f"API recon error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Simple endpoint to check memory / status of Dexa core CLI presence
@app.get("/api/status")
async def status():
    return {"dexa_core": True, "nmap_installed": bool(shutil.which("nmap")), "whois_installed": bool(shutil.which("whois"))}
