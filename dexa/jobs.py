import uuid
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dexa.core import scanner, recon, report
from dexa.utils.logger import log

# Thread pool for running scans without blocking
executor = ThreadPoolExecutor(max_workers=5)

# In-memory job store
jobs = {}

class JobStatus:
    QUEUED = "queued"
    RUNNING = "running"
    DONE = "done"
    ERROR = "error"

def create_job(task_type, target):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"id": job_id, "type": task_type, "target": target, "status": JobStatus.QUEUED, "result": None}
    log(f"Job {job_id} created for {task_type} on {target}")
    return job_id

def get_job(job_id):
    return jobs.get(job_id)

async def run_scan_job(job_id):
    job = jobs[job_id]
    job["status"] = JobStatus.RUNNING
    target = job["target"]
    try:
        out = await asyncio.to_thread(scanner.run_scan, target)
        path = await asyncio.to_thread(report.save_report, out, target)
        job["status"] = JobStatus.DONE
        job["result"] = {"report": path, "output_preview": out[:800]}
    except Exception as e:
        job["status"] = JobStatus.ERROR
        job["result"] = {"error": str(e)}
        log(f"Job {job_id} failed: {e}")

async def run_recon_job(job_id):
    job = jobs[job_id]
    job["status"] = JobStatus.RUNNING
    domain = job["target"]
    try:
        out = await asyncio.to_thread(recon.passive_recon, domain)
        path = await asyncio.to_thread(report.save_report, out, domain)
        job["status"] = JobStatus.DONE
        job["result"] = {"report": path, "output_preview": out[:800]}
    except Exception as e:
        job["status"] = JobStatus.ERROR
        job["result"] = {"error": str(e)}
        log(f"Job {job_id} failed: {e}")
