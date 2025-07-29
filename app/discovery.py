"""Prospect Discovery Service (CrewAI Tool)."""
from crewai_tools import Tool
import httpx, urllib.parse as ul
from app.auth import LinkedInAuth
from app.observability import logger

class LinkedInSearchTool(Tool):
    name = "linkedin_search_people"
    description = "Search LinkedIn for prospects given a boolean query string."

    def _run(self, query: str, **kwargs):
        auth = LinkedInAuth()
        token = auth.token()
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "q": "people",
            "keywords": query,
            "count": 25,
        }
        url = "https://api.linkedin.com/v2/peopleSearch?" + ul.urlencode(params)
        logger.info(f"[Discovery] LinkedIn search → {query}")
        r = httpx.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()