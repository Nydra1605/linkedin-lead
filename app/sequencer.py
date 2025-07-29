"""APScheduler‑backed outreach scheduler."""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, time as dtime
from typing import Callable
from app.observability import logger

scheduler = BackgroundScheduler()

class OutreachScheduler:
    """Utility exposed as a Tool to schedule message sending."""
    def schedule(self, when: datetime, fn: Callable, *args, **kwargs):
        job = scheduler.add_job(fn, 'date', run_date=when, args=args, kwargs=kwargs)
        logger.info(f"[Scheduler] Job {job.id} scheduled @ {when.isoformat()}")
        return job.id

# start scheduler once
scheduler.start()