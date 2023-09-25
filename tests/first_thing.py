import spotipy
import time
import logging
import json
import pprint as pp

from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
token = SpotifyClientCredentials.get_access_token(SpotifyClientCredentials(), as_dict=False)
pp.pprint(token)
