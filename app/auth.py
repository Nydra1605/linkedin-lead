"""LinkedIn OAuth 2.0 helper (Access & Auth layer)."""
import requests, time
from datetime import datetime, timedelta
from typing import Optional
from app.config import settings

TOKEN_ENDPOINT = "https://www.linkedin.com/oauth/v2/accessToken"

class LinkedInAuth:
    _instance = None  # singleton for shared token

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._access_token = None
            cls._instance._expires_at: Optional[datetime] = None
        return cls._instance

    # --- public helpers -----------------------------------------------------
    def authorization_url(self, state: str) -> str:
        return (
            "https://www.linkedin.com/oauth/v2/authorization?response_type=code"
            f"&client_id={settings.linkedin_client_id}"
            f"&redirect_uri={settings.linkedin_redirect_uri}"
            "&scope=r_liteprofile%20r_emailaddress%20w_member_social%20rw_organization_admin"
            f"&state={state}"
        )

    def exchange_code(self, code: str) -> str:
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.linkedin_redirect_uri,
            "client_id": settings.linkedin_client_id,
            "client_secret": settings.linkedin_client_secret,
        }
        res = requests.post(TOKEN_ENDPOINT, data=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        self._access_token = data["access_token"]
        self._expires_at = datetime.utcnow() + timedelta(seconds=data["expires_in"] - 60)
        return self._access_token

    def token(self) -> str:
        if self._access_token is None or datetime.utcnow() >= self._expires_at:
            raise RuntimeError("No valid LinkedIn token – begin OAuth flow first.")
        return self._access_token