from pydantic import BaseModel
import base64
from requests import post


AUTH_URL = "https://accounts.spotify.com/api/token"


class AuthRequest(BaseModel):
    email: str
    password: str


class CredentialManager:
    access_token: str
    _client_id: str
    _client_secret: str

    def __init__(self, CLIENT_ID: str, CLIENT_SECRET: str):
        self._client_id = CLIENT_ID
        self._client_secret = CLIENT_SECRET
        self.get_access_token()

    def get_access_token(self):
        auth_str = self._client_id + ':' + self._client_secret
        auth_data = auth_str.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_data), encoding='utf-8')

        url = AUTH_URL
        headers = {
            'Authorization': 'Basic ' + auth_base64,
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            "grant_type": "client_credentials"
        }

        result = post(url, data=data, headers=headers)
        self.access_token = result.json()["access_token"]

    def get_auth_header(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}
