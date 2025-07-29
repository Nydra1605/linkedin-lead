"""Feature Enrichment Tool – calls Clearbit + Crunchbase etc."""
from crewai_tools import Tool
import httpx, os
from app.observability import logger

CLEARBIT_TOKEN = os.getenv("CLEARBIT_API_KEY", "")

class EnrichmentTool(Tool):
    name = "enrich_prospect"
    description = "Append extra company & email data using Clearbit API. Input: email or domain."

    def _run(self, email_or_domain: str, **kwargs):
        if not CLEARBIT_TOKEN:
            raise RuntimeError("CLEARBIT_API_KEY missing")
        headers = {"Authorization": f"Bearer {CLEARBIT_TOKEN}"}
        r = httpx.get(f"https://person.clearbit.com/v2/combined/find?email={email_or_domain}", headers=headers, timeout=30)
        logger.info(f"[Enrichment] Clearbit lookup → {email_or_domain}")
        if r.status_code == 404:
            return {}
        r.raise_for_status()
        return r.json()