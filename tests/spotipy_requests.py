
import requests as rq
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import pprint as pp
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID = 'd226cb1348484b019d632c263a4bc270'
SPOTIPY_CLIENT_SECRET = '6510ffc4406148d3876d397248fd09f0'
SPOTIPY_REDIRECT_URI = 'http://localhost:7777/callback'
scope = 'user-top-read'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
token = SpotifyClientCredentials.get_access_token(SpotifyClientCredentials(), as_dict=False)
pp.pprint(token)

params = (
    ('client_id', SPOTIPY_CLIENT_ID),
    ('response_type', 'code'),
    ('redirect_uri', SPOTIPY_REDIRECT_URI),
    ('scope', scope)
)
headers = {}
response = rq.post('https://accounts.spotify.com/authorize', params=params)
pp.pprint(response)

'https://accounts.spotify.com/api/token'
