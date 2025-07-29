"""LLM‑powered message composer."""
from crewai_tools import Tool
from openai import OpenAI
from app.config import settings

openai_client = OpenAI(api_key=settings.openai_api_key)

class MessageComposer(Tool):
    name = "compose_message"
    description = "Craft a personalised LinkedIn connection invite. Input: dict with prospect + context."

    def _run(self, payload: dict, **kwargs):
        prompt = (
            "You are an SDR who writes *brief* but personalised LinkedIn connection requests. "
            "Use a friendly, value‑adding tone and avoid spam.\n"
            f"Prospect: {payload}\n"
            "Return ONLY the message text."
        )
        resp = openai_client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=120,
        )
        return resp.choices[0].message.content.strip()