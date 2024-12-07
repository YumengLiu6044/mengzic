import os
import base64
import sys
from requests import post, get
import fastapi


def _log(info: str):
    print("Mengzic: " + info)
    return


# Load Global Variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
AUTH_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"

if CLIENT_ID and CLIENT_SECRET:
    _log("Successfully loaded credentials")
else:
    sys.exit("Environment variables not found")


# App startup
app = fastapi.FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, welcome to Yumeng's app"}


# Gets Spotify token
def _get_token() -> str:
    auth_str = CLIENT_ID + ':' + CLIENT_SECRET
    auth_data = auth_str.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_data), encoding='utf-8')

    url = AUTH_URL
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        "grant_type": "refresh_token"
    }

    result = post(url, data=data, headers=headers)
    return result.json()


def _get_auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _search_by_artist(token: str, artist_name: str):
    url = SEARCH_URL
    headers = _get_auth_header(token)
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": 1,
        "market": "US"
    }

    result = get(url, headers=headers, params=params)
    return result.json()


def _search_by_song(token: str, song_name: str):
    url = SEARCH_URL
    headers = _get_auth_header(token)
    params = {
        "q": song_name,
        "type": "track",
        "limit": "1",
        "include_external": "audio"
    }

    result = get(url, headers=headers, params=params)
    return result.json()


if __name__ == "__main__":

    print(_get_token())
