import os
import sys
from requests import get
import fastapi
from pprint import pprint
from util_classes import CredentialManager


def _log(info: str):
    print("Mengzic: " + info)
    return


# Load Global Variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

SEARCH_URL = "https://api.spotify.com/v1/search"

if CLIENT_ID and CLIENT_SECRET:
    _log("Successfully loaded credentials")
else:
    sys.exit("Environment variables not found")

credential = CredentialManager(CLIENT_ID, CLIENT_SECRET)

# App startup
app = fastapi.FastAPI()
_log("App startup successful")


@app.get("/")
async def root():
    return {"message": "Hello, welcome to Yumeng's app"}


def regenerate_credential_on_fail(func):
    def execute(*args, **kwargs):
        result = func(*args, **kwargs)
        if "error" in result and result["error"]["status"] == 401:
            credential.get_access_token()
            result = func(*args, **kwargs)

        return result

    return execute


@regenerate_credential_on_fail
def _general_search(album_name: str, limit: int = 10):
    url = SEARCH_URL
    headers = credential.get_auth_header()
    params = {
        "q": album_name,
        "type": "album,track,artist",
        "limit": limit,
        "market": "US"
    }

    result = get(url, headers=headers, params=params)
    return result.json()


@regenerate_credential_on_fail
def _search_by_album(album_name: str, limit: int = 10):
    url = SEARCH_URL
    headers = credential.get_auth_header()
    params = {
        "q": album_name,
        "type": "album",
        "limit": limit,
        "market": "US"
    }

    result = get(url, headers=headers, params=params)
    return result.json()


@regenerate_credential_on_fail
def _search_by_artist(artist_name: str, limit=10):
    url = SEARCH_URL
    headers = credential.get_auth_header()
    params = {
        "q": artist_name,
        "type": "artist",
        "limit": limit,
        "market": "US"
    }

    result = get(url, headers=headers, params=params)
    return result.json()


@regenerate_credential_on_fail
def _search_by_song(song_name: str, limit=10):
    url = SEARCH_URL
    headers = credential.get_auth_header()
    params = {
        "q": song_name,
        "type": "track",
        "limit": limit,
        "include_external": "audio"
    }

    result = get(url, headers=headers, params=params)
    return result.json()
