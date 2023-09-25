# Creates a playlist of the top 20 most played song from the last 4 weeks

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Instantiate sp
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri = 'http://localhost:7777/callback', username='12185848836'))

print(sp.me())
