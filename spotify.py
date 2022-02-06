import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="618100b2e5db45b1b9e01dc7f6a70c22",
        client_secret="2dffa36890634d7e9d9c9e4f3e05aac8",
        redirect_uri="http://localhost:8888/callback",
        scope="user-read-playback-state user-modify-playback-state user-read-currently-playing",
    )
)


def reset():
    sp.seek_track(0)


def pause():
    sp.pause_playback()


def play(song=None):
    if song:
        return sp.start_playback(uris=[song])
    sp.start_playback()


def playback():
    return sp.current_playback()
